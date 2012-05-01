
# Based on ideas from https://github.com/tkaemming/django-subdomains
from django.conf import settings
from subdomains.middleware import SubdomainURLRoutingMiddleware
from accounts.models import Account, UserAccount
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class AccountAuthMiddleware(SubdomainURLRoutingMiddleware):

    def redirect_to_public_home(self,request):
        from django.contrib.sites.models import Site
        site = Site.objects.get(pk=settings.SITE_ID)
        # Yes, having this if in the middleware is ridiculous. But, it's fast, and should only fail on edges.
        if settings.SELENIUM_TESTING:
            return HttpResponseRedirect("%s%s:settings.LIVE_SERVER_PORT" % (request.protocol, site.domain, settings.LIVE_SERVER_PORT))
        else:
            return HttpResponseRedirect("%s%s" % (request.protocol, site.domain))
        
            

    def process_request(self, request, *args, **kwargs):
        super(AccountAuthMiddleware,self).process_request(request, *args, **kwargs)
        
        if request.is_secure():
            request.protocol = "https://"
        else:
            request.protocol = "http://"
        

        subdomain = getattr(request, 'subdomain', False)
        # print subdomain
        if subdomain is not False:

            # get the account
            poss_account = Account.objects.filter(subdomain=request.subdomain)
            # print poss_account

            if poss_account.count() == 1:
                request.account = poss_account[0]
            else:
                # if we don't have an account, and this isn't a public site (or in dev mode, serving media), bail. 
                if not request.subdomain in settings.PUBLIC_SUBDOMAINS and not (settings.ENV == "DEV" and request.path[:len(settings.MEDIA_URL)] == settings.MEDIA_URL):
                    return self.redirect_to_public_home(request)

            user = request.user


            if not request.subdomain in settings.PUBLIC_SUBDOMAINS:
                try:
                    # print user
                    # print request.account
                    # try get the useraccount
                    request.useraccount = UserAccount.objects.get(user=user, account=request.account)
                    # print request.useraccount

                except:
                    #  from qi_toolkit.helpers import print_exception
                    #  print_exception()

                    # if we're not logging in right now (or in dev mode, serving media), bail. 
                    # print reverse("accounts:login")
                    # print request.path
                    # print reverse("accounts:login") != request.path 
                    if reverse("accounts:login") != request.path and not (settings.ENV == "DEV" and request.path[:len(settings.MEDIA_URL)] == settings.MEDIA_URL):
                        # redirect to login page
                        if request.path != reverse("accounts:login") and request.path != "/":
                            return HttpResponseRedirect("%s?next=%s" % (reverse("accounts:login"),request.path))
                        else:
                            return HttpResponseRedirect(reverse("accounts:login"))
                    # print "skipped"
        else:
            
            # if there's no subdomain, but tis wasn't handled by the SubdomainURLRoutingMiddleware, something weird is happening. Bail.
            if not request.subdomain in settings.PUBLIC_SUBDOMAINS:
                self.redirect_to_public_home(request)

        # print "exiting safely"
        return None