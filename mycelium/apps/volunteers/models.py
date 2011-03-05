from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from taggit.managers import TaggableManager
from people.models import Person
from django.db.models.signals import post_save
import datetime

VOLUNTEER_STATII = [
    ("active", "Active"),
    ("inactive", "Active"),
    ("temp_inactive", "Temporarily Inactive"),
]

class Volunteer(TimestampModelMixin):
    """A volunteer!"""
    person = models.OneToOneField(Person)
    status = models.CharField(max_length=50,default=VOLUNTEER_STATII[0])
    reactivation_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.person
    
    @property
    def completed_shifts(self):
        return self.completedshift_set.all()
    
    @classmethod
    def make_each_person_a_volunteer(cls, sender, instance, created=None, *args, **kwargs):
        if created:
            v = Volunteer.objects.get_or_create(person=instance)[0]
            v.save()
    
    @classmethod
    def make_volunteers_for_each_person(cls):
        [cls.make_each_person_a_volunteer(Person,p,True) for p in Person.objects.all()]


class Shift(TimestampModelMixin):
    """A future need for volunteers"""
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Shift Name")
    start_datetime = models.DateTimeField()
    duration = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    volunteers_needed = models.IntegerField(blank=True, null=True)
    # coordinator = models.ForeignKey(Staff, blank=True, null=True)

class ScheduledShift(TimestampModelMixin):
    """A volunteer, scheduled to work a shift"""
    volunteer = models.ForeignKey(Volunteer, related_name="volunteer_shifts")
    shift = models.ForeignKey(Shift, blank=True, null=True,)
    duration = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2, help_text="Length of shift, in hours")
    date = models.DateField(default=datetime.date.today,verbose_name="Shift date")

    # categories = TaggableManager()
    

class CompletedShift(TimestampModelMixin):
    """A work shift (possibly informal) completed by a volunteer"""
    volunteer = models.ForeignKey(Volunteer)
    shift = models.ForeignKey(Shift, blank=True, null=True,)
    scheduled_shift = models.ForeignKey(ScheduledShift, blank=True, null=True,)
    duration = models.DecimalField(default=2, max_digits=6, decimal_places=2, help_text="Length of shift, in hours")
    date = models.DateField(default=datetime.date.today,verbose_name="Shift date")
    
    categories = TaggableManager()

    def __unicode__(self):
        "%s worked on %s %s for %s hours" % (self.volunteer, self.shift, self.date, self.duration)

    class Meta:
        ordering = ["-date"]

post_save.connect(Volunteer.make_each_person_a_volunteer,sender=Person)