from django.db import models
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from mycelium_core.models import SearchableItemProxy
from accounts.models import AccountBasedModel
from mycelium_core.tasks import update_proxy_results_db_cache, put_in_cache_forever
from django.core.cache import cache
from django.template.loader import render_to_string
from django.db.models.signals import post_save

from groups.models import Group
from people.models import Person
from spreadsheets import SPREADSHEET_TEMPLATE_CHOICES, NO_NAME_STRING_SPREADSHEET
from spreadsheets.spreadsheet import SPREADSHEET_SOURCE_TYPES
from spreadsheets.export_templates import SPREADSHEET_TEMPLATE_INSTANCES


class Spreadsheet(AccountBasedModel, SimpleSearchableModel, TimestampModelMixin):
    name                    = models.CharField(max_length=255, blank=True, null=True)
    group                   = models.ForeignKey(Group, blank=True, null=True)
    spreadsheet_template    = models.CharField(max_length=255, choices=SPREADSHEET_TEMPLATE_CHOICES, default=SPREADSHEET_TEMPLATE_CHOICES[0][0])
    default_filetype        = models.CharField(max_length=255, choices=SPREADSHEET_SOURCE_TYPES, default=SPREADSHEET_SOURCE_TYPES[0][0])

    def __unicode__(self):
        return "%s" % self.name

    search_fields = ["searchable_name",]

    @property
    def searchable_name(self):
        if self.name:
            return "%s" % self.full_name
        else:
            return ""

        

    class Meta(object):
        ordering = ("name",)

    @property
    def full_name(self):
        if self.name and self.name != "":
            return "%s" % (self.name,)
        else:
            return NO_NAME_STRING_SPREADSHEET
            

    @property
    def num_rows(self):
        return self.members.count()

    @property
    def num_people(self):
        return self.members.count()

    
    @property
    def people(self):
        if self.group:
            return self.group.members
        else:
            return Person.objects_by_account(self.account).all()
    
    @property
    def members(self):
        t = self.template_instance_class(self.account)
        if t.model == Person:
            if self.group:
                return self.group.members
            else:
                return Person.objects_by_account(self.account).all()
        else:
            if self.group:
                qs = self.group.members.filter()
            else:
                qs = Person.objects_by_account(self.account).all()
            filter_kwargs = {"%s__in" % t.person_field.replace(".","__") : [p.pk for p in qs]}
            return t.model.objects.filter(**filter_kwargs)

    @property
    def template_obj(self):
        obj = None
        for c in SPREADSHEET_TEMPLATE_CHOICES:
            if c[0] == self.spreadsheet_template:
                obj = c[1]
                break
        return obj
    
    @property
    def template_instance_class(self):
        return SPREADSHEET_TEMPLATE_INSTANCES[self.template_obj.template_type]
    
    @classmethod
    def spreadsheet_template_instance_class(self, template_type):
        return SPREADSHEET_TEMPLATE_INSTANCES[template_type]


class SpreadsheetSearchProxy(SearchableItemProxy):
    SEARCH_GROUP_NAME = "spreadsheets"
    spreadsheet = models.ForeignKey('spreadsheets.Spreadsheet', blank=True, null=True)

    @property
    def obj(self):
        return self.spreadsheet or None

    @property
    def type(self):
        if self.spreadsheet_id != None:
            return "spreadsheet"
        return None
    
    @property
    def obj_id(self):
        if self.spreadsheet_id:
            return self.spreadsheet_id            
        else:
            return None

    def get_sorting_name(self):
        sn = ""
        if self.spreadsheet_id:
            sn = self.spreadsheet.searchable_name
        if sn == NO_NAME_STRING_SPREADSHEET:
            sn = ""
        return sn
        
    @property
    def search_result_row(self):
        return self.render_result_row()

    def regenerate_and_cache_search_results(self):
        ss = self.render_result_row()
        # popping over to celery
        put_in_cache_forever.delay(self.cache_name,ss)
        update_proxy_results_db_cache.delay(SpreadsheetSearchProxy, self,ss)
        cache.set(self.cached_count_key, self.members.count())
        return ss

    @property
    def cache_name(self):
        return "%s-%s-%s" % (self.search_group_name, self.type, self.obj_id)

    def generate_search_string(self):
        return self.obj.qi_simple_searchable_search_field

    def render_result_row(self):
        if self.spreadsheet_id:
            return render_to_string("spreadsheets/_search_result_row_spreadsheet.html",{'obj':self.obj})
        else:
            return ""

    @property
    def cached_count_key(self):
        return "SPREADSHEETCOUNT-%s" % (self.id,)

    @classmethod
    def spreadsheet_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        proxy, nil = cls.raw_objects.get_or_create(account=instance.account, spreadsheet=instance, search_group_name=cls.SEARCH_GROUP_NAME)
        cache.delete(proxy.cache_name)
        proxy.save()

    @classmethod
    def related_spreadsheet_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        cls.spreadsheet_record_changed(sender, instance.spreadsheet, *args, **kwargs)

    @classmethod
    def populate_cache(cls):
        [cls.spreadsheet_record_changed(Spreadsheet,g) for g in Spreadsheet.raw_objects.all()]

    @classmethod
    def resave_all_spreadsheets(cls):
        from spreadsheets.models import Spreadsheet
        [s.save() for s in Spreadsheet.raw_objects.all()]


    class Meta(SearchableItemProxy.Meta):
        verbose_name_plural = "SpreadsheetSearchProxies"

    @classmethod
    def spreadsheet_results_may_have_changed(cls, sender, instance, created=None, *args, **kwargs):
        from spreadsheets.tasks import regnerate_all_rulespreadsheet_search_results_for_account
        regnerate_all_rulespreadsheet_search_results_for_account.delay(cls, instance.account)


post_save.connect(SpreadsheetSearchProxy.spreadsheet_record_changed,sender=Spreadsheet)
