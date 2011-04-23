from generic_tags.models import TagSet, Tag
class GroupTestAbstractions(object):

    def create_tag_for_person(self, account=None, person=None, tagset_name=None, tag=None):
        if not account and not person:
            raise Exception, "Missing account and person."
        else:
            if not account:
                account = person.account

        ts = TagSet.raw_objects.get_or_create(account=account, name=tagset_name)[0]
        t = Tag.raw_objects.get_or_create(account=account, name=tag, tagset=ts)[0]
        t.add_tag_to_person(person)
