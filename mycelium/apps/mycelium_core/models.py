from django.db import models
from qi_toolkit.models import SimpleSearchableModel
from mycelium_core.tasks import update_proxy_results_db_cache, put_in_cache_forever
import re

class SearchableItemProxy(SimpleSearchableModel):
    # models = []
    search_group_name = models.CharField(max_length=255)
    sorting_name = models.CharField(max_length=255, blank=True, null=True)
    search_string = models.TextField(blank=True, null=True)
    cached_search_result = models.TextField(blank=True, null=True)

    @property
    def cache_name(self):
        # Define this on subclassing.
        return "%s-%s" % (self.search_group_name, self.pk)
    
    def generate_search_string(self):
        # Define this on subclassing.
        return "%s" % (self.pk)

    def get_sorting_name(self):
        # Define this on subclassing.
        return "%s" % (self.pk)
        
    def __unicode__(self):
        return self.generate_search_string()

    class Meta(object):
        # abstract = True
        ordering = ["sorting_name","-id"]

    @property
    def child_proxy(self):
        try:
            return self.peopleandorganizationssearchproxy_set.get()
        except:
            return self.groupproxy_set.get()
    
    @property
    def obj(self):
        return self.child_proxy.obj
    
    @property
    def search_result_row(self):
        return self.child_proxy.search_result_row

    # overridden to trust accounts
    @classmethod
    def search(cls, account, query, delimiter=" ", ignorable_chars=None):
        # Accept a list of ignorable characters to strip from the query (dashes in phone numbers, etc)
        if ignorable_chars:
            ignorable_re = re.compile("[%s]+"%("".join(ignorable_chars)))
            query = ignorable_re.sub('',query)
        
        # Split the querystring by a given delimiter.
        if delimiter and delimiter != "":
            queries = query.split(delimiter)
        else:
            queries = [query]
        
        results = cls.objects_by_account(account).all()
        for q in queries:
            if q != "":
                results = results.filter(qi_simple_searchable_search_field__icontains=q)

        return results


    def save(self,*args,**kwargs):
        self.search_string = self.generate_search_string()
        self.sorting_name = self.get_sorting_name()
        ss = self.render_result_row()
        self.cached_search_result = ss
        super(SearchableItemProxy,self).save(*args,**kwargs)
        put_in_cache_forever(self.cache_name, ss)
