from django.contrib import admin
from models import Plan, Account, AccessLevel, UserAccount

admin.site.register(Plan)
admin.site.register(Account)
admin.site.register(AccessLevel)
admin.site.register(UserAccount)