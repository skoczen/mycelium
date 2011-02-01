from qi_toolkit.factory import QiFactory
from people.models import Person, EmailAddress, PhoneNumber, Address, ContactMethodType

class DummyObj(object):
    pass

class Factory(QiFactory):
    def email(cls, person=None):
        if not person:
            person = cls.person()
        email = EmailAddress.objects.create(person=person, email="%s@%s.com" % (cls.rand_str(), cls.rand_str()), primary=cls.rand_bool())
        return email

    def phone(cls, person=None):
        if not person:
            person = cls.person()
        phone = PhoneNumber.objects.create(person=person, phone_number="%s-%s-%s" % (cls.rand_int(100,999), cls.rand_int(100,999),cls.rand_int(1000,9999)), primary=cls.rand_bool())
        return phone

    def address(cls, person=None):
        if not person:
            person = cls.person()
        apt_str = ""
        if cls.rand_bool():
            apt_str = "Apt. %s" % (cls.rand_int(1,1000))
        address = Address.objects.create(
            person=person,
            line_1="%s %s %s" % (cls.rand_int(10,100), cls.rand_plant_name(), cls.rand_street_suffix()),
            line_2=apt_str,
            city=cls.rand_plant_name(),
            state=cls.rand_str(2).upper(),
            postal_code=cls.rand_int(10000,99999),
            primary=cls.rand_bool(),
            )
        return address

    def person(cls):
        person = Person.objects.create(first_name=cls.rand_name(), last_name=cls.rand_name())
        cls.address(person)
        cls.phone(person)
        cls.email(person)
        return person


    def report(cls):
        o = DummyObj()
        o.pk = 1
        return o

    def data_import(cls):
        o = DummyObj()
        o.pk = 1
        return o