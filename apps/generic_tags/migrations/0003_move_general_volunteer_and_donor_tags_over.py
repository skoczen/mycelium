# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    depends_on = (
        ("groups", "0014_copy_data_to_generic_tags"),
    )

    def forwards(self, orm):
        # Previous migrations moved the general current tags into the TagSet object. Crap.  Fix that, and move them to the right place.
        
        # Get the right one again
        gen_ts = orm.TagSet.objects.get_or_create(name="General")[0]

        from django.contrib.contenttypes.models import ContentType
        tsm_ct = ContentType.objects.get_for_model(orm.TagSetMembership)
        people_whose_tsms_to_clear = []

        for tsm in orm.TagSetMembership.objects.all():
            new_person_tsm = orm.TagSetMembership.objects.get_or_create(person=tsm.person,tagset=gen_ts)[0]

            new_tag = orm["taggit.tag"].objects.get_or_create(name=tsm.tagset.name)[0]
            orm["taggit.taggeditem"].objects.get_or_create(tag=new_tag, object_id=new_person_tsm.id, content_type_id=tsm_ct.id)
            people_whose_tsms_to_clear.append(tsm.person)

        # clear out people's non-general tsms.
        for p in people_whose_tsms_to_clear:
            for tsm in orm.TagSetMembership.objects.filter(person=p):
                if tsm.tagset != gen_ts:
                    tsm.delete()

        # Clear out all the crap
        for ts in orm.TagSet.objects.all():
            if ts != gen_ts:
                ts.delete()
        
        # Re-make the other general tagsets we want.
        orm.TagSet.objects.get_or_create(name="Volunteer")
        orm.TagSet.objects.get_or_create(name="Donor")
       


    def backwards(self, orm):
        "Write your backwards methods here."

        print "NO BACKWARDS MIGRATION!!  Seriously. Have you seen the forwards migration? Hell no!"

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic_tags.tagset': {
            'Meta': {'ordering': "('name',)", 'object_name': 'TagSet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'generic_tags.tagsetmembership': {
            'Meta': {'ordering': "('tagset', 'person')", 'object_name': 'TagSetMembership'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'tagset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['generic_tags.TagSet']", 'null': 'True', 'blank': 'True'})
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
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['taggit', 'generic_tags']
