from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
from django.http import JsonResponse
from apps.core.utils.permissions import get_user_actions, require_action
from django.contrib.auth.models import User
from apps.core.model.authorize.models import UserTicket,UserProfile,UserAuth

from apps.core.model.authorize.serializers import UserTicketSerializer

@login_required(login_url='/login')
@require_action('Add User')
def ApiGetUserTicket(request):
    qs = UserTicket.objects.exclude(user__id=1).select_related('user')

    user_auths = UserAuth.objects.filter(user_permission=4).select_related('user')

    auth_map = {}
    for auth in user_auths:
        auth_map.setdefault(auth.user_id, []).append(auth)

    search_term = (request.GET.get('search[value]') or request.GET.get('search') or '').strip()
    if search_term:
        tokens = [t for t in re.split(r'[\s\-_/]+', search_term) if t]
        base_q = (
            Q(user__username__icontains=search_term)
            | Q(user__first_name__icontains=search_term)
            | Q(user__last_name__icontains=search_term)
            | Q(phone__icontains=search_term)
            | Q(user__userauth__user_permission__name__icontains=search_term)
        )

        applied_status_only = False

        if len(tokens) > 1:
            q_tokens = Q()
            for t in tokens:
                q_tokens &= (
                    Q(user__first_name__icontains=t) | Q(user__last_name__icontains=t)
                )
        else:
            q = base_q

        if not applied_status_only:
            qs = qs.filter(q).distinct()

    sort_field = request.GET.get('sort[0][field]')
    sort_dir = request.GET.get('sort[0][dir]')

    if sort_field and sort_dir:
        sort_mapping = {
            'username': 'user__username',
            'full_name': ['user__first_name', 'user__last_name'],
            'role': 'user__userauth__user_permission__name',
            'phone': 'phone',
            'status': 'user__is_active'
        }
        
        if sort_field in sort_mapping:
            fields = sort_mapping[sort_field]
            if not isinstance(fields, list):
                fields = [fields]
            
            ordering = []
            for f in fields:
                ordering.append(f'-{f}' if sort_dir == 'desc' else f)
            qs = qs.order_by(*ordering)
            if sort_field == 'role':
                qs = qs.distinct()
    else:
        qs = qs.order_by('-user__date_joined')

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

    serializer = UserTicketSerializer(page_qs, many=True).data
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
