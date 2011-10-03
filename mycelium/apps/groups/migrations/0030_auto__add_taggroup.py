# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TagGroup'
        db.create_table('groups_taggroup', (
            ('group_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['groups.Group'], unique=True, primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['generic_tags.Tag'])),
        ))
        db.send_create_signal('groups', ['TagGroup'])


    def backwards(self, orm):
        
        # Deleting model 'TagGroup'
        db.delete_table('groups_taggroup')


    models = {
        'accounts.account': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Account'},
            'agreed_to_terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'challenge_has_added_a_donation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'challenge_has_added_board': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'challenge_has_created_other_accounts': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'challenge_has_downloaded_spreadsheet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'challenge_has_imported_contacts': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'challenge_has_logged_volunteer_hours': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'challenge_has_set_up_tags': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'challenge_has_submitted_support': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feature_access_level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'free_trial_ends_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'has_completed_all_challenges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_completed_any_challenges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_demo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_four': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'last_stripe_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'next_billing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Plan']", 'blank': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signup_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 1, 2, 41, 31, 243562)', 'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stripe_customer_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'was_a_feedback_partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'accounts.plan': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Plan'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stripe_plan_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'generic_tags.tag': {
            'Meta': {'ordering': "('tagset', 'name')", 'object_name': 'Tag'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'tagset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic_tags.TagSet']", 'null': 'True', 'blank': 'True'})
        },
        'generic_tags.tagset': {
            'Meta': {'ordering': "('id',)", 'object_name': 'TagSet'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'groups.group': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Group'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rules_boolean': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'groups.grouprule': {
            'Meta': {'ordering': "('group', 'id')", 'object_name': 'GroupRule'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_side': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rules.LeftSide']", 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rules.Operator']", 'null': 'True', 'blank': 'True'}),
            'right_side_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rules.RightSideType']", 'null': 'True', 'blank': 'True'}),
            'right_side_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'groups.groupsearchproxy': {
            'Meta': {'ordering': "['sorting_name', '-id']", 'object_name': 'GroupSearchProxy', '_ormbases': ['mycelium_core.SearchableItemProxy']},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']", 'null': 'True', 'blank': 'True'}),
            'searchableitemproxy_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mycelium_core.SearchableItemProxy']", 'unique': 'True', 'primary_key': 'True'})
        },
        'groups.taggroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'TagGroup', '_ormbases': ['groups.Group']},
            'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['groups.Group']", 'unique': 'True', 'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic_tags.Tag']"})
        },
        'mycelium_core.searchableitemproxy': {
            'Meta': {'ordering': "['sorting_name', '-id']", 'object_name': 'SearchableItemProxy'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'cached_search_result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'search_group_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'search_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sorting_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'rules.leftside': {
            'Meta': {'ordering': "('order',)", 'object_name': 'LeftSide'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
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
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
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
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['groups']
