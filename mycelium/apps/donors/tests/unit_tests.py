from test_factory import Factory
from nose.tools import istest
import datetime
from donors.models import Donation

@istest
def test_donations_by_year_returns_sanely():
    person = Factory.person()
    today = datetime.date.today()
    
    
    d1 = Donation.objects.create(donor=person.donor, amount=5, date=today)
    d2 = Donation.objects.create(donor=person.donor, amount=41, date=datetime.datetime.now()-datetime.timedelta(days=1))

    target = [{'donations': [d1, d2],
          'total_donations': d1.amount+d2.amount,
          'total_number_of_donations':2,
          'year': today.year
    }]
    
    assert person.donor.donations_by_year == target

@istest
def test_donations_by_year_for_non_donors_returns_properly():
    person = Factory.person()
    target = []

    assert person.donor.donations_by_year == target