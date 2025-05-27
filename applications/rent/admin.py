from django.contrib import admin

from applications.rent.models.rent import Address, Rent

admin.site.register(Address)
admin.site.register(Rent)