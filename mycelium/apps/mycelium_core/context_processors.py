from django.conf import settings
def cdn_media_url(request):
    """ Returns CDN_MEDIA_URL url to context."""
    return { 'CDN_MEDIA_URL': settings.CDN_MEDIA_URL, }

def manual_media_url(request):
    """ Returns MANUAL_MEDIA_URL url to context."""
    return { 'MANUAL_MEDIA_URL': settings.MANUAL_MEDIA_URL, }


