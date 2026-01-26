# apps/home/views.py
from django.shortcuts import render, redirect
from functools import wraps
from django.contrib.auth.decorators import login_required
# from apps.page_notfound.views import page_not_found
from apps.core.utils.function import BaseListAPIView, PageNumberPagination
from django.db.models import Q
from django.http import JsonResponse,FileResponse,Http404
from django.core import serializers
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction, DatabaseError,IntegrityError
import socket
import uuid
import os
from django.conf import settings
from user_agents import parse
from django.utils import timezone
import json

from apps.core.utils.function import create_user_log, get_user_os_browser_architecture


# models
from apps.core.model.authorize.models import UserAuth,MainDatabase,UserLog,UserGroup,UserTeam
from apps.configuration.models import UserPermission,UserPermissionDetail

#serializer
from apps.core.model.authorize.serializers import MainDatabaseSerializer


def check_permission(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user_auth = UserAuth.objects.filter(user=user).first()
            if user_auth and not user_auth.status:
                return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required(login_url='/login')
def ApiIndexRole(request):
    
    base_user_permission_qs = UserPermission.objects.filter(type__in=["administrator", "auditor", "operator"])
    user_permission_other_qs = UserPermission.objects.exclude(type__in=["administrator", "auditor", "operator"]).order_by('name')
    user_permission_detail_qs = UserPermissionDetail.objects.exclude(user_permission__in=["1", "2", "3"])

    # Convert QuerySets to plain lists/dicts so JsonResponse can serialize them
    base_user_permission = list(base_user_permission_qs.values())
    user_permission_other = list(user_permission_other_qs.values())
    user_permission_detail = list(user_permission_detail_qs.values())

    return JsonResponse({
        'base_user_permission': base_user_permission,
        'user_permission_other': user_permission_other,
        'user_permission_detail': user_permission_detail,
    })

def ApiGetRoleDetails(request, role_id):
    
    # 1. Find the role object by type
    role = UserPermission.objects.filter(id=role_id).first()
    
    if not role:
        return JsonResponse({'status': False, 'message': 'Role not found'})

    # 2. Get details (actions) for this role
    # Assuming UserPermissionDetail contains rows for all actions (active and inactive)
    details = UserPermissionDetail.objects.filter(user_permission=role).order_by('action').order_by('id')
    
    all_permissions = []
    role_permissions = []
    default_permissions = []
    
    for detail in details:
        # Use 'action' (int) as the identifier (action)
        # Since model has no name for action, we generate one or use the ID
        all_permissions.append({
            'action': detail.action,
            'name': f"{detail.action}",  # Or map this to a real name if you have a mapping
            'type': detail.type
        })
        
        if detail.status:
            role_permissions.append(detail.action)
        
        if detail.default:
            default_permissions.append(detail.action)
        
    return JsonResponse({
        'status': True,
        'role_name': role.name,
        'role_type': role.type,
        'all_permissions': all_permissions,
        'role_permissions': role_permissions,
        'default_permissions': default_permissions
    })


