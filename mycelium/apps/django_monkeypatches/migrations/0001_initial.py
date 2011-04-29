# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'User.username'
        db.alter_column('auth_user', 'username', models.CharField(max_length=100))


    def backwards(self, orm):

        # Changing field 'User.username'
        db.alter_column('auth_user', 'username', models.CharField(max_length=35))


    models = {
        
    }

    complete_apps = ['django_monkeypatches']
