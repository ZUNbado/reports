from django.contrib import admin
from .models import Checklist, Section, Item
from grappelli_nested.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline




class ItemInline(NestedTabularInline):
    model = Item
    extra = 1

class SectionInline(NestedStackedInline):
    model = Section
    extra = 1
    inlines = [ ItemInline, ]

class ChecklistAdmin(NestedModelAdmin):
    inlines = [ SectionInline, ]

admin.site.register(Checklist, ChecklistAdmin)
