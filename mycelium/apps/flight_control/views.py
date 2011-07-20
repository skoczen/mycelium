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
    active_account_denominator = 1
    if active_account_count > 1:
        active_account_denominator = active_account_count

    recent_users = User.objects.all().order_by("-last_login")[:5]
    
    week_1 = Account.objects.week_1.filter(is_demo=False).count()
    week_2 = Account.objects.week_2.filter(is_demo=False).count()
    week_3 = Account.objects.week_3.filter(is_demo=False).count()
    week_4 = Account.objects.week_4.filter(is_demo=False).all()

    total_people= Person.objects.filter(account__is_demo=False).count()

    total_people_denominator = total_people
    if total_people_denominator == 0:
        total_people_denominator = 1

    avg_users = float(UserAccount.objects.filter(account__is_demo=False).count()) / active_account_denominator
    avg_people = total_people / active_account_denominator
    avg_organizations = Organization.objects.filter(account__is_demo=False).count() / active_account_denominator

    total_donations_divisor = Donation.objects.filter(account__is_demo=False).count()
    if total_donations_divisor == 0:
        total_donations_divisor = 1
    total_donation_amount = Donation.objects.filter(account__is_demo=False).all().aggregate(Sum('amount'))["amount__sum"]
    if total_donation_amount == None:
        total_donation_amount = 0

    avg_donations = Donation.objects.filter(account__is_demo=False).count() / active_account_denominator
    if Donation.objects.filter(account__is_demo=False).count() == 0:
        avg_donation = 0
    else:
        avg_donation =  total_donation_amount / total_donations_divisor

    total_volunteer_hours = CompletedShift.objects.filter(account__is_demo=False).all().aggregate(Sum('duration'))["duration__sum"] or 0
    avg_volunteer_hours = float(total_volunteer_hours) / active_account_denominator
    avg_vol_hours_per_person = float(total_volunteer_hours) / total_people_denominator
    avg_tags = float(Tag.objects.filter(account__is_demo=False).count()) / active_account_denominator
    avg_tags_per_person = float(TaggedItem.objects.filter(account__is_demo=False).count()) / total_people_denominator
    avg_groups = float(Group.objects.filter(account__is_demo=False).count()) / active_account_denominator
    avg_spreadsheets = float(Spreadsheet.objects.filter(account__is_demo=False).count()) / active_account_denominator

    return locals()

@staff_member_required
@render_to("flight_control/account.html")
def account(request, account_id):
    account = Account.objects.get(pk=account_id)
    recent_users = account.useraccount_set.order_by("-user__last_login")[:5]
    
    # recent_activity = Activity.objects_by_account(account).all()[:10]
    recent_activity = []
    

    num_people = Person.objects_by_account(account).count()
    num_organizations = Organization.objects_by_account(account).count()
    num_donations = Donation.objects_by_account(account).count()
    avg_donation = 0
    if num_donations > 0:
        avg_donation = account.total_donation_sum / num_donations
    num_volunteer_hours = account.total_volunteer_hours
    avg_vol_hours_per_person = 0
    if account.total_volunteer_hours and num_people > 0:
        avg_vol_hours_per_person = float(account.total_volunteer_hours) / num_people
    num_tags = Tag.objects_by_account(account).count()
    avg_tags_per_person = 0
    if TaggedItem.objects_by_account(account).count() and num_people > 0:
        avg_tags_per_person = float(TaggedItem.objects_by_account(account).count()) / num_people
    
    num_groups = Group.objects_by_account(account).count() 
    num_spreadsheets = Spreadsheet.objects_by_account(account).count()

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
