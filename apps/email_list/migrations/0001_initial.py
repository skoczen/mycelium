# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EmailSubscription'
        db.create_table('email_list_emailsubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('email_list', ['EmailSubscription'])


    def backwards(self, orm):
        
        # Deleting model 'EmailSubscription'
        db.delete_table('email_list_emailsubscription')


    models = {
        'email_list.emailsubscription': {
            'Meta': {'object_name': 'EmailSubscription'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['email_list']
