# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def backwards(self, orm):

        # Deleting model 'EmailAddress'
        db.delete_table('people_emailaddress')

        # Deleting model 'Address'
        db.delete_table('people_address')

        # Deleting model 'PhoneNumber'
        db.delete_table('people_phonenumber')

        # Deleting model 'ContactMethodType'
        db.delete_table('people_contactmethodtype')

        from people.models import PeopleAndOrganizationsSearchProxy
        PeopleAndOrganizationsSearchProxy.populate_cache()

    def forwards(self, orm):
        # Adding model 'EmailAddress'
        db.create_table('people_emailaddress', (
          ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
          ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
          ('contact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'], null=True, blank=True)),
          ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
          ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
          ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
          ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('people', ['EmailAddress'])

        # Adding model 'Address'
        db.create_table('people_address', (
          ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
          ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
          ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
          ('city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
          ('contact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'], null=True, blank=True)),
          ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
          ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
          ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
          ('state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
          ('line_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
          ('line_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('people', ['Address'])

        # Adding model 'PhoneNumber'
        db.create_table('people_phonenumber', (
          ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
          ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
          ('contact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'], null=True, blank=True)),
          ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
          ('modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
          ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
          ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('people', ['PhoneNumber'])

        # Adding model 'ContactMethodType'
        db.create_table('people_contactmethodtype', (
          ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
          ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
          ('internal_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('people', ['ContactMethodType'])        

    models = {
        'people.employee': {
            'Meta': {'ordering': "('organization', 'person')", 'object_name': 'Employee'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employees'", 'to': "orm['people.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employers'", 'to': "orm['people.Person']"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'people.organization': {
            'Meta': {'object_name': 'Organization'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.OrganizationType']", 'null': 'True', 'blank': 'True'}),
            'organization_type_other_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'primary_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'people.organizationtype': {
            'Meta': {'ordering': "('id',)", 'object_name': 'OrganizationType'},
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'people.peopleandorganizationssearchproxy': {
            'Meta': {'ordering': "('person', 'organization')", 'object_name': 'PeopleAndOrganizationsSearchProxy'},
            'cached_search_result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Organization']", 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'search_group_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'search_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'people.person': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Person'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['people']
