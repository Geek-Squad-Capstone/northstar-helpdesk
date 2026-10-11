from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

def user_has_role(user, allowed_roles):
    """
    Check if the user's role is one of the allowed roles.

    Args:
        user: The user object to check.
        allowed_roles: A list of roles that are allowed.

    Returns:
        bool: True if the user’s role is one of the allowed roles, False otherwise.
    """
    if not user:
        return False

    if not user.is_authenticated:
        return False

    user_profile = getattr(user, 'profile', None)
    if not user_profile:
        return False

    user_role = user_profile.role

    return user_role in allowed_roles

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            if not user_has_role(request.user, allowed_roles):
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
