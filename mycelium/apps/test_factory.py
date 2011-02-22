from qi_toolkit.factory import QiFactory
from people.models import Person, Organization, Employee

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
    def report(cls):
        o = DummyObj()
        o.pk = 1
        return o

    @classmethod
    def data_import(cls):
        o = DummyObj()
        o.pk = 1
        return o