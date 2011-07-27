# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        from django.contrib.contenttypes.models import ContentType
        tsm_ct = ContentType.objects.get_for_model(orm.TagSetMembership)
        vol_ts = orm.TagSet.objects.get(name="Volunteer")
        don_ts = orm.TagSet.objects.get(name="Donor")

        volunteer_tags = ["friday morning volunteer", "monday volunteer", "tuesday volunteer", "wednesday volunteer"]
        donor_tags = ["potential donor",]
        delete_tags = ["volunteer", "donor", "testing", "developer", "cook", "editing", "awesome", "photographer"]

        for ti in orm["taggit.taggeditem"].objects.filter(content_type=tsm_ct):
            my_tsm = orm.TagSetMembership.objects.get(pk=ti.object_id)
            p = orm["people.Person"].objects.get(pk=my_tsm.person_id)

            volunteer_id = orm.TagSetMembership.objects.get_or_create(tagset=vol_ts, person=p)[0].id
            donor_id = orm.TagSetMembership.objects.get_or_create(tagset=don_ts, person=p)[0].id

            if ti.tag.name in delete_tags:
                ti.delete()
            elif ti.tag.name in volunteer_tags:
                ti.object_id = volunteer_id
                ti.save()
            elif ti.tag.name in donor_tags:
                ti.object_id = donor_id
                ti.save()

        rename_tags = [
            ("cli board member", "board member"),
            ("great editing skills", "editing skills"),
            ("friday morning volunteer", "friday morning"),
            ("monday volunteer", "monday"),
            ("tuesday volunteer", "tuesday"),
            ("wednesday volunteer", "wednesday"),
        ]

        for ren_tup in rename_tags:
            try:
                tag = orm["taggit.tag"].objects.get(name=ren_tup[0])
                tag.name=ren_tup[1]
                tag.save()
            except:
                pass
        

    def backwards(self, orm):
        "Write your backwards methods here."
        print "Don't worry about it."

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic_tags.tagset': {
            'Meta': {'ordering': "('id',)", 'object_name': 'TagSet'},
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

    complete_apps = ['generic_tags']
