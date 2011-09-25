from functools import wraps
from django.core.exceptions import PermissionDenied

def restricted_to(access_level_const):
    def feature_level_access(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            if not request.account.has_access_to_level(access_level_const):
                raise PermissionDenied
            return function(request, *args, **kwargs)
        return wrapper
    return feature_level_access
