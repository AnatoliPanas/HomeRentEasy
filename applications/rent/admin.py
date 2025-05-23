from django.contrib import admin

from applications.rent.models import Address, Rent

admin.site.register(Address)
admin.site.register(Rent)