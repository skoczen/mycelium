from django.contrib import admin
from models import *


admin.site.register(Person)
# admin.site.register(ContactMethodType)
# admin.site.register(EmailAddress)
# admin.site.register(PhoneNumber)
# admin.site.register(Address)
admin.site.register(Organization)
admin.site.register(OrganizationType)
admin.site.register(Employee)

