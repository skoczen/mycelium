# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        db.rename_table('groups_smartgroup', 'groups_group')
        db.rename_table('groups_smartgrouprule', 'groups_grouprule')

    def backwards(self, orm):
        db.rename_table('groups_group', 'groups_smartgroup')
        db.rename_table('groups_grouprule', 'groups_smartgrouprule')

    models = {
        'groups.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'groups.grouprule': {
            'Meta': {'ordering': "('group', 'id')", 'object_name': 'GroupRule'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['groups']
