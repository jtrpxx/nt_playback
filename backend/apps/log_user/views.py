from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta

from apps.core.model.authorize.models import UserLog
from apps.core.utils.permissions import get_user_actions

def ApiGetUserLogs(request,type):
    try:
        type = str(type)
    except (ValueError, TypeError):
        return JsonResponse({'status': False, 'message': 'Invalid type'}, status=400)

    # permission check depending on log type
    required_action = 'System Logs' if type == 'system' else ('Audit Logs' if type == 'audit' else 'User Logs')
    user_actions = get_user_actions(request.user)
    if required_action not in user_actions:
        return JsonResponse({'detail': 'Access Denied'}, status=403)
    
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 25))
    search_value = request.GET.get("search[value]", "").strip()
    
    # log_list = Viewlog.objects.all()
    # ฟิลเตอร์จาก request.form หรือ request.GET
    name = request.POST.get("name") or request.GET.get("name")
    username = request.POST.get("username") or request.GET.get("username")  
    full_name = request.POST.get("full_name") or request.GET.get("full_name")
    action = request.POST.get("action") or request.GET.get("action")
    status = request.POST.get("status") or request.GET.get("status")
    description = request.POST.get("detail") or request.GET.get("detail") 
    ip_address = request.POST.get("ip_address") or request.GET.get("ip_address")
    start_date = request.POST.get("start_date") or request.GET.get("start_date")
    end_date = request.POST.get("end_date") or request.GET.get("end_date")
    client_type = request.POST.get("client_type") or request.GET.get("client_type")
    
    # base queryset and type filter
    # avoid N+1 queries on user access by selecting related user
    log_list = UserLog.objects.select_related('user').all()

    if type == 'system':
        log_list = log_list.filter(status='error')
    elif type == 'audit':
        log_list = log_list.filter(status='success')

    # total before applying filters (for DataTables recordsTotal)
    records_total = log_list.count()

    # apply explicit filters from form
    if name:
        # allow comma-separated list of usernames from frontend (e.g. "snadmin,wisitp")
        try:
            names = [n.strip() for n in str(name).split(',') if n.strip()]
            if len(names) > 1:
                log_list = log_list.filter(user__username__in=names)
            else:
                log_list = log_list.filter(user__username=names[0])
        except Exception:
            log_list = log_list.filter(user__username=name)
    if username:
        log_list = log_list.filter(user__username__icontains=username)
    if full_name:
        log_list = log_list.filter(Q(user__first_name__icontains=full_name) | Q(user__last_name__icontains=full_name))    
    if action:
        # allow comma-separated list of actions (e.g. "Login,Play audio")
        try:
            acts = [a.strip() for a in str(action).split(',') if a.strip()]
            if len(acts) > 1:
                log_list = log_list.filter(action__in=acts)
            else:
                log_list = log_list.filter(action__icontains=acts[0])
        except Exception:
            log_list = log_list.filter(action__icontains=action)
    if status:
        log_list = log_list.filter(status__icontains=status)
    if description:
        log_list = log_list.filter(detail__icontains=description)
    if ip_address:
        log_list = log_list.filter(ip_address__icontains=ip_address)
    if start_date:
        try:
            dt = parse_datetime(start_date)
            if dt is None:
                dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
            if settings.USE_TZ and dt.tzinfo is None:
                dt = timezone.make_aware(dt, timezone.get_current_timezone())
            log_list = log_list.filter(timestamp__gte=dt)
        except Exception:
            pass
    if end_date:
        try:
            dt = parse_datetime(end_date)
            if dt is None:
                dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
            if settings.USE_TZ and dt.tzinfo is None:
                dt = timezone.make_aware(dt, timezone.get_current_timezone())
            # include the full minute of the provided end time (up to :59)
            dt_end = dt + timedelta(seconds=59)
            log_list = log_list.filter(timestamp__lte=dt_end)
        except Exception:
            pass
    if client_type:
        log_list = log_list.filter(client_type__icontains=client_type)

    # support comma-separated search terms across multiple columns
    if search_value:
        tokens = [t.strip() for t in search_value.split(',') if t.strip()]
        if tokens:
            q_search = Q()
            for tok in tokens:
                q_tok = (Q(user__username__icontains=tok) |
                         Q(user__first_name__icontains=tok) |
                         Q(user__last_name__icontains=tok) |
                         Q(action__icontains=tok) |
                         Q(detail__icontains=tok) |
                         Q(ip_address__icontains=tok) |
                         Q(client_type__icontains=tok))
                q_search &= q_tok
            log_list = log_list.filter(q_search)

    # records after filtering
    records_filtered = log_list.count()

    # Pagination (select_related already applied)
    log_page = log_list[start:start + length]

    data = []
    for idx, log in enumerate(log_page, start=start+1):
        data.append({
            "no": idx,
            "username": str(log.user) if log.user else "-",
            "full_name": f"{log.user.first_name} {log.user.last_name}" if log.user else "-",
            "action": str(log.action) if log.action else "-",
            "status": str(log.status) if log.status else "-",
            "detail": str(log.detail) if log.detail else "-",
            "ip_address": str(log.ip_address) if log.ip_address else "-",
            "detail": str(log.detail) if log.detail else "-",
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M") if log.timestamp else "-",
            "client_type": str(log.client_type) if log.client_type else "-",
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })
