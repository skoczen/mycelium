# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Group.name'
        db.add_column('groups_group', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'SmartGroupRule.group'
        db.add_column('groups_smartgrouprule', 'group', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['groups.SmartGroup']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Group.name'
        db.delete_column('groups_group', 'name')

        # Deleting field 'SmartGroupRule.group'
        db.delete_column('groups_smartgrouprule', 'group_id')


    models = {
        'groups.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.SmartGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['groups']
