# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Operator'
        db.create_table('rules_operator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('query_string_partial', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=100)),
        ))
        db.send_create_signal('rules', ['Operator'])

        # Adding model 'RightSideType'
        db.create_table('rules_rightsidetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('rules', ['RightSideType'])

        # Adding model 'RightSideValue'
        db.create_table('rules_rightsidevalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('right_side_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rules.RightSideType'])),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('rules', ['RightSideValue'])

        # Adding model 'LeftSide'
        db.create_table('rules_leftside', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('query_string_partial', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('rules', ['LeftSide'])

        # Adding M2M table for field allowed_operators on 'LeftSide'
        db.create_table('rules_leftside_allowed_operators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('leftside', models.ForeignKey(orm['rules.leftside'], null=False)),
            ('operator', models.ForeignKey(orm['rules.operator'], null=False))
        ))
        db.create_unique('rules_leftside_allowed_operators', ['leftside_id', 'operator_id'])

        # Adding M2M table for field allowed_right_side_types on 'LeftSide'
        db.create_table('rules_leftside_allowed_right_side_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('leftside', models.ForeignKey(orm['rules.leftside'], null=False)),
            ('rightsidetype', models.ForeignKey(orm['rules.rightsidetype'], null=False))
        ))
        db.create_unique('rules_leftside_allowed_right_side_types', ['leftside_id', 'rightsidetype_id'])


    def backwards(self, orm):
        
        # Deleting model 'Operator'
        db.delete_table('rules_operator')

        # Deleting model 'RightSideType'
        db.delete_table('rules_rightsidetype')

        # Deleting model 'RightSideValue'
        db.delete_table('rules_rightsidevalue')

        # Deleting model 'LeftSide'
        db.delete_table('rules_leftside')

        # Removing M2M table for field allowed_operators on 'LeftSide'
        db.delete_table('rules_leftside_allowed_operators')

        # Removing M2M table for field allowed_right_side_types on 'LeftSide'
        db.delete_table('rules_leftside_allowed_right_side_types')


    models = {
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

    complete_apps = ['rules']
