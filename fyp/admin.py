from django.contrib import admin

from django.contrib import admin
from .models import Business, Event

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'category')

admin.site.register(Business, BusinessAdmin)
admin.site.register(Event)
