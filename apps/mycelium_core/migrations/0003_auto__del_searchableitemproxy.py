# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'SearchableItemProxy'
        db.delete_table('mycelium_core_searchableitemproxy')


    def backwards(self, orm):
        
        # Adding model 'SearchableItemProxy'
        db.create_table('mycelium_core_searchableitemproxy', (
            ('cached_search_result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('qi_simple_searchable_search_field', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sorting_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('search_string', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('search_group_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mycelium_core', ['SearchableItemProxy'])


    models = {
        
    }

    complete_apps = ['mycelium_core']
