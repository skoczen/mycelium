from django.conf import settings
def cdn_media_url(request):
    """ Returns CDN_MEDIA_URL url to context."""
    return { 'CDN_MEDIA_URL': settings.CDN_MEDIA_URL, }
