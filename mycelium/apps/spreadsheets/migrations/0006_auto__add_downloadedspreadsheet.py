# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DownloadedSpreadsheet'
        db.create_table('spreadsheets_downloadedspreadsheet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Account'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('spreadsheet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spreadsheets.Spreadsheet'])),
            ('num_records', self.gf('django.db.models.fields.IntegerField')()),
            ('file_type', self.gf('django.db.models.fields.CharField')(default='CSV', max_length=20)),
            ('downloaded_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('spreadsheets', ['DownloadedSpreadsheet'])


    def backwards(self, orm):
        
        # Deleting model 'DownloadedSpreadsheet'
        db.delete_table('spreadsheets_downloadedspreadsheet')


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
            'signup_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 24, 4, 13, 23, 227653)', 'null': 'True'}),
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
        'spreadsheets.downloadedspreadsheet': {
            'Meta': {'object_name': 'DownloadedSpreadsheet'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'downloaded_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'default': "'CSV'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'num_records': ('django.db.models.fields.IntegerField', [], {}),
            'spreadsheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spreadsheets.Spreadsheet']"})
        },
        'spreadsheets.spreadsheet': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Spreadsheet'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_filetype': ('django.db.models.fields.CharField', [], {'default': "'CSV'", 'max_length': '255'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groups.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'spreadsheet_template': ('django.db.models.fields.CharField', [], {'default': "'full_contact_list'", 'max_length': '255'})
        },
        'spreadsheets.spreadsheetsearchproxy': {
            'Meta': {'ordering': "['sorting_name', '-id']", 'object_name': 'SpreadsheetSearchProxy', '_ormbases': ['mycelium_core.SearchableItemProxy']},
            'searchableitemproxy_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mycelium_core.SearchableItemProxy']", 'unique': 'True', 'primary_key': 'True'}),
            'spreadsheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spreadsheets.Spreadsheet']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spreadsheets']
