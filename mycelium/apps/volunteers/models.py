from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from taggit.managers import TaggableManager
from people.models import Person
from django.db.models.signals import post_save

class Volunteer(TimestampModelMixin):
    person = models.OneToOneField(Person)

    def __unicode__(self):
        return "%s" % self.person
    
    @classmethod
    def make_each_person_a_volunteer(cls, sender, instance, created=None, *args, **kwargs):
        if created:
            v = Volunteer.objects.get_or_create(person=instance)[0]
            v.save()
    
    @classmethod
    def make_volunteers_for_each_person(cls):
        [cls.make_each_person_a_volunteer(Person,p,True) for p in Person.objects.all()]

class VolunteerShiftEvent(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Event Name")

class VolunteerShift(TimestampModelMixin):
    volunteer = models.ForeignKey(Volunteer, related_name="volunteer_shifts")
    time = models.DecimalField(blank=True, null=True, verbose_name="Length of Shift", max_digits=6, decimal_places=2)
    date = models.DateField()
    event = models.ForeignKey(VolunteerShiftEvent, blank=True, null=True, related_name="Event (optional)")
    categories = TaggableManager()



post_save.connect(Volunteer.make_each_person_a_volunteer,sender=Person)