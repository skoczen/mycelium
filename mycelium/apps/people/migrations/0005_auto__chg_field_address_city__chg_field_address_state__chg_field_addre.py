# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Address.city'
        db.alter_column('people_address', 'city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Address.state'
        db.alter_column('people_address', 'state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Address.postal_code'
        db.alter_column('people_address', 'postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Address.line_1'
        db.alter_column('people_address', 'line_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Address.line_2'
        db.alter_column('people_address', 'line_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))


    def backwards(self, orm):
        
        # Changing field 'Address.city'
        db.alter_column('people_address', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Address.state'
        db.alter_column('people_address', 'state', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Address.postal_code'
        db.alter_column('people_address', 'postal_code', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

        # Changing field 'Address.line_1'
        db.alter_column('people_address', 'line_1', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

        # Changing field 'Address.line_2'
        db.alter_column('people_address', 'line_2', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))


    models = {
        'people.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'people.contactmethodtype': {
            'Meta': {'object_name': 'ContactMethodType'},
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'people.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'people.person': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'people.phonenumber': {
            'Meta': {'object_name': 'PhoneNumber'},
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['people']
