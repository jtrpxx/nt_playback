# apps/home/views.py
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction, DatabaseError,IntegrityError
from django.db.models import Q
import re
from django.contrib import messages
from apps.core.utils.function import create_user_log
import json

# models
from apps.core.model.authorize.models import MainDatabase,UserAuth,UserProfile,Department,MainDatabase,UserGroup,UserTeam,UserLog


from apps.configuration.models import UserPermission,UserPermissionDetail

#serializer
from apps.core.model.authorize.serializers import UserProfileSerializer,DepartmentSerializer,UserGroupSerializer,UserTeamSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

@login_required(login_url='/login')
def ApiGetUser(request):
    # prepare base query
    qs = UserProfile.objects.exclude(user=request.user).select_related('user', 'team')

    user_auths = UserAuth.objects.filter(
        allow=True,
        user_permission__isnull=False
    ).select_related('user', 'maindatabase', 'user_permission')

    auth_map = {}
    for auth in user_auths:
        auth_map.setdefault(auth.user_id, []).append(auth)

    main_db_ids = set(MainDatabase.objects.filter(status=True).values_list('id', flat=True))

    # apply search filter if provided (DataTables style: search[value])
    search_term = (request.GET.get('search[value]') or request.GET.get('search') or '').strip()
    if search_term:
        # split on whitespace and common separators (hyphen, slash, underscore)
        tokens = [t for t in re.split(r'[\s\-_/]+', search_term) if t]
        base_q = (
            Q(user__username__icontains=search_term)
            | Q(user__first_name__icontains=search_term)
            | Q(user__last_name__icontains=search_term)
            | Q(phone__icontains=search_term)
            | Q(team__name__icontains=search_term)
            | Q(user_code__icontains=search_term)
            | Q(user__userauth__maindatabase__database_name__icontains=search_term)
            | Q(user__userauth__user_permission__name__icontains=search_term)
        )

        # detect explicit or partial status tokens (allow partial like 'inac' or 'act')
        status_value = None
        exact_status = {t.lower() for t in tokens if t.lower() in ('active', 'inactive')}
        if 'active' in exact_status and 'inactive' not in exact_status:
            status_value = True
        elif 'inactive' in exact_status and 'active' not in exact_status:
            status_value = False
        else:
            # allow partial/ prefix matches for status tokens (accept shorter prefixes)
            partial_hits = set()
            for t in tokens:
                lt = t.lower()
                # consider prefixes of length >= 2 to be helpful for users (e.g., 'ac' or 'inc')
                if len(lt) >= 2:
                    added = False
                    # prefer prefix matches to avoid accidental substring collisions
                    if 'active'.startswith(lt) and not 'inactive'.startswith(lt):
                        partial_hits.add('active')
                        added = True
                    if 'inactive'.startswith(lt) and not 'active'.startswith(lt):
                        partial_hits.add('inactive')
                        added = True
                    if not added:
                        # fallback to substring matching when prefix rules are ambiguous
                        hit = []
                        if 'active'.find(lt) != -1:
                            hit.append('active')
                        if 'inactive'.find(lt) != -1:
                            hit.append('inactive')
                        if len(hit) == 1:
                            partial_hits.add(hit[0])
            if 'active' in partial_hits and 'inactive' not in partial_hits:
                status_value = True
            elif 'inactive' in partial_hits and 'active' not in partial_hits:
                status_value = False

        applied_status_only = False

        # build tokenized name/group queries for multi-token searches
        if len(tokens) > 1:
            q_tokens = Q()
            for t in tokens:
                q_tokens &= (
                    Q(user__first_name__icontains=t) | Q(user__last_name__icontains=t)
                )
            # also try matching all tokens across group/team fields (e.g. "Group - Team")
            q_tokens_group = Q()
            for t in tokens:
                q_tokens_group &= (
                    Q(team__name__icontains=t) | Q(team__user_group__group_name__icontains=t)
                )

            # if a status token exists alongside other tokens, require status AND the other tokens
            if status_value is not None:
                q = (base_q | q_tokens | q_tokens_group) & Q(user__is_active=status_value)
            else:
                q = base_q | q_tokens | q_tokens_group
        else:
            # single-token search
            if status_value is not None:
                # if the search is just 'active' or 'inactive', filter by status only
                qs = qs.filter(user__is_active=status_value)
                applied_status_only = True
            else:
                q = base_q

        if not applied_status_only:
            qs = qs.filter(q).distinct()

    # annotate profile instances with permission and database_servers for use in serialization
    for profile in qs:
        auths = auth_map.get(profile.user_id, [])
        profile.permission = auths[0].user_permission.name if auths else None
        allowed_db_ids = {auth.maindatabase_id for auth in auths}
        if allowed_db_ids:
            profile.database_servers = [auth.maindatabase.database_name for auth in auths]
        else:
            profile.database_servers = None

    # paging parameters (DataTables style)
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    try:
        start = max(0, int(start))
    except Exception:
        start = 0
    try:
        length = max(1, min(1000, int(length)))
    except Exception:
        length = 25

    records_total = qs.count()
    page_qs = qs[start:start + length]

    serializer = UserProfileSerializer(page_qs, many=True).data
    # inject computed fields (permission, database_servers) into serialized data
    data = list(serializer)
    for i, profile in enumerate(page_qs):
        try:
            data[i]['permission'] = getattr(profile, 'permission', None)
            data[i]['database_servers'] = getattr(profile, 'database_servers', None)
        except Exception:
            pass
        

    return JsonResponse({
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_total,
        'data': data
    })


@login_required
@require_POST
def ApiChangeUserStatus(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user == request.user:
            return JsonResponse({'status': 'error', 'message': 'Cannot change your own status.'})
        user.is_active = not user.is_active
        user.save()
        status_msg = 'Active' if user.is_active else 'Inactive'
        return JsonResponse({'status': 'success', 'message': f'User is now {status_msg}.'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

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
            ).values_list('action'))
            
            if role.type in ['administrator', 'auditor', 'operator']:
                roles_permissions[role.type] = {
                    'id': role.id,
                    'permissions': active_actions
                }
            else:
                custom_roles.append({
                    'id': role.id,
                    'name': role.name,
                    'permissions': active_actions
                })

        return JsonResponse({
            'status': 'success',
            'all_permissions': all_perms_data,
            'base_roles': roles_permissions,
            'custom_roles': custom_roles
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def ApiGetUSerProfile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user == request.user:
            return JsonResponse({'status': 'error', 'message': 'Cannot change your own status.'})

        user_to_edit = user
        user_profile = UserProfile.objects.filter(user=user_to_edit).first()

        user_auths = UserAuth.objects.filter(user=user_to_edit)
        selected_db_ids = [str(auth.maindatabase.id) for auth in user_auths if getattr(auth, 'allow', False)]
        
        main_db_qs = MainDatabase.objects.all()
        main_db = [
            {
                'id': d.id,
                'database_name': getattr(d, 'database_name', None),
                'status': getattr(d, 'status', None)
            }
            for d in main_db_qs
        ]

        all_db_selected = len(selected_db_ids) == len(main_db) and len(main_db) > 0

        user_permission = None
        if user_auths.exists() and user_auths.first().user_permission:
            user_permission = user_auths.first().user_permission

        selected_role_id = None
        selected_role_type = None
        if user_permission:
            if user_permission.type in ['administrator', 'auditor', 'operator']:
                selected_role_type = user_permission.type
            else:
                selected_role_id = str(user_permission.id)

        profile_data = UserProfileSerializer(user_profile).data if user_profile else None

        return JsonResponse({
            'status': 'success',
            'user_profile': profile_data,
            'selected_db_id': selected_db_ids,
            'all_db_selected': all_db_selected,
            'selected_role_id': selected_role_id,
            'selected_role_type': selected_role_type,
        })
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'})
        

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
        create_user_log(user=request.user, action="Change User Status", detail=f"message : User not found", status="error", request=request)
        return JsonResponse({'status': 'error', 'message': 'User not found.'})
    except Exception as e:
        create_user_log(user=request.user, action="Change User Status", detail=f"message : {str(e)}", status="error", request=request)
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
