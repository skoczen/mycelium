from qi_toolkit.factory import QiFactory
from people.models import Person, Organization, Employee
from groups.models import Group, GroupRule
from django.conf import settings
from volunteers.models import CompletedShift
from donors.models import Donation
from rules.models import LeftSide, Operator, RightSideType
from generic_tags.models import Tag, TagSet
from accounts.models import Plan, Account, UserAccount, AccessLevel
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from volunteers import VOLUNTEER_STATII
import datetime

import sys, os
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class DummyObj(object):
    pass

class Factory(QiFactory):

    @classmethod
    def email(cls, name_hint=None):
        if not name_hint:
            name_hint = cls.rand_str()
        
        return "%s@%s" % (name_hint, cls.rand_domain())


    @classmethod
    def phone(cls):
        phone = "%s-%s-%s" % (cls.rand_int(100,999), cls.rand_int(100,999),cls.rand_int(1000,9999))
        return phone

    @classmethod
    def address(cls):
        apt_str = ""
        if cls.rand_bool():
            apt_str = "Apt. %s" % (cls.rand_int(1,1000))
        address = {
            "line_1": "%s %s %s" % (cls.rand_int(10,1000), cls.rand_plant_name(), cls.rand_street_suffix()),
            "line_2": apt_str,
            "city": cls.rand_plant_name(),
            "state": cls.rand_us_state(),
            "postal_code": cls.rand_int(10000,99999),
            "primary": cls.rand_bool(),
        }
        return address

    @classmethod
    def person(cls, account=None):
        if not account:
            print "No account specified when creating a person. Making one up."
            account = cls.account
        
        first_name = cls.rand_name()
        person = Person.raw_objects.create(account=account,
                                       first_name=first_name, 
                                       last_name=cls.rand_name(),
                                       email=cls.email(name_hint=first_name),
                                       phone_number=cls.phone(),
                )
        person.__dict__.update(cls.address())
        person.save()
        return person

    @classmethod
    def tagset(cls, account, name=None):
        if not name:
            name = cls.rand_str()
        return TagSet.raw_objects.get_or_create(account=account, name=name)[0]

    @classmethod
    def tag(cls, account, name=None, tagset=None):
        if not name:
            name = cls.rand_str()
        if not tagset:
            tagset = cls.tagset()

        return Tag.raw_objects.get_or_create(account=account, name=name, tagset=tagset)[0]    

    @classmethod
    def tag_person(cls, tag_name=None, tagset=None, person=None):
        tag = cls.tag(name=tag_name, tagset=tagset)
        if not person:
            person= cls.person()

        tag.add_tag_to_person(person)


    @classmethod
    def organization(cls, account):
        organization = Organization.raw_objects.create(account=account,
                                       name="%ss for %s" % (cls.rand_name(), cls.rand_name()), 
                                       twitter_username=cls.rand_str(),
                                       website=cls.rand_str(),                                       
                                       primary_phone_number=cls.phone(),
                )
        organization.__dict__.update(cls.address())
        return organization



    @classmethod
    def employee(cls, account):
        employee = Employee.raw_objects.create(account=account,
                                       first_name=cls.rand_name(), 
                                       last_name=cls.rand_name(),
                                       role=cls.rand_str(),
                                       email=cls.email(),
                                       phone_number=cls.phone(),
                )
        return employee

    @classmethod
    def volunteer_history(cls, account, person=None):
        if not person:
            person = cls.person()

        cur_date = datetime.datetime.now()
        for i in range(0,cls.rand_int(end=300)):
            cur_date = cur_date - datetime.timedelta(days=cls.rand_int(0,30))
            CompletedShift.raw_objects.create(
                                    account=account,
                                    volunteer=person.volunteer,
                                    duration=cls.rand_int(1,16),
                                    date=cur_date
            )
        return person
    
    @classmethod
    def completed_volunteer_shift(cls, person, date=None, duration=None):
        if not date:
            date = datetime.datetime.now() - datetime.timedelta(days=cls.rand_int(0,3000))
        
        if not duration:
            duration = cls.rand_int(1,16)

        return CompletedShift.raw_objects.create(account=person.account,
                                            volunteer=person.volunteer,
                                            duration=duration,
                                            date=date)

    @classmethod
    def donor_history(cls, person=None):
        if not person:
            person = cls.person()

        cur_date = datetime.datetime.now()
        for i in range(0,cls.rand_int(end=150)):
            cur_date = cur_date - datetime.timedelta(days=cls.rand_int(0,10))
            cls.donation(person, date=cur_date)

        return person

    @classmethod
    def donation(cls, person, date=None, amount=None):
        if not date:
            date = datetime.datetime.now() - datetime.timedelta(days=cls.rand_int(0,3000))
        
        if not amount:
            amount = cls.rand_currency()

        return Donation.raw_objects.create( account=person.account,
                                        donor=person.donor,
                                        amount=amount,
                                        date=date)
         
    @classmethod
    def report(cls):
        o = DummyObj()
        o.pk = 1
        return o

    @classmethod
    def data_import(cls):
        o = DummyObj()
        o.pk = 1
        return o

    @classmethod
    def group(cls, account, name=None, **kwargs):
        if not name:
            name = cls.rand_str()
        return Group.raw_objects.get_or_create(account=account, name=name, **kwargs)[0]

    @classmethod
    def grouprule(cls, account, left_side_str, operator_str, right_side_str, group=None, **kwargs):
        if not group:
            group = cls.group()

        left_side = LeftSide.objects(account).get(display_name__iexact=left_side_str)
        operator = Operator.objects(account).get(display_name__iexact=operator_str)
        right_side_type = left_side.first_right_side_type
        right_side_value = right_side_str

        return GroupRule.raw_objects.get_or_create(account=account,
                                               left_side=left_side,
                                               operator=operator,
                                               right_side_type=right_side_type,
                                               right_side_value=right_side_value,
                                               group=group,
                                               )[0]


    @classmethod
    def account(cls, name=None, subdomain=None, delete_existing=False):
        if not name:
            name = cls.rand_str()
        if not subdomain:
            subdomain = slugify(name)
        
        if not delete_existing:
            assert Account.objects.filter(name=name).count() == 0
        else:
            if Account.objects.filter(name=name).count() == 1:
                Account.objects.filter(name=name).delete()

        monthly_plan = Plan.objects.get(name="Monthly")
        return Account.objects.create(plan=monthly_plan, name=name, subdomain=subdomain)

    @classmethod
    def useraccount(cls, account=account, username=None, password=None, full_name=None, access_level=None):
        if not username:
            username = cls.rand_str()
        if not password:
            password = username
        if not account:
            account = account
        if not access_level:
            access_level = AccessLevel.objects.get(name__iexact="Staff")
        
        if not full_name:
            full_name = "%s %s" % (cls.rand_name(), cls.rand_name())
        
        return account.create_useraccount(username=username, password=password, full_name=full_name, access_level=access_level, email=cls.email(name_hint=full_name))

    @classmethod
    def create_demo_site(cls, organization_name, subdomain=None, delete_existing=False, quick=False):
        if quick:
            max_num_people = 20
            max_num_orgs = 2
            num_tags = 1
        else:
            max_num_people = 2000
            max_num_orgs = 200
            num_tags = 10

        site = Site.objects.get(pk=settings.SITE_ID)

        # Create account
        print "Starting creation of %s's site." % organization_name
        account = cls.account(name=organization_name, subdomain=subdomain, delete_existing=delete_existing)
        request = DummyObj()
        request.account = account

        print "Creating site at %s.%s." % (account.subdomain, site)
        print "Account created."

        admin_accesslevel = AccessLevel.objects.get(name__iexact="Admin")
        staff_accesslevel = AccessLevel.objects.get(name__iexact="Staff")
        volunteer_accesslevel = AccessLevel.objects.get(name__iexact="Volunteer")

        # create admin user (admin / admin)
        cls.useraccount(account=account, username="admin", password="admin", access_level=admin_accesslevel)

        # create staff user (staff / staff)
        cls.useraccount(account=account, username="staff", password="staff", access_level=staff_accesslevel)

        # create volunteer user ( volunteer / volunteer )
        cls.useraccount(account=account, username="volunteer", password="volunteer", access_level=volunteer_accesslevel)
        print "Users created."

        # create a bunch of reasonable tags, including the favorite color category
        gen_ts = cls.tagset(account, name="General")
        vol_ts = cls.tagset(account, name="Volunteer")
        don_ts = cls.tagset(account, name="Donor")
        color_ts = cls.tagset(account, name="Favorite Color")
        print "Tagsets created."

        # gen tagsname=
        cls.tag(account, tagset=gen_ts, name="Board of Directors")
        cls.tag(account, tagset=gen_ts, name="Advocate")
        cls.tag(account, tagset=gen_ts, name="Media Contact")
        cls.tag(account, tagset=gen_ts, name="Community Partner")

        # vol tags
        cls.tag(account, tagset=vol_ts, name="Monday")
        cls.tag(account, tagset=vol_ts, name="Tuesday")
        cls.tag(account, tagset=vol_ts, name="Wednesday")
        cls.tag(account, tagset=vol_ts, name="Thursday")
        cls.tag(account, tagset=vol_ts, name="Friday")
        cls.tag(account, tagset=vol_ts, name="Weekly")
        cls.tag(account, tagset=vol_ts, name="Monthly")
        cls.tag(account, tagset=vol_ts, name="Phone Skills")

        # don tags
        cls.tag(account, tagset=don_ts, name="Major Donor")
        cls.tag(account, tagset=don_ts, name="Potential Major Donor")
        cls.tag(account, tagset=don_ts, name="Fundraiser")
        cls.tag(account, tagset=don_ts, name="Monthly Donor")
        cls.tag(account, tagset=don_ts, name="Quarterly Donor")
        cls.tag(account, tagset=don_ts, name="Yearly Donor")

        # color tags
        cls.tag(account, tagset=color_ts, name="Red")
        cls.tag(account, tagset=color_ts, name="Orange")
        cls.tag(account, tagset=color_ts, name="Yellow")
        cls.tag(account, tagset=color_ts, name="Green")
        cls.tag(account, tagset=color_ts, name="Aquamarine")
        cls.tag(account, tagset=color_ts, name="Blue")
        cls.tag(account, tagset=color_ts, name="Violet")
        cls.tag(account, tagset=color_ts, name="Purple")
        cls.tag(account, tagset=color_ts, name="Black")
        cls.tag(account, tagset=color_ts, name="White")
        cls.tag(account, tagset=color_ts, name="Gray")
        print "Tags created."

        # create a bunch of people
        people_created = []
        num = cls.rand_int(2,max_num_people)
        print "Creating %s people" % num,
        for i in range(0, num):
            p = cls.person(account)
            people_created.append(p)
            sys.stdout.write("."),
        print "done."

        num = cls.rand_int(2,max_num_orgs)
        print "Creating %s organizations" % num,
        # create a few organizations, with people
        for i in range(0, num):
            cls.organization(account)
            sys.stdout.write("."),

        print "done."

        # give some of the people volunteer histories and statii
        print "Adding volunteer histories",
        for p in people_created:
            if cls.rand_bool():
                cls.volunteer_history(account, p)
                
            if cls.rand_bool():
                v = p.volunteer
                v.status = VOLUNTEER_STATII[1][0]
                v.save()
            
            sys.stdout.write("."),
        print "done."

        # give some of the people donation histories
        print "Adding donation histories",
        for p in people_created:
            if cls.rand_bool():
                cls.donor_history(p)
            
            sys.stdout.write("."),
        print "done."

        print "Adding tags",
        # give some of the people tags
        all_tags = [t for t in Tag.objects(request).all()]
        for p in people_created:
            for i in range(0,cls.rand_int(0,num_tags)):
                t = all_tags[cls.rand_int(0,len(all_tags)-1)]
                if t.tagset!=gen_ts or  (cls.rand_bool() and cls.rand_bool()):
                    t.add_tag_to_person(p)
            
            sys.stdout.write("."),
        
        print "done."        

        # create a few groups
        

        # Board of Directors
        group = cls.group(account, name="Board of Directors")
        cls.grouprule(account, "have a general tag that","contains","Board of Directors", group=group)
        print "Created Board of Directors group"

        # Active Volunteers
        group = cls.group(account, name="Active Volunteers")
        cls.grouprule(account, "volunteer status","is",VOLUNTEER_STATII[0][0], group=group)
        print "Created Active Volunteers group"

        # Warm color people
        group = cls.group(account, name="Warm Color People", rules_boolean=False)
        cls.grouprule(account, "have a Favorite Color tag that","contains","red", group=group)
        cls.grouprule(account, "have a Favorite Color tag that","contains","orange", group=group)
        cls.grouprule(account, "have a Favorite Color tag that","contains","yellow", group=group)
        print "Created Warm color people group"

        # Recurring donors
        group = cls.group(account, name="Recurring Donors", rules_boolean=False)
        cls.grouprule(account, "have a Donor tag that","is exactly","monthly donor", group=group)
        cls.grouprule(account, "have a Donor tag that","is exactly","quarterly donor", group=group)
        cls.grouprule(account, "have a Donor tag that","is exactly","yearly donor", group=group)
        print "Created Recurring donors group"

        # Volunteers this year
        today = datetime.date.today()
        group = cls.group(account, name="Volunteers this year")
        cls.grouprule(account, "last volunteer shift","is after",datetime.date(day=1,month=1,year=today.year), group=group)

        print "Setup complete."
        return account

