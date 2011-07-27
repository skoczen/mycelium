# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Group'
        db.create_table('groups_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('groups', ['Group'])

        # Adding model 'SmartGroupRule'
        db.create_table('groups_smartgrouprule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('groups', ['SmartGroupRule'])

        # Adding model 'SmartGroup'
        db.create_table('groups_smartgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('groups', ['SmartGroup'])


    def backwards(self, orm):
        
        # Deleting model 'Group'
        db.delete_table('groups_group')

        # Deleting model 'SmartGroupRule'
        db.delete_table('groups_smartgrouprule')

        # Deleting model 'SmartGroup'
        db.delete_table('groups_smartgroup')


    models = {
        'groups.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'groups.smartgroup': {
            'Meta': {'object_name': 'SmartGroup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'groups.smartgrouprule': {
            'Meta': {'object_name': 'SmartGroupRule'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['groups']
