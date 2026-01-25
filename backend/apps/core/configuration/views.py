# apps/home/views.py
from django.shortcuts import render, redirect
from functools import wraps
from django.contrib.auth.decorators import login_required
from apps.page_notfound.views import page_not_found
from utils.function import BaseListAPIView,PageNumberPagination
from django.db.models import Q
from django.http import JsonResponse,FileResponse,Http404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
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

from utils.function import create_user_log, get_user_os_browser_architecture


# models
from apps.model_center.authorize.models import UserAuth,MainDatabase,SetAudio,UserLog,UserGroup,UserTeam
from apps.configuration.models import UserPermission,UserPermissionDetail

#serializer
from apps.model_center.authorize.serializers import MainDatabaseSerializer


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
def index_audio_search(request):

    context = {
        'test': 'test',
    }
    
    return render(request, 'audio_search/index.html', context)

@login_required(login_url='/login')
def index_group(request):
    user_group = UserGroup.objects.filter(status=1).order_by('group_name')
    user_team = UserTeam.objects.filter(status=1).order_by('name')
    database = MainDatabase.objects.filter(status=1)
    context = {
        'user_group': user_group,
        'user_team': user_team,
        'database': database,
    }
    return render(request, 'group/index.html', context)


@login_required(login_url='/login')
def index_role(request):
    
    base_user_permission = UserPermission.objects.filter(type__in=["administrator", "auditor", "operator"])
    user_permission_other = UserPermission.objects.exclude(type__in=["administrator", "auditor", "operator"]).order_by('name')
    user_permission_detail = UserPermissionDetail.objects.exclude(user_permission__in=["1", "2", "3"])

    context = { 
               'base_user_permission': base_user_permission,
               'user_permission_other': user_permission_other,
               'user_permission_detail': user_permission_detail 
            }
       
    return render(request, 'role/index.html', context)

def get_role_details(request):
    role_id = request.GET.get('role_id')
    
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

@require_POST
@login_required(login_url='/login')
def create_role(request):
    try:
        data = json.loads(request.body)
        role_name = data.get('role_name', '').strip()
        permissions = data.get('permissions', []) # List of action IDs

        if not role_name:
            return JsonResponse({'status': 'error', 'message': 'Role name is required.'})

        # Check for duplicate name
        if UserPermission.objects.filter(name__iexact=role_name).exists():
            return JsonResponse({'status': 'error', 'message': 'Role name already exists.'})

        with transaction.atomic():
            # Create Role
            new_role = UserPermission.objects.create(type='role_other', name=role_name)

            # Use 'administrator' as a template for all possible actions
            admin_role = UserPermission.objects.filter(type='administrator').first()
            
            if admin_role:
                admin_details = UserPermissionDetail.objects.filter(user_permission=admin_role)
                new_details = []
                
                for detail in admin_details:
                    # Check if this action is in the selected permissions
                    is_active = str(detail.action) in map(str, permissions)
                    
                    new_details.append(UserPermissionDetail(
                        user_permission=new_role,
                        action=detail.action,
                        status=is_active,
                        type=detail.type,
                        default='t' if is_active else 'f'
                    ))
                
                UserPermissionDetail.objects.bulk_create(new_details)

            # Log the action
            create_user_log(user=request.user, action="Create Custom Role", detail=f"Created role: {role_name}",status="success", request=request)

        return JsonResponse({
            'status': 'success', 
            'message': 'Role created successfully.',
            'role': {
                'id': new_role.id,
                'name': new_role.name,
                'type': new_role.type
            }
        })

    except Exception as e:
        create_user_log(user=request.user, action="Create Custom Role", detail=f"Error creating role: {str(e)}", status="error", request=request)
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_POST
@login_required(login_url='/login')
def update_role(request):
    try:
        data = json.loads(request.body)
        role_id = data.get('role_id')
        role_name = data.get('role_name', '').strip()
        permissions = data.get('permissions', [])

        if not role_id or not role_name:
            return JsonResponse({'status': 'error', 'message': 'Role ID and Name are required.'})

        role = UserPermission.objects.filter(id=role_id).first()
        if not role:
            return JsonResponse({'status': 'error', 'message': 'Role not found.'})

        # Check duplicate name (excluding current role)
        if UserPermission.objects.filter(name__iexact=role_name).exclude(id=role_id).exists():
            return JsonResponse({'status': 'error', 'message': 'Role name already exists.'})

        with transaction.atomic():
            role.name = role_name
            role.save()

            # Update Permissions
            details = UserPermissionDetail.objects.filter(user_permission=role)
            for detail in details:
                is_active = str(detail.action) in map(str, permissions)
                detail.status = is_active
                detail.save()

            create_user_log(user=request.user, action="Update Custom Role", detail=f"Updated role: {role_name}", status="success", request=request)

        return JsonResponse({'status': 'success', 'message': 'Role updated successfully.', 'role': {'id': role.id, 'name': role.name}})

    except Exception as e:
        create_user_log(user=request.user, action="Update Custom Role", detail=f"Error updating role: {str(e)}", status="error", request=request)
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_POST
@login_required(login_url='/login')
def delete_role(request):
    try:
        data = json.loads(request.body)
        role_id = data.get('role_id')
        role = UserPermission.objects.filter(id=role_id).first()
        
        if role:
            role_name = role.name
            role.delete() # Cascade delete should handle details
            create_user_log(user=request.user, action="Delete Custom Role", detail=f"Deleted role: {role_name}", status="success", request=request)
            return JsonResponse({'status': 'success', 'message': 'Role deleted successfully.', 'role': {'id': role.id, 'name': role.name}})
        return JsonResponse({'status': 'error', 'message': 'Role not found.'})
    except Exception as e:
        create_user_log(user=request.user, action="Delete Custom Role", detail=f"Error deleting role: {str(e)}", status="error", request=request)
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url='/login')
def create_form_group(request):
    
    user_group = UserGroup.objects.filter(status=1).first()

    context = {
        'test': 'test',
    }
    return render(request, 'group/create.html', context)


@login_required(login_url='/login')
def index_team(request):
    user_team = UserTeam.objects.filter(status=1).order_by('name')
    context = {
        'user_team': user_team,
    }
    return render(request, 'team/index.html', context)

@login_required(login_url='/login')
def create_config_group(request):
    post_data = request.POST.dict()
    group_name = (post_data.get("group_name") or "").strip()  # ตัดช่องว่างหัวท้าย
    description = post_data.get("description", "")

    if not group_name:
        return JsonResponse({"status": "error", "message": "Group name is required."})

    try:
        # ตรวจสอบว่ามีชื่อซ้ำ 
        existing_group = UserGroup.objects.filter(group_name__iexact=group_name).first()
        if existing_group:
            # บันทึก log (error)
            create_user_log(user=request.user,action="Create Config Group",detail=f"Duplicate group : {group_name}",status="error",request=request)
            return JsonResponse({"status": "error", "message": "This group name is already in the system."})

        with transaction.atomic():
            # สร้าง group ใหม่
            new_group = UserGroup.objects.create(
                group_name=group_name,
                description=description,
                status=1
            )

            # บันทึก log (success)
            create_user_log(user=request.user,action="Create Config Group",detail=f"Created group : {group_name} | Description: {description}",status="success",request=request)

            context = {
                'status': "success",
                'group': {
                    'id': new_group.id,
                    'group_name': new_group.group_name,
                    'description': new_group.description
                }
            }

        return JsonResponse(context)

    except IntegrityError as e:
        # Log กรณี error จาก database
        create_user_log(user=request.user,action="Create Config Group",detail=f"Database error : {str(e)}",status="error",request=request)
        return JsonResponse({"status": "error", "message": "เกิดข้อผิดพลาดกับฐานข้อมูล"})

    except Exception as e:
        # Log กรณี error อื่น ๆ
        create_user_log(user=request.user,action="Create Config Group",detail=f"Unexpected error: {str(e)}",status="error",request=request)
        
        return JsonResponse({"status": "error", "message": f"เกิดข้อผิดพลาด: {str(e)}"})

@login_required(login_url='/login')
def get_group_details(request):
    group_id = request.GET.get('group_id')
    group = UserGroup.objects.filter(id=group_id).first()
    if not group:
        return JsonResponse({'status': 'error', 'message': 'Group not found'})
    
    return JsonResponse({
        'status': 'success',
        'group': {
            'id': group.id,
            'group_name': group.group_name,
            'description': group.description
        }
    })

@require_POST
@login_required(login_url='/login')
def update_config_group(request):
    post_data = request.POST.dict()
    group_id = post_data.get('group_id')
    group_name = (post_data.get("group_name") or "").strip()
    description = post_data.get("description", "")

    if not group_id or not group_name:
        return JsonResponse({"status": "error", "message": "Group ID and Name are required."})

    try:
        group = UserGroup.objects.filter(id=group_id).first()
        if not group:
            return JsonResponse({"status": "error", "message": "Group not found."})

        # Check duplicate name (exclude self)
        if UserGroup.objects.filter(group_name__iexact=group_name).exclude(id=group_id).exists():
            create_user_log(user=request.user, action="Update Config Group", detail=f"Duplicate group : {group_name}", status="error", request=request)
            return JsonResponse({"status": "error", "message": "This group name is already in the system."})

        with transaction.atomic():
            group.group_name = group_name
            group.description = description
            group.save()
            
            create_user_log(user=request.user, action="Update Config Group", detail=f"Updated group : {group_name}", status="success", request=request)

        return JsonResponse({
            "status": "success", 
            "group": {
                "id": group.id,
                "group_name": group.group_name,
                "description": group.description
            }
        })
    except Exception as e:
        create_user_log(user=request.user, action="Update Config Group", detail=f"Error: {str(e)}", status="error", request=request)
        return JsonResponse({"status": "error", "message": str(e)})

@require_POST
@login_required(login_url='/login')
def delete_config_group(request):
    try:
        data = json.loads(request.body)
        group_id = data.get('group_id')
        group = UserGroup.objects.filter(id=group_id).first()
        
        if group:
            group_name = group.group_name
            group.delete()
            create_user_log(user=request.user, action="Delete Config Group", detail=f"Deleted group: {group_name}", status="success", request=request)
            return JsonResponse({'status': 'success', 'message': 'Group deleted successfully.'})
        return JsonResponse({'status': 'error', 'message': 'Group not found.'})
    except Exception as e:
        create_user_log(user=request.user, action="Delete Config Group", detail=f"Error deleting group: {str(e)}", status="error", request=request)
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url='/login')
def get_teams_by_group(request):
    group_id = request.GET.get('group_id')
    if not group_id:
        return JsonResponse({'status': 'error', 'message': 'Group ID is required'})
    
    teams = UserTeam.objects.filter(user_group_id=group_id, status=1).select_related('user_group').order_by('name')
    
    team_list = []
    for team in teams:
        team_list.append({
            'id': team.id,
            'name': team.name,
            'group_name': team.user_group.group_name
        })
        
    return JsonResponse({'status': 'success', 'teams': team_list})

@login_required(login_url='/login')
def get_group_list(request):
    groups = UserGroup.objects.filter(status=1).values('id', 'group_name').order_by('group_name')
    return JsonResponse({'status': 'success', 'groups': list(groups)})

@login_required(login_url='/login')
def create_form_team(request):
    main_db = MainDatabase.objects.all()

    context = {
        'main_db':main_db,}
    return render(request, 'team/create.html', context)
    
@login_required(login_url='/login')
def create_config_team(request):
    post_data = request.POST.dict()
    group_id = post_data.get("group")
    team = post_data.get("team_name")
    
    # Support both list of IDs and individual keys
    if "database_ids" in request.POST:
        maindatabase_ids = request.POST.getlist("database_ids")
    else:
        maindatabase_ids = [
            post_data.get("db_id-1"),
            post_data.get("db_id-2"),
            post_data.get("db_id-3"),
            post_data.get("db_id-4"),
        ]
    # กรองค่า None หรือค่าว่างออกก่อน
    maindatabase_ids = [db_id for db_id in maindatabase_ids if db_id]

    server_ip = socket.gethostbyname(socket.gethostname())
    info = get_user_os_browser_architecture(request)

    try:
        # ✅ ดึง instance ของ group
        user_group = UserGroup.objects.filter(id=group_id).first()
        if not user_group:
            return JsonResponse({"status": "error", "message": "ไม่พบกลุ่มที่เลือก"})

        # ✅ ตรวจสอบชื่อทีมซ้ำ
        if UserTeam.objects.filter(name__iexact=team).exists():
            UserLog.objects.create(
                user=request.user,
                action="Create Config Team",
                timestamp=timezone.now(),
                detail=f"Duplicate team : {team}",
                ip_address=server_ip,
                audiofile_id=None,
                client_type=f"{info['os']} / {info['browser']}",
                status="error"
            )
            return JsonResponse({"status": "error", "message": "ชื่อทีมนี้มีอยู่ในระบบแล้ว"})

        # ✅ ดึงชื่อฐานข้อมูล
        main_dbs = MainDatabase.objects.filter(id__in=maindatabase_ids)
        db_names = [db.database_name for db in main_dbs]
        db_name_str = ", ".join(db_names) if db_names else "No database selected"

        with transaction.atomic():
            # ✅ สร้างทีมใหม่
            new_team = UserTeam.objects.create(
                name=team,
                user_group=user_group,
                maindatabase=json.dumps(maindatabase_ids),  # เก็บเป็น JSON
            )

            # ✅ บันทึก log
            UserLog.objects.create(
                user=request.user,
                action="Create Config Team",
                timestamp=timezone.now(),
                detail=(
                    f"Created Team: {team} | "
                    f"Group: {user_group.group_name} | "
                    f"Main Database: {db_name_str}"
                ),
                ip_address=server_ip,
                audiofile_id=None,
                client_type=f"{info['os']} / {info['browser']}",
                status="success"
            )

        return JsonResponse({
            'status': 'success',
            'team': {
                'id': new_team.id,
                'name': new_team.name,
                'group_name': user_group.group_name,
                'group_id': user_group.id
            }
        })

    except IntegrityError as e:
        UserLog.objects.create(
            user=request.user,
            action="Create Config Team",
            timestamp=timezone.now(),
            detail=f"Database error : {str(e)}",
            ip_address=server_ip,
            audiofile_id=None,
            client_type=f"{info['os']} / {info['browser']}",
            status="error"
        )
        return JsonResponse({"status": "error", "message": "เกิดข้อผิดพลาดกับฐานข้อมูล"})

    except Exception as e:
        UserLog.objects.create(
            user=request.user,
            action="Create Config Team",
            timestamp=timezone.now(),
            detail=f"Unexpected error: {str(e)}",
            ip_address=server_ip,
            audiofile_id=None,
            client_type=f"{info['os']} / {info['browser']}",
            status="error"
        )
        return JsonResponse({"status": "error", "message": f"เกิดข้อผิดพลาด: {str(e)}"})
    
@require_POST
@login_required(login_url='/login')
def delete_config_team(request):
    try:
        data = json.loads(request.body)
        team_id = data.get('team_id')
        team = UserTeam.objects.filter(id=team_id).first()
        
        if team:
            team_name = team.name
            group_id = team.user_group_id
            team.delete()
            create_user_log(user=request.user, action="Delete Config Team", detail=f"Deleted team: {team_name}", status="success", request=request)
            return JsonResponse({
                'status': 'success', 
                'message': 'Team deleted successfully.',
                'deleted_team_name': team_name,
                'group_id': group_id
            })
        return JsonResponse({'status': 'error', 'message': 'Team not found.'})
    except Exception as e:
        create_user_log(user=request.user, action="Delete Config Team", detail=f"Error deleting team: {str(e)}", status="error", request=request)
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url='/login')
def get_team_details(request):
    team_id = request.GET.get('team_id')
    team = UserTeam.objects.filter(id=team_id).first()
    if not team:
        return JsonResponse({'status': 'error', 'message': 'Team not found'})
    
    try:
        db_ids = json.loads(team.maindatabase)
    except:
        db_ids = []

    return JsonResponse({
        'status': 'success',
        'team': {
            'id': team.id,
            'name': team.name,
            'group_id': team.user_group_id,
            'database_ids': db_ids
        }
    })

@require_POST
@login_required(login_url='/login')
def update_config_team(request):
    post_data = request.POST.dict()
    team_id = post_data.get('team_id')
    group_id = post_data.get("group")
    team_name = post_data.get("team_name")
    
    if "database_ids" in request.POST:
        maindatabase_ids = request.POST.getlist("database_ids")
    else:
        maindatabase_ids = []
    
    maindatabase_ids = [db_id for db_id in maindatabase_ids if db_id]

    if not team_id or not team_name or not group_id:
         return JsonResponse({"status": "error", "message": "Missing required fields."})

    try:
        team = UserTeam.objects.filter(id=team_id).first()
        if not team:
            return JsonResponse({"status": "error", "message": "Team not found."})

        user_group = UserGroup.objects.filter(id=group_id).first()
        if not user_group:
             return JsonResponse({"status": "error", "message": "Group not found."})

        # Check duplicate name (exclude self)
        if UserTeam.objects.filter(name__iexact=team_name).exclude(id=team_id).exists():
             return JsonResponse({"status": "error", "message": "This team name is already in the system."})

        with transaction.atomic():
            team.name = team_name
            team.user_group = user_group
            team.maindatabase = json.dumps(maindatabase_ids)
            team.save()
            
            create_user_log(user=request.user, action="Update Config Team", detail=f"Updated team: {team_name}", status="success", request=request)

        return JsonResponse({
            'status': 'success',
            'team': {
                'id': team.id,
                'name': team.name,
                'group_name': user_group.group_name,
                'group_id': user_group.id
            }
        })
    except Exception as e:
        create_user_log(user=request.user, action="Update Config Team", detail=f"Error updating team: {str(e)}", status="error", request=request)
        return JsonResponse({"status": "error", "message": str(e)})
    