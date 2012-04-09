# This app has no models, or publicly accessible views.
# It's used for common tasks like field saving, template tags, etc
"""
General-purpose tasks that are not tied to a given app.

Right now this is mostly to hook celery into johnny-cache, so our app server
and celery are on the same page as far as cache invalidation goes. Celery does
not have any notion of middleware, so we have to fake it with 
"""
# from johnny.cache import get_backend, local
# from celery.signals import task_prerun, task_postrun, task_failure
# # from johnny.middleware import QueryCacheMiddleware, LocalStoreClearMiddleware

# def task_prerun_handler(*args, **kwargs):
#     """
#     Before each Task is ran, we have to instantiate Johnny's query cache
#     monkey patch. This will make sure that any table writes invalidate table
#     caches, and reads pull from any existing caches.
#     """
#     get_backend().patch()
# task_prerun.connect(task_prerun_handler)

# def task_postrun_handler(*args, **kwargs):
#     """
#     After each task is ran, the LocalStore cache (similar to threadlocals) is
#     cleared, as is the case with views (instead of celery tasks).
#     """
#     local.clear()

# task_postrun.connect(task_postrun_handler)
# # Also have to cleanup on failure.
# task_failure.connect(task_postrun_handler)
