# apps/home/views.py
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction, DatabaseError,IntegrityError
from django.contrib import messages
# from apps.core.utils.function import create_user_log

# models
from apps.core.model.authorize.models import MainDatabase,UserAuth,UserProfile,Department,MainDatabase,UserGroup,UserTeam,UserLog


from apps.configuration.models import UserPermission,UserPermissionDetail

#serializer
from apps.core.model.authorize.serializers import UserProfileSerializer,DepartmentSerializer,UserGroupSerializer,UserTeamSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

@login_required(login_url='/login')
def ApiIndexUserManagement(request):
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

    # annotate profile instances with permission and database_servers for use in serialization
    for profile in qs:
        auths = auth_map.get(profile.user_id, [])
        profile.permission = auths[0].user_permission.name if auths else None
        allowed_db_ids = {auth.maindatabase_id for auth in auths}
        if allowed_db_ids == main_db_ids and allowed_db_ids:
            profile.database_servers = "ALL"
        elif allowed_db_ids:
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

    
    