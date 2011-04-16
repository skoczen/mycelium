from django.contrib.auth.models import User

class AccountAuthBackend(object):
    """
    Account Authentication Backend
    
    Authenticate against the user table, using Account.namespaced_username_for_username for the username
    """

    def authenticate(self, request=None, username=None, password=None):
        print "authenticating"
        print username
        try:
            assert request != None
            # """ If we want to support email login:"""
            # user = User.objects.get(email=username)
            # if user.check_password(password):
            #     return user
            user = User.objects.get(username=request.account.namespaced_username_for_username(username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None 

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

