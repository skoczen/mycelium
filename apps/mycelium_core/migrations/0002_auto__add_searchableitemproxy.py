# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("people", "0029_clear_search_proxies"),
        ("groups", "0026_clear_search_proxies"),
    )

    def forwards(self, orm):
        
        # Adding model 'SearchableItemProxy'
        db.create_table('mycelium_core_searchableitemproxy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qi_simple_searchable_search_field', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('search_group_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sorting_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('search_string', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cached_search_result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mycelium_core', ['SearchableItemProxy'])


    def backwards(self, orm):
        
        # Deleting model 'SearchableItemProxy'
        db.delete_table('mycelium_core_searchableitemproxy')


    models = {
        'mycelium_core.searchableitemproxy': {
            'Meta': {'ordering': "['sorting_name', '-id']", 'object_name': 'SearchableItemProxy'},
            'cached_search_result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'search_group_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'search_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sorting_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mycelium_core']
