from django.forms import ModelForm

def adjust_queryset_for_account_based_models(f, *args, **kwargs):
    if hasattr(f,"queryset"):
        print "has queryset"
    


class AccountBasedModelForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ModelForm, self).__init__(*args,**kwargs)
        for f in self.fields:
            if f.instance and  hasattr(f,"queryset"):
                pass
                # print f.instance
                # print f.queryset
                # f.queryset = f.rel.to._default_manager(request).using(db).complex_filter(f.rel.limit_choices_to)

    # formfield_callback = adjust_queryset_for_account_based_models