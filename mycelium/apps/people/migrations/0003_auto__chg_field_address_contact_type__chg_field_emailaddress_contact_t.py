# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Address.contact_type'
        db.alter_column('people_address', 'contact_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'], null=True))

        # Changing field 'EmailAddress.contact_type'
        db.alter_column('people_emailaddress', 'contact_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'], null=True))

        # Deleting field 'PhoneNumber.phone'
        db.delete_column('people_phonenumber', 'phone')

        # Adding field 'PhoneNumber.phone_number'
        db.add_column('people_phonenumber', 'phone_number', self.gf('django.db.models.fields.CharField')(default=0, max_length=255), keep_default=False)

        # Changing field 'PhoneNumber.contact_type'
        db.alter_column('people_phonenumber', 'contact_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'], null=True))


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Address.contact_type'
        raise RuntimeError("Cannot reverse this migration. 'Address.contact_type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'EmailAddress.contact_type'
        raise RuntimeError("Cannot reverse this migration. 'EmailAddress.contact_type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'PhoneNumber.phone'
        raise RuntimeError("Cannot reverse this migration. 'PhoneNumber.phone' and its values cannot be restored.")

        # Deleting field 'PhoneNumber.phone_number'
        db.delete_column('people_phonenumber', 'phone_number')

        # User chose to not deal with backwards NULL issues for 'PhoneNumber.contact_type'
        raise RuntimeError("Cannot reverse this migration. 'PhoneNumber.contact_type' and its values cannot be restored.")


    models = {
        'people.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line_2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'Meta': {'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
