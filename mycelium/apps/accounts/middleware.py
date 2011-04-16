# Based on ideas from https://github.com/tkaemming/django-subdomains
from django.conf import settings
from subdomains.middleware import SubdomainURLRoutingMiddleware
from accounts.models import Account, UserAccount
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class AccountAuthMiddleware(SubdomainURLRoutingMiddleware):
    def process_request(self, request, *args, **kwargs):
        super(AccountAuthMiddleware,self).process_request(request, *args, **kwargs)

        subdomain = getattr(request, 'subdomain', False)
        
        if subdomain is not False:
            # get the account
            poss_account = Account.objects.filter(subdomain=request.subdomain)
            if poss_account.count() == 1:
                request.account = poss_account[0]
            else:
                if not request.subdomain in settings.PUBLIC_SUBDOMAINS and (reverse("accounts:login") != request.path and not (settings.ENV == "DEV" and request.path[:len(settings.MEDIA_URL)] == settings.MEDIA_URL)):
                    return HttpResponseRedirect(reverse("accounts:login"))

            # if it's not in a public site
            if not request.subdomain in settings.PUBLIC_SUBDOMAINS:
                # get the user
                user = request.user
                try:
                    request.useraccount = UserAccount.objects.get(user=user, account=request.account)
                except:
                    if reverse("accounts:login") != request.path and not (settings.ENV == "DEV" and request.path[:len(settings.MEDIA_URL)] == settings.MEDIA_URL):
                        # redirect to login page
                        return HttpResponseRedirect(reverse("accounts:login"))
        else:
            if not request.subdomain in settings.PUBLIC_SUBDOMAINS:
                from django.contrib.sites.models import Site
                site = Site.objects.get(pk=settings.SITE_ID)
                if request.is_secure:
                    protocol = "https://"
                else:
                    protocol = "http://"
                return HttpResponseRedirect("%s%s" % (protocol, site.domain))
                    