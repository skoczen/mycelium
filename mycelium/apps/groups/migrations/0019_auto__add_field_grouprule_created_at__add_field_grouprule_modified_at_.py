# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'GroupRule.created_at'
        db.add_column('groups_grouprule', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'GroupRule.modified_at'
        db.add_column('groups_grouprule', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'GroupRule.left_side'
        db.add_column('groups_grouprule', 'left_side', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rules.LeftSide'], null=True, blank=True), keep_default=False)

        # Adding field 'GroupRule.operator'
        db.add_column('groups_grouprule', 'operator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rules.Operator'], null=True, blank=True), keep_default=False)

        # Adding field 'GroupRule.right_side_value'
        db.add_column('groups_grouprule', 'right_side_value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rules.RightSideValue'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'GroupRule.created_at'
        db.delete_column('groups_grouprule', 'created_at')

        # Deleting field 'GroupRule.modified_at'
        db.delete_column('groups_grouprule', 'modified_at')

        # Deleting field 'GroupRule.left_side'
        db.delete_column('groups_grouprule', 'left_side_id')

        # Deleting field 'GroupRule.operator'
        db.delete_column('groups_grouprule', 'operator_id')

        # Deleting field 'GroupRule.right_side_value'
        db.delete_column('groups_grouprule', 'right_side_value_id')


    models = {
        'groups.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'groups.grouprule': {
            'Meta': {'ordering': "('group', 'id')", 'object_name': 'GroupRule'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_side': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rules.LeftSide']", 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rules.Operator']", 'null': 'True', 'blank': 'True'}),
            'right_side_value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rules.RightSideValue']", 'null': 'True', 'blank': 'True'})
        },
        'rules.leftside': {
            'Meta': {'object_name': 'LeftSide'},
            'allowed_operators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rules.Operator']", 'symmetrical': 'False'}),
            'allowed_right_side_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rules.RightSideType']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'query_string_partial': ('django.db.models.fields.TextField', [], {})
        },
        'rules.operator': {
            'Meta': {'object_name': 'Operator'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'query_string_partial': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'rules.rightsidetype': {
            'Meta': {'object_name': 'RightSideType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'rules.rightsidevalue': {
            'Meta': {'object_name': 'RightSideValue'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'right_side_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rules.RightSideType']"}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['groups']
