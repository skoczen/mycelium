# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Logo.image'
        db.alter_column('logo_maker_logo', 'image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100))


    def backwards(self, orm):
        
        # Changing field 'Logo.image'
        db.alter_column('logo_maker_logo', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))


    models = {
        'logo_maker.logo': {
            'Meta': {'object_name': 'Logo'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['logo_maker']
