from django.conf.urls.defaults import *
from django.conf import settings
from accounts.forms import AccountAuthenticationForm
from accounts.views import mycelium as views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
   url(r'^login/$',                     views.login,              {'template_name': 'accounts/login.html', 
                                                                   'authentication_form':AccountAuthenticationForm,}     
                                                                                                                             , name="login"         ),
   url(r'^logged-out/$',                                'django.contrib.auth.views.logout',      {'template_name': 'accounts/logout.html'}    , name="logout"                    ),
   url(r'^accounts/manage-users$',                       views.manage_users                                                                   , name="manage_users"              ),
   url(r'^accounts/update-access$',                      views.save_account_access_info                                                       , name="save_account_access_info"  ),
   url(r'^accounts/new-account$',                        views.save_new_account                                                               , name="save_new_account"          ),
   url(r'^accounts/{ua_id:digits}/reset-password$',      views.reset_account_password                                                         , name="reset_account_password"    ),
   url(r'^accounts/{ua_id:digits}/delete-user$'   ,      views.delete_account                                                                 , name="delete_account"            ),
   url(r'^accounts/manage-account$',                     views.manage_account                                                                 , name="manage_account"            ),
   url(r'^accounts/save-account-info$',                  views.save_account_info                                                              , name="save_account_info"         ),
   url(r'^accounts/my-account$',                         views.my_account                                                                     , name="my_account"                ),
   url(r'^accounts/save-my-account-info$',               views.save_my_account_info                                                           , name="save_my_account_info"      ),
   url(r'^accounts/change-my-password$',                 views.change_my_password                                                             , name="change_my_password"        ),

   # Redirect to dashboard
    url(r'^$',                                           views.dashboard                                                                      , name="dashboard"              ),
)
