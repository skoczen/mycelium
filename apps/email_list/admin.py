from django.contrib import admin
from models import *

class EmailSubscriptionOptions(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)

admin.site.register(EmailSubscription,EmailSubscriptionOptions)