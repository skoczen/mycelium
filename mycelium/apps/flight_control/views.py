from accounts.managers import get_or_404_by_account
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.db.models import Sum, Count, Avg

from accounts.models import Account
from accounts import BILLING_PROBLEM_STATII
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
@render_to("flight_control/home.html")
def home(request):
    problem_accounts = Account.objects.billing_problem.all()
    active_account_count = Account.objects.active.count()
    
    week_1 = Account.objects.week_1.count()
    week_2 = Account.objects.week_2.count()
    week_3 = Account.objects.week_3.count()
    week_4 = Account.objects.week_4.count()
    return locals()

@staff_member_required
@render_to("flight_control/account.html")
def account(request, account_id):
    account = Account.objects.get(pk=account_id)
    # recent_activity = Activity.objects.all()[:10]
    recent_activity = []
    
    return locals()

@staff_member_required
@json_view
def search_results(request):
    pass