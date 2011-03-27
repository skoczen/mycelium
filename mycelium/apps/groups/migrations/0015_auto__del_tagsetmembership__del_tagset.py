# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'TagSetMembership'
        db.delete_table('groups_tagsetmembership')

        # Deleting model 'TagSet'
        db.delete_table('groups_tagset')


    def backwards(self, orm):
        
        # Adding model 'TagSetMembership'
        db.create_table('groups_tagsetmembership', (
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groups.TagSet'], null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groupmembership', null=True, to=orm['people.Person'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('groups', ['TagSetMembership'])

        # Adding model 'TagSet'
        db.create_table('groups_tagset', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('groups', ['TagSet'])


    models = {
        'groups.smartgroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'SmartGroup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'groups.smartgrouprule': {
            'Meta': {'ordering': "('group', 'id')", 'object_name': 'SmartGroupRule'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.SmartGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['groups']
