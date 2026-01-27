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

@login_required(login_url='/login')
def ApiGetRoleDetails(request, role_id):
    try:
        role_id = int(role_id)
    except (ValueError, TypeError):
        return JsonResponse({'status': False, 'message': 'Invalid role_id'}, status=400)

    role = UserPermission.objects.filter(pk=role_id).first()
    if not role:
        return JsonResponse({'status': False, 'message': 'Role not found'}, status=404)

    # Basic permission check: only staff or users with explicit permission may view role details
    user = request.user
    if not (user.is_staff or user.has_perm('configuration.view_userpermission')):
        return JsonResponse({'status': False, 'message': 'Permission denied'}, status=403)

    details = UserPermissionDetail.objects.filter(user_permission=role).order_by('action', 'id')

    all_permissions = []
    role_permissions = []
    default_permissions = []

    for detail in details:
        all_permissions.append({
            'action': detail.action,
            'name': f"{detail.action}",
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
    
def ApiIndexGroup(request):
    user_group = UserGroup.objects.filter(status=1).order_by('group_name')
    user_team = UserTeam.objects.filter(status=1).order_by('name')
    database = MainDatabase.objects.filter(status=1)
    
    return JsonResponse({
        'user_group': list(user_group.values()),
        'user_team': list(user_team.values()),
        'database': list(database.values()),
    })
    
def ApiGetTeamByGroup(request, group_id):
    try:
        group_id = int(group_id)
    except (ValueError, TypeError):
        return JsonResponse({'status': False, 'message': 'Invalid group_id'}, status=400)
    
    teams = UserTeam.objects.filter(user_group_id=group_id, status=1).select_related('user_group').order_by('name')
    
    team_list = []
    for team in teams:
        team_list.append({
            'id': team.id,
            'name': team.name,
            'group_name': team.user_group.group_name
        })
        
    return JsonResponse({'status': 'success', 'teams': team_list})

class MainDatabaseAPIView(BaseListAPIView):
    serializer_class = MainDatabaseSerializer

    def get_queryset(self):
        queryset = MainDatabase.objects.all()
        return queryset