from test_factory import Factory
from nose.tools import istest
import datetime

# @istest
# def test_completed_shifts_by_year_returns_sanely():
#     person = Factory.person()
#     today = datetime.date.today()
    
    
#     s1 = CompletedShift.raw_objects.create(account=account, volunteer=person.volunteer, duration=5, date=today)
#     s2 = CompletedShift.raw_objects.create(account=account, volunteer=person.volunteer, duration=1, date=today)

#     target = [{'shifts': [s2, s1],
#           'total_hours': s1.duration+s2.duration,
#           'total_shifts': 2,
#           'year': today.year
#     }]
    
#     assert person.volunteer.completed_shifts_by_year == target
