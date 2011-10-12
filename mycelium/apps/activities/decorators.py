from functools import wraps
from activities.tasks import save_action

def action(account, action_type, **action_kwargs):
    def feature_level_access(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            ret = function(request, *args, **kwargs)
            save_action.delay(account, action_type, **action_kwargs)
            return ret
        return wrapper
    return feature_level_access


