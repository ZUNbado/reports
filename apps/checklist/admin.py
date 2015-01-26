from django.contrib import admin
from .models import Checklist, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

class ChecklistAdmin(admin.ModelAdmin):
    inlines = [ ItemInline, ]

admin.site.register(Checklist, ChecklistAdmin)
