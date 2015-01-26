from django.contrib import admin
from .models import Template, Block, Replace
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline


class ReplaceInline(NestedTabularInline):
    model = Replace
    extra = 0

class BlockInline(NestedStackedInline):
    model = Block
    extra = 0
    inlines = [ ReplaceInline, ]

class TemplateAdmin(NestedModelAdmin):
    inlines = [ BlockInline, ]

admin.site.register(Template, TemplateAdmin)
