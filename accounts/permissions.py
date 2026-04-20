from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from .models import User


VIEW_ROLES = {User.Roles.VIEWER, User.Roles.COORDINATOR, User.Roles.ADMIN}
COORDINATOR_ROLES = {User.Roles.COORDINATOR, User.Roles.ADMIN}
ADMIN_ROLES = {User.Roles.ADMIN}


def get_user_role(user):
    if not getattr(user, "is_authenticated", False):
        return None
    if getattr(user, "is_superuser", False):
        return User.Roles.ADMIN
    return getattr(user, "role", None)


def has_any_role(user, allowed_roles):
    if not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_superuser", False):
        return True
    return get_user_role(user) in set(allowed_roles)


def can_view_app(user):
    return has_any_role(user, VIEW_ROLES)


def can_manage_facilities(user):
    return has_any_role(user, COORDINATOR_ROLES)


def can_delete_facilities(user):
    return has_any_role(user, ADMIN_ROLES)


def can_manage_user_access(user):
    return has_any_role(user, ADMIN_ROLES)


def build_permission_flags(user):
    return {
        "can_view_app": can_view_app(user),
        "can_manage_facilities": can_manage_facilities(user),
        "can_delete_facilities": can_delete_facilities(user),
        "can_manage_user_access": can_manage_user_access(user),
        "is_viewer": has_any_role(user, {User.Roles.VIEWER}),
        "is_coordinator": has_any_role(user, {User.Roles.COORDINATOR}),
        "is_admin": has_any_role(user, ADMIN_ROLES),
        "role": get_user_role(user),
    }


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = set()
    raise_exception = True

    def test_func(self):
        return has_any_role(self.request.user, self.allowed_roles)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name(),
            )
        raise PermissionDenied(self.get_permission_denied_message())


class ViewerRequiredMixin(RoleRequiredMixin):
    allowed_roles = VIEW_ROLES


class CoordinatorRequiredMixin(RoleRequiredMixin):
    allowed_roles = COORDINATOR_ROLES


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ADMIN_ROLES
