from django.contrib import admin
from .models import Dictionary, Value

class ValueInline(admin.TabularInline):
    model = Value
    extra = 1

class DictionaryAdmin(admin.ModelAdmin):
    inlines = [ ValueInline, ]

admin.site.register(Dictionary, DictionaryAdmin)
