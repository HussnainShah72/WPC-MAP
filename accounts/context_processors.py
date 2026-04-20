from .permissions import build_permission_flags


def app_permissions(request):
    return {
        "app_perms": build_permission_flags(request.user),
    }
