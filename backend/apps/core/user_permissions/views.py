# apps/home/views.py
from django.shortcuts import render, redirect
from functools import wraps
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
from apps.model_center.authorize.models import MainDatabase,UserAuth,UserProfile,Department,MainDatabase,UserGroup,UserTeam,UserLog

from apps.model_center.licenses.models import License,UserLicense

from apps.configuration.models import UserPermission,UserPermissionDetail



#serializer
from apps.model_center.authorize.serializers import UserProfileSerializer,DepartmentSerializer,UserGroupSerializer,UserTeamSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class NoLimitPagination(PageNumberPagination):
    page_size = 1000  

def page_not_found(request, exception=None):
    return render(request, 'page_notfound/index.html', status=404)

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
def index(request):
    user_profiles = UserProfile.objects.exclude(user=request.user).select_related(
        'user', 'team'
    )

    user_auths = UserAuth.objects.filter(
        allow=True,
        user_permission__isnull=False
    ).select_related(
        'user', 'maindatabase', 'user_permission'
    )

    # group auth ตาม user
    auth_map = {}
    for auth in user_auths:
        auth_map.setdefault(auth.user_id, []).append(auth)

    main_db_ids = set(
        MainDatabase.objects.filter(status=True).values_list('id', flat=True)
    )

    for profile in user_profiles:
        auths = auth_map.get(profile.user_id, [])

        # ✅ permission เดียว
        profile.permission = auths[0].user_permission.name if auths else None

        # ✅ database
        allowed_db_ids = {auth.maindatabase_id for auth in auths}

        if allowed_db_ids == main_db_ids and allowed_db_ids:
            profile.database_servers = "ALL"
        elif allowed_db_ids:
            profile.database_servers = [
                auth.maindatabase.database_name for auth in auths
            ]
        else:
            profile.database_servers = None

    return render(request, 'user_permissions/index.html', {
        'user_profile': user_profiles
    })
    
    

class UserGroupAPIView(BaseListAPIView):
    pagination_class = NoLimitPagination
    serializer_class = UserGroupSerializer

    def get_queryset(self):
        queryset = UserGroup.objects.filter(status=1)
        return queryset
    
def user_team(request):
    group_id = request.GET.get("group_id", None)

    user_team = UserTeam.objects.filter(user_group=group_id).values("id", "name")

    return JsonResponse({
        "results": list(user_team)
    })
    

@login_required(login_url='/login')
def user_add(request):

    # ดึงเฉพาะ user ที่ active แต่ไม่รวม user ปัจจุบัน
    User = get_user_model()
    user_auth = User.objects.filter(is_active=True).exclude(id=request.user.id)
    user_profile = UserProfile.objects.filter(user__in=user_auth)
    main_db = MainDatabase.objects.all()
    licenses = License.objects.all()

    context = {
        'main_db':main_db,
        'user_profile': user_profile,
        'licenses': licenses
    }
    return render(request, 'add_user/index.html', context)

@login_required(login_url='/login')
def user_edit(request, user_id):
    try:
        # Get user and related data
        user_to_edit = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.filter(user=user_to_edit).first()
        
        # Get all databases for the scope card
        main_db = MainDatabase.objects.all()
        
        # Get user's selected databases
        user_auths = UserAuth.objects.filter(user=user_to_edit)
        selected_db_ids = [str(auth.maindatabase.id) for auth in user_auths if auth.allow]
        
        # Check if all are selected
        all_db_selected = len(selected_db_ids) == main_db.count() and main_db.count() > 0

        # Get user's role
        # Assuming one role per user for simplicity, stored on the first auth record
        user_permission = user_auths.first().user_permission if user_auths.exists() and user_auths.first().user_permission else None
        selected_role_id = None
        selected_role_type = None
        if user_permission:
            if user_permission.type in ['administrator', 'auditor', 'operator']:
                selected_role_type = user_permission.type
            else:
                selected_role_id = str(user_permission.id)

        context = {
            'user_to_edit': user_to_edit,
            'user_profile': user_profile,
            'main_db': main_db,
            'selected_db_ids_json': json.dumps(selected_db_ids),
            'all_db_selected_json': json.dumps(all_db_selected),
            'selected_role_id_json': json.dumps(selected_role_id),
            'selected_role_type_json': json.dumps(selected_role_type),
        }
        return render(request, 'edit_user/index.html', context)
    except User.DoesNotExist:
        return redirect('user_permissions:index')

@login_required
@require_POST
def update_user(request, user_id):
    try:
        user_to_update = User.objects.get(id=user_id)
        profile_to_update = UserProfile.objects.get(user=user_to_update)
        
        post_data = request.POST

        # Check for username duplication (excluding self)
        new_username = post_data.get('username', user_to_update.username)
        if User.objects.filter(username=new_username).exclude(id=user_id).exists():
            return JsonResponse({"status": "error", "message": "This name is already in the system."})

        with transaction.atomic():
            user_to_update.username = new_username
            user_to_update.first_name = post_data.get('first_name', user_to_update.first_name)
            user_to_update.last_name = post_data.get('last_name', user_to_update.last_name)
            user_to_update.email = post_data.get('email', user_to_update.email)
            
            password = post_data.get('password')
            if password:
                user_to_update.set_password(password)
            user_to_update.save()

            profile_to_update.phone = post_data.get('phone', profile_to_update.phone)
            team_id = post_data.get('team')
            if team_id:
                profile_to_update.team = UserTeam.objects.filter(id=team_id).first()
            profile_to_update.save()

            # --- Update Role and Select Database Server ---
            role_input = post_data.get('role', None)
            user_permission_obj = None
            if role_input:
                if role_input.isdigit():
                    user_permission_obj = UserPermission.objects.filter(id=role_input).first()
                else:
                    user_permission_obj = UserPermission.objects.filter(type=role_input).first()

            # Reset UserAuth (Delete old and create new)
            UserAuth.objects.filter(user=user_to_update).delete()
            
            main_dbs = MainDatabase.objects.all()
            is_all_dbs = post_data.get('db_id-all') == 'all'
            
            user_auths = []
            for db in main_dbs:
                allow = True if is_all_dbs else bool(post_data.get(f'db_id-{db.id}', None))
                user_auths.append(UserAuth(
                    user=user_to_update,
                    maindatabase=db,
                    allow=allow,
                    user_permission=user_permission_obj
                ))
            UserAuth.objects.bulk_create(user_auths)

        create_user_log(user=request.user, action="Update User", detail=f"Updated user: {user_to_update.username}", status="success", request=request)
        return JsonResponse({'status': 'success', 'message': 'User updated successfully.', 'username': user_to_update.username})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'})
    except Exception as e:
        create_user_log(user=request.user, action="Update User", detail=f"Error updating user: {str(e)}", status="error", request=request)
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'})

def running_app(user_code: str):
    latest_profile = UserProfile.objects.filter(user_code=user_code).first()
    if latest_profile:
        latest_app_id = latest_profile.user_code
        running_no = latest_app_id[-4:]
        new_running_no = str(int(running_no) + 1).zfill(4)
        app_id = latest_app_id[:-4] + new_running_no
    else:
        app_id = user_code + '0001'

    return app_id

@login_required(login_url='/login')
def create(request):

    User = get_user_model()
    post_data = request.POST.dict()

    username = post_data.get('username', None)
    password = post_data.get('password', None)
    email = post_data.get('email', None)
    first_name = post_data.get('first_name', None)
    last_name = post_data.get('last_name', None)
    phone = post_data.get('phone', None)

    # Get Role and Team
    role_input = post_data.get('role', None)
    team_id = post_data.get('team', None)
    
    user_permission_obj = None
    if role_input:
        if role_input.isdigit():
            user_permission_obj = UserPermission.objects.filter(id=role_input).first()
        else:
            user_permission_obj = UserPermission.objects.filter(type=role_input).first()
            
    team_obj = UserTeam.objects.filter(id=team_id).first() if team_id else None

    # Check if username exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": "error", "message": "This name is already in the system."})

    try:
        with transaction.atomic():
            auth_user_create = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=True,
            )

            if auth_user_create:
                main_dbs = list(MainDatabase.objects.only('id').order_by('id'))

                is_all_dbs = post_data.get('db_id-all') == 'all'

                user_auths = []
                for db in main_dbs:
                    if is_all_dbs:
                        db_select = post_data.get(f'db_id-{db.id}', None)
                        allow = True
                    else:
                        db_select = post_data.get(f'db_id-{db.id}', None)
                        allow = bool(db_select)
                    user_auths.append(UserAuth(
                        user=auth_user_create,
                        maindatabase=db,
                        allow=allow,
                        user_permission=user_permission_obj
                    ))
                UserAuth.objects.bulk_create(user_auths)

                UserProfile.objects.create(
                    user=auth_user_create,
                    phone=phone,
                    team=team_obj
                )

            context = {
                'status': "success",
                'message': "User created successfully",
                'username': username
            }
            create_user_log(user=request.user, action="Created User", detail=f"User created successfully: {username}", status="success", request=request)
        return JsonResponse(context)

    except IntegrityError as e:
        error_message = str(e)
        create_user_log(user=request.user, action="Created User",  detail=f"IntegrityError: {error_message}", status="error", request=request)
        return JsonResponse({"status": "error", "message": "Error: " + error_message})

    except Exception as e:
        create_user_log(user=request.user, action="Created User", detail=f"Error: {str(e)}", status="error", request=request)
        return JsonResponse({"status": "error", "message": f"Error: {str(e)}"})


@login_required(login_url='/login')
def get_team_maindatabase(request):
    team_id = request.GET.get("team_id")
    try:
        team = UserTeam.objects.get(id=team_id)
        maindatabase_ids = json.loads(team.maindatabase)  # ["1", "2", "3"]
        return JsonResponse({"status": "success", "maindatabase_ids": maindatabase_ids})
    except UserTeam.DoesNotExist:
        return JsonResponse({"status": "error", "message": "ไม่พบทีม"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    
@login_required
@require_POST
def change_user_status(request, user_id):
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
def delete_user_permission(request, user_id):
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
def get_all_roles_permissions(request):
    try:
        # 1. Get all available permissions (definitions) from Administrator role (template)
        # Assuming Administrator has all possible permissions
        admin_role = UserPermission.objects.filter(type='administrator').first()
        all_perms_data = []
        
        if admin_role:
            # Get all details to list available actions
            details = UserPermissionDetail.objects.filter(user_permission=admin_role).order_by('type', 'action')
            for d in details:
                all_perms_data.append({
                    'action': d.action,
                    'name': d.action.replace('-', ' ').title(), # Format name nicely e.g. "system-access" -> "System Access"
                    'type': d.type
                })

        # 2. Get Roles and their active permissions
        roles = UserPermission.objects.all()
        roles_permissions = {}
        custom_roles = []

        for role in roles:
            # Get active permissions for this role
            active_actions = list(UserPermissionDetail.objects.filter(
                user_permission=role, 
                status=True
            ).values_list('action', flat=True))
            
            if role.type in ['administrator', 'auditor', 'operator']:
                roles_permissions[role.type] = active_actions
            else:
                # Custom roles
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

@login_required(login_url='/login')
def check_username(request):
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
