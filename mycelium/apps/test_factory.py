from qi_toolkit.factory import QiFactory
from people.models import Person, Organization, Employee
from groups.models import Group, GroupRule
from volunteers.models import CompletedShift
from donors.models import Donation
import datetime

class DummyObj(object):
    pass

class Factory(QiFactory):

    @classmethod
    def email(cls):
        return "%s@%s.com" % (cls.rand_str(), cls.rand_str())


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
            "state": cls.rand_str(2).upper(),
            "postal_code": cls.rand_int(10000,99999),
            "primary": cls.rand_bool(),
        }
        return address

    @classmethod
    def person(cls):
        person = Person.objects.create(first_name=cls.rand_name(), 
                                       last_name=cls.rand_name(),
                                       email=cls.email(),
                                       phone_number=cls.phone(),
                )
        person.__dict__.update(cls.address())
        return person

    @classmethod
    def organization(cls):
        organization = Organization.objects.create(name="%ss for %s" % (cls.rand_name(), cls.rand_name()), 
                                       email=cls.email(),
                                       twitter_username=cls.rand_str(),
                                       website=cls.rand_str(),                                       
                                       primary_phone_number=cls.phone(),
                )
        organization.__dict__.update(cls.address())
        return organization



    @classmethod
    def employee(cls):
        employee = Employee.objects.create(first_name=cls.rand_name(), 
                                       last_name=cls.rand_name(),
                                       role=cls.rand_str(),
                                       email=cls.email(),
                                       phone_number=cls.phone(),
                )
        return employee

    @classmethod
    def volunteer_history(cls, person=None):
        if not person:
            person = cls.person()

        cur_date = datetime.datetime.now()
        for i in range(0,cls.rand_int(end=300)):
            cur_date = cur_date - datetime.timedelta(days=cls.rand_int(0,30))
            CompletedShift.objects.create(volunteer=person.volunteer,
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

        return CompletedShift.objects.create(volunteer=person.volunteer,
                                            duration=duration,
                                            date=date)
         
    @classmethod
    def donation(cls, person, date=None, amount=None):
        if not date:
            date = datetime.datetime.now() - datetime.timedelta(days=cls.rand_int(0,3000))
        
        if not amount:
            amount = cls.rand_currency()

        return Donation.objects.create(donor=person.donor,
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
    def group(cls, name=None):
        if not name:
            name = cls.rand_str()
        return Group.objects.get_or_create(name=name)[0]
