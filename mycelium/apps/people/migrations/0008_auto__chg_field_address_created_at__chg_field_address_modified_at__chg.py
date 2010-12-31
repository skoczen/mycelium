# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Address.created_at'
        db.alter_column('people_address', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Address.modified_at'
        db.alter_column('people_address', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'EmailAddress.created_at'
        db.alter_column('people_emailaddress', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'EmailAddress.modified_at'
        db.alter_column('people_emailaddress', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Person.created_at'
        db.alter_column('people_person', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Person.modified_at'
        db.alter_column('people_person', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PhoneNumber.created_at'
        db.alter_column('people_phonenumber', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'PhoneNumber.modified_at'
        db.alter_column('people_phonenumber', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'Address.created_at'
        db.alter_column('people_address', 'created_at', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Address.modified_at'
        db.alter_column('people_address', 'modified_at', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'EmailAddress.created_at'
        db.alter_column('people_emailaddress', 'created_at', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'EmailAddress.modified_at'
        db.alter_column('people_emailaddress', 'modified_at', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Person.created_at'
        db.alter_column('people_person', 'created_at', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Person.modified_at'
        db.alter_column('people_person', 'modified_at', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'PhoneNumber.created_at'
        db.alter_column('people_phonenumber', 'created_at', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'PhoneNumber.modified_at'
        db.alter_column('people_phonenumber', 'modified_at', self.gf('django.db.models.fields.DateField')(null=True))


    models = {
        'people.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'people.person': {
            'Meta': {'ordering': "('first_name', 'last_name')", 'object_name': 'Person'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'qi_simple_searchable_search_field': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'people.phonenumber': {
            'Meta': {'object_name': 'PhoneNumber'},
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['people']
