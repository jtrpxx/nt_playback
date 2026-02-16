from functools import wraps
from django.http import JsonResponse
from apps.core.model.authorize.models import UserAuth
from apps.configuration.models import UserPermissionDetail


def get_user_actions(user):
    """Return a set of action strings where status=True for user's assigned permissions."""
    if not user or not user.is_authenticated:
        return set()

    # root user bypass: user with id == 1 has all permissions
    try:
        if getattr(user, 'id', None) == 1:
            all_actions = UserPermissionDetail.objects.filter(status=True).values_list('action', flat=True).distinct()
            return set(a for a in all_actions if a)
    except Exception:
        # fall back to normal path on any error
        pass

    qs = UserAuth.objects.filter(user=user, allow=True, user_permission__isnull=False).select_related('user_permission')
    actions = set()
    for ua in qs:
        details = UserPermissionDetail.objects.filter(user_permission=ua.user_permission, status=True).values_list('action', flat=True)
        for a in details:
            actions.add(a)
    return actions


def require_action(*action_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            # Require authentication first
            if not request.user.is_authenticated:
                return JsonResponse({'detail': 'Authentication required'}, status=401)

            # root user bypass
            try:
                if getattr(request.user, 'id', None) == 1:
                    return view_func(request, *args, **kwargs)
            except Exception:
                pass

            # Check action permission
            if action_name not in get_user_actions(request.user):
                return JsonResponse({'detail': 'Access Denied'}, status=403)

            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
