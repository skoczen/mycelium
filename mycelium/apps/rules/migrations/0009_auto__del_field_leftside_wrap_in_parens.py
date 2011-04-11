# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'LeftSide.wrap_in_parens'
        db.delete_column('rules_leftside', 'wrap_in_parens')


    def backwards(self, orm):
        
        # Adding field 'LeftSide.wrap_in_parens'
        db.add_column('rules_leftside', 'wrap_in_parens', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    models = {
        'rules.leftside': {
            'Meta': {'ordering': "('order',)", 'object_name': 'LeftSide'},
            'add_closing_paren': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allowed_operators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rules.Operator']", 'symmetrical': 'False'}),
            'allowed_right_side_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rules.RightSideType']", 'symmetrical': 'False'}),
            'choices': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'query_string_partial': ('django.db.models.fields.TextField', [], {})
        },
        'rules.operator': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Operator'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'query_string_partial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'use_filter': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'rules.rightsidetype': {
            'Meta': {'object_name': 'RightSideType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rules']
