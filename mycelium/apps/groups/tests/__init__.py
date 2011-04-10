from generic_tags.models import TagSet, Tag

class GroupTestAbstractions(object):

    def create_tag_for_person(self, person=None, tagset_name=None, tag=None):
        ts = TagSet.objects.get_or_create(name=tagset_name)[0]
        t = Tag.objects.get_or_create(name=tag, tagset=ts)[0]
        t.add_tag_to_person(person)
