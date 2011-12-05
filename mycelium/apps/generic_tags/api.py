from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from generic_tags.models import TagSet, Tag
 
class TagSetResource(ModelResource):
    class Meta:
        queryset = TagSet.objects.all()
        authorization = Authorization()

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        authorization = Authorization()