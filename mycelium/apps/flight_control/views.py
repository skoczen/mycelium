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






@staff_member_required
@render_to("flight_control/home.html")
def home(request):
    
    problem_accounts = Account.objects.billing_problem.all()
    active_account_count = Account.objects.active.count()
    
    week_1 = Account.objects.week_1.count()
    week_2 = Account.objects.week_2.count()
    week_3 = Account.objects.week_3.count()
    week_4 = Account.objects.week_4.all()

    avg_users = float(UserAccount.objects.count()) / active_account_count
    avg_people = Person.objects.count() / active_account_count
    avg_organizations = Organization.objects.count() / active_account_count
    avg_donations = Donation.objects.count() / active_account_count
    avg_donation = Donation.objects.all().aggregate(Sum('amount'))["amount__sum"] / Donation.objects.count()
    avg_volunteer_hours = CompletedShift.objects.all().aggregate(Sum('duration'))["duration__sum"] / active_account_count
    avg_vol_hours_per_person = CompletedShift.objects.all().aggregate(Sum('duration'))["duration__sum"] / Person.objects.count()
    avg_tags = Tag.objects.count() / active_account_count
    avg_tags_per_person = TaggedItem.objects.count() / Person.objects.count()
    avg_groups = Group.objects.count() / active_account_count
    avg_spreadsheets = Spreadsheet.objects.count() / active_account_count

    return locals()

@staff_member_required
@render_to("flight_control/account.html")
def account(request, account_id):
    account = Account.objects.get(pk=account_id)
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
