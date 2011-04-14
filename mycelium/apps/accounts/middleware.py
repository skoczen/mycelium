# Based on ideas from https://github.com/tkaemming/django-subdomains
from django.conf import settings
from subdomains.middleware import SubdomainURLRoutingMiddleware
from accounts.models import Account, UserAccount


class AccountAuthMiddleware(SubdomainURLRoutingMiddleware):
    def process_request(self, request):

        subdomain = getattr(request, 'subdomain', False)
            
        if subdomain is not False:
            # get the account
            poss_account = Account.objects.filter(subdomain=request.subdomain)
            if poss_account.count() == 1:
                request.account = poss_account[0]
            else:
                if not request.subdomain in settings.PUBLIC_SUBDOMAINS:
                    print "redirect to subdomain's login page"

            # if it's not in a public site
            if not request.subdomain in settings.PUBLIC_SUBDOMAINS:
                # get the user
                user = request.user
                try:
                    request.useraccount = UserAccount.objects.get(user=user, account=request.account)
                except:
                    # redirect to login page
                    print "redirect to subdomain's login page"
                    pass
