from accounts.managers import get_or_404_by_account
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg

from accounts.models import Account, UserAccount
from accounts import BILLING_PROBLEM_STATII
from people.models import Person
from organizations.models import Organization
from donors.models import Donation
from volunteers.models import CompletedShift
from generic_tags.models import Tag, TaggedItem
from groups.models import Group
from spreadsheets.models import Spreadsheet
from django.contrib.auth.models import User



@staff_member_required
@render_to("flight_control/home.html")
def home(request):
    
    problem_accounts = Account.objects.billing_problem.filter(is_demo=False).all()
    active_account_count = Account.objects.active.filter(is_demo=False).count() 
    
    recent_users = User.objects.all().order_by("-last_login")[:5]
    
    week_1 = Account.objects.week_1.count()
    week_2 = Account.objects.week_2.count()
    week_3 = Account.objects.week_3.count()
    week_4 = Account.objects.week_4.all()

    total_people = Account.all_non_demo_accounts_num_total_people
    total_people_denominator = Account.num_non_demo_accounts_num_total_people_denominator

    avg_users = Account.all_non_demo_accounts_average_num_users
    avg_people = Account.all_non_demo_accounts_average_num_people
    avg_organizations = Account.all_non_demo_accounts_average_num_organizations

    total_donations_divisor = Account.num_non_demo_accounts_num_total_donations_denominator
    total_donation_amount = Account.all_non_demo_accounts_total_donation_amount

    avg_donations = Account.all_non_demo_accounts_average_number_of_donations_per_account
    avg_donation = Account.all_non_demo_accounts_average_donation_amount

    total_volunteer_hours = Account.all_non_demo_accounts_total_volunteer_hours
    avg_volunteer_hours = Account.all_non_demo_accounts_average_volunteer_hours_per_account
    avg_vol_hours_per_person = Account.all_non_demo_accounts_average_volunteer_hours_per_person
    avg_tags = Account.all_non_demo_accounts_average_tags_per_account
    avg_tags_per_person = Account.all_non_demo_accounts_average_taggeditems_per_person
    avg_groups = Account.all_non_demo_accounts_average_groups_per_account
    avg_spreadsheets = Account.all_non_demo_accounts_average_spreadsheets_per_account

    account_stats = Account

    return locals()

@staff_member_required
@render_to("flight_control/account.html")
def account(request, account_id):
    account = Account.objects.get(pk=account_id)
    recent_users = account.useraccount_set.order_by("-user__last_login")[:5]
    
    # recent_activity = Activity.objects_by_account(account).all()[:10]
    recent_activity = []


    return locals()

@staff_member_required
@json_view
def search_results(request):
    search_results = Account.objects.all()[:6]
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            search_results = Account.search(q,ignorable_chars=["-","(",")"])[:6]

    return {"fragments":{"global_search_results":render_to_string("flight_control/_search_results.html", locals())}}
