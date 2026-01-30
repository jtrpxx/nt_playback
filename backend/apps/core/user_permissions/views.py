from django.contrib.auth.decorators import login_required
# from apps.page_notfound.views import page_not_found
from utils.function import BaseListAPIView,PageNumberPagination
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
import os
import subprocess
from django.db import transaction, DatabaseError,IntegrityError
from django.contrib import messages
from utils.function import create_user_log

# models
from apps.core.model.authorize.models import MainDatabase,UserAuth,UserProfile,Department,MainDatabase,UserGroup,UserTeam,UserLog

from apps.core.model.licenses.models import License,UserLicense

from apps.configuration.models import UserPermission,UserPermissionDetail



#serializer
from apps.core.model.authorize.serializers import UserProfileSerializer,DepartmentSerializer,UserGroupSerializer,UserTeamSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

@login_required(login_url='/login')
def ApiGetAllRolesPermissions(request):
    try:
        admin_role = UserPermission.objects.filter(type='administrator').first()
        all_perms_data = []
        
        if admin_role:
            details = UserPermissionDetail.objects.filter(user_permission=admin_role).order_by('type', 'action')
            for d in details:
                all_perms_data.append({
                    'action': d.action,
                    'name': d.action.replace('-', ' ').title(), 
                    'type': d.type
                })

        roles = UserPermission.objects.all()
        roles_permissions = {}
        custom_roles = []

        for role in roles:
            active_actions = list(UserPermissionDetail.objects.filter(
                user_permission=role, 
                status=True
            ).values_list('action', flat=True))
            
            if role.type in ['administrator', 'auditor', 'operator']:
                roles_permissions[role.type] = active_actions
            else:
                roles_permissions[str(role.id)] = active_actions
                custom_roles.append({
                    'id': role.id,
                    'name': role.name,
                    'permissions': active_actions
                })

        return JsonResponse({
            'status': 'success',
            'all_permissions': all_perms_data,
            'roles_permissions': roles_permissions,
            'custom_roles': custom_roles
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



@login_required
@require_POST
def ChangeUserStatus(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        if user == request.user:
            return JsonResponse({'status': 'error', 'message': 'Cannot change your own status.'})
            
        user.is_active = not user.is_active
        user.save()
        
        status_msg = "Active" if user.is_active else "Inactive"
        create_user_log(user=request.user, action="Change User Status", detail=f"Changed status of {user.username} to {status_msg}", status="success", request=request)
        
        return JsonResponse({'status': 'success', 'message': f'User is now {status_msg}.'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@login_required
@require_POST
def DeleteUserPermission(request, user_id):
    """
    Hard deletes a user and cleans up related data to avoid foreign key constraints.
    """
    print('user_id',user_id)
    try:
        user_to_delete = User.objects.get(id=user_id)

        if user_to_delete.is_superuser:
            create_user_log(user=request.user, action="Delete User", detail=f"Attempted to delete superuser: {user_to_delete.username}", status="error", request=request)
            return JsonResponse({'status': 'error', 'message': 'Cannot delete a superuser.'})
        if user_to_delete == request.user:
            create_user_log(user=request.user, action="Delete User", detail=f"Attempted to delete self: {user_to_delete.username}", status="error", request=request)
            return JsonResponse({'status': 'error', 'message': 'Cannot delete your own account.'})

        username = user_to_delete.username 
        
        with transaction.atomic():
            # 1. ลบ Logs ของ User นี้ก่อน (มักเป็นสาเหตุหลักของ FK Constraint แบบ PROTECT)
            UserLog.objects.filter(user=user_to_delete).delete()
            
            # 2. ลบข้อมูล Auth และ Profile (ปกติจะเป็น CASCADE แต่ลบเพื่อความชัวร์)
            UserAuth.objects.filter(user=user_to_delete).delete()
            UserProfile.objects.filter(user=user_to_delete).delete()
            
            # 3. ลบ User ออกจากระบบ
            user_to_delete.delete()

        create_user_log(user=request.user, action="Delete User", detail=f"Successfully deleted user: {username} (ID: {user_id})", status="success", request=request)
        return JsonResponse({'status': 'success', 'message': 'User deleted successfully.', 'username': username})
    except User.DoesNotExist:
        create_user_log(user=request.user, action="Delete User", detail=f"Attempted to delete non-existent user with ID: {user_id}", status="error", request=request)
        return JsonResponse({'status': 'error', 'message': 'User not found.'})
    except Exception as e:
        create_user_log(user=request.user, action="Delete User", detail=f"Failed to delete user with ID: {user_id}", status="error", request=request, exception=e)
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})


@login_required(login_url='/login')
def CheckUsername(request):
    username = request.GET.get('username', None)
    user_id = request.GET.get('user_id', None)
    if not username:
        return JsonResponse({'status': 'error', 'message': 'Username is required'})
    
    query = User.objects.filter(username=username)
    if user_id:
        query = query.exclude(id=user_id)

    if query.exists():
        return JsonResponse({'status': 'success', 'is_taken': True, 'message': 'This name is already in the system.'})
    else:
        return JsonResponse({'status': 'success', 'is_taken': False})
