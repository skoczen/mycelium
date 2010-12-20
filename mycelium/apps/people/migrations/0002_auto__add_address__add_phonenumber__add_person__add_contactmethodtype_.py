# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Address'
        db.create_table('people_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('contact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('line_1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line_2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('people', ['Address'])

        # Adding model 'PhoneNumber'
        db.create_table('people_phonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('contact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('people', ['PhoneNumber'])

        # Adding model 'Person'
        db.create_table('people_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('people', ['Person'])

        # Adding model 'ContactMethodType'
        db.create_table('people_contactmethodtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('internal_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('people', ['ContactMethodType'])

        # Adding model 'EmailAddress'
        db.create_table('people_emailaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('contact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.ContactMethodType'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
        ))
        db.send_create_signal('people', ['EmailAddress'])


    def backwards(self, orm):
        
        # Deleting model 'Address'
        db.delete_table('people_address')

        # Deleting model 'PhoneNumber'
        db.delete_table('people_phonenumber')

        # Deleting model 'Person'
        db.delete_table('people_person')

        # Deleting model 'ContactMethodType'
        db.delete_table('people_contactmethodtype')

        # Deleting model 'EmailAddress'
        db.delete_table('people_emailaddress')


    models = {
        'people.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']"}),
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
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']"}),
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
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.ContactMethodType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['people']
