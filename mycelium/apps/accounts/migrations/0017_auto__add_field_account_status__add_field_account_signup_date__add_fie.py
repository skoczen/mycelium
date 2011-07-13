# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Account.status'
        db.add_column('accounts_account', 'status', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Account.signup_date'
        db.add_column('accounts_account', 'signup_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 12, 18, 44, 14, 259395), null=True), keep_default=False)

        # Adding field 'Account.last_billing_date'
        db.add_column('accounts_account', 'last_billing_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Account.chargify_subscription_started'
        db.add_column('accounts_account', 'chargify_subscription_started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Account.chargify_subscription_id'
        db.add_column('accounts_account', 'chargify_subscription_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Account.chargify_state'
        db.add_column('accounts_account', 'chargify_state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Account.chargify_activated_at'
        db.add_column('accounts_account', 'chargify_activated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Account.chargify_cancel_at_end_of_period'
        db.add_column('accounts_account', 'chargify_cancel_at_end_of_period', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Account.chargify_next_assessment_at'
        db.add_column('accounts_account', 'chargify_next_assessment_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Account.status'
        db.delete_column('accounts_account', 'status')

        # Deleting field 'Account.signup_date'
        db.delete_column('accounts_account', 'signup_date')

        # Deleting field 'Account.last_billing_date'
        db.delete_column('accounts_account', 'last_billing_date')

        # Deleting field 'Account.chargify_subscription_started'
        db.delete_column('accounts_account', 'chargify_subscription_started')

        # Deleting field 'Account.chargify_subscription_id'
        db.delete_column('accounts_account', 'chargify_subscription_id')

        # Deleting field 'Account.chargify_state'
        db.delete_column('accounts_account', 'chargify_state')

        # Deleting field 'Account.chargify_activated_at'
        db.delete_column('accounts_account', 'chargify_activated_at')

        # Deleting field 'Account.chargify_cancel_at_end_of_period'
        db.delete_column('accounts_account', 'chargify_cancel_at_end_of_period')

        # Deleting field 'Account.chargify_next_assessment_at'
        db.delete_column('accounts_account', 'chargify_next_assessment_at')


    models = {
        'accounts.accesslevel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AccessLevel'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
            'chargify_activated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'chargify_cancel_at_end_of_period': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chargify_next_assessment_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'chargify_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'chargify_subscription_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'chargify_subscription_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'has_completed_all_challenges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_completed_any_challenges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_billing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Plan']", 'blank': 'True'}),
            'signup_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 12, 18, 44, 14, 259395)', 'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'accounts.plan': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Plan'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'accounts.useraccount': {
            'Meta': {'ordering': "('account', 'nickname', 'user__first_name', 'access_level', 'user')", 'object_name': 'UserAccount'},
            'access_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.AccessLevel']"}),
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'show_challenges_complete_section': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']
