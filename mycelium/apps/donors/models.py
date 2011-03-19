from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from django.db.models.signals import post_save
import datetime


from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from people.models import Person
from django.db.models.signals import post_save
import datetime
from taggit.managers import TaggableManager

class Donor(TimestampModelMixin):
    """A donor!"""
    person = models.OneToOneField(Person)

    tags = TaggableManager()

    def __unicode__(self):
        return "%s" % self.person

    class Meta(object):
        ordering = ["person"]

    @classmethod
    def make_each_person_a_donor(cls, sender, instance, created=None, *args, **kwargs):
        if created:
            d = Donor.objects.get_or_create(person=instance)[0]
            d.save()
    
    @property
    def alphabetical_tags(self):
        return self.tags.all().order_by("name")
    
    @classmethod
    def make_donors_for_each_person(cls):
        [cls.make_each_person_a_donor(Person,p,True) for p in Person.objects.all()]

    @property
    def donations(self):
        return self.donation_set.all()

    @property
    def donations_by_year(self):
        donations_by_year = []
        current_year = 0
        cur_year_dict = {}
        donations_this_year = 0
        number_of_donations_this_year = 0
        for donation in self.donations:
            if donation.date.year != current_year:
                if cur_year_dict != {}:
                    cur_year_dict['total_donations'] = donations_this_year
                    cur_year_dict["total_number_of_donations"] = number_of_donations_this_year
                    donations_by_year.append(cur_year_dict)

                current_year = donation.date.year
                donations_this_year = 0
                number_of_donations_this_year = 0
                    
                cur_year_dict = {
                    'year':donation.date.year,
                    'donations':[],
                }

            cur_year_dict["donations"].append(donation)
            number_of_donations_this_year += 1
            donations_this_year += donation.amount
        
        if cur_year_dict != {}:
            cur_year_dict['total_donations'] = donations_this_year
            cur_year_dict["total_number_of_donations"] = number_of_donations_this_year            
            donations_by_year.append(cur_year_dict)
        return donations_by_year


class Donation(TimestampModelMixin):
    """A specific donation"""
    donor = models.ForeignKey(Donor)
    date = models.DateField(default=datetime.date.today)
    currency = models.CharField(default="USD", max_length=255)
    amount = models.DecimalField(blank=True, null=True, max_digits=18, decimal_places=2)

    def __unicode__(self):
        return "%s on %s by %s" % (self.pretty_amount, self.date, self.donor)

    class Meta(object):
        ordering = ["-date", "amount"]

    @property
    def pretty_amount(self):
    	return "$%s" % self.amount


# class RecurringDonation(TimestampModelMixin):
#     """A volunteer, scheduled to work a shift"""
#     volunteer = models.ForeignKey(Volunteer, related_name="volunteer_shifts")
#     shift = models.ForeignKey(Shift, blank=True, null=True,)
#     duration = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2, help_text="Length of shift, in hours")
#     date = models.DateField(default=datetime.date.today,verbose_name="Shift date")

#     # categories = TaggableManager()
    
post_save.connect(Donor.make_each_person_a_donor,sender=Person)