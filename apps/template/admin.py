from django.contrib import admin
from .models import Template, Block, Replace
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline


class ReplaceInline(NestedStackedInline):
    model = Replace

class BlockInline(NestedStackedInline):
    model = Block
    inlines = [ ReplaceInline, ]

class TemplateAdmin(NestedModelAdmin):
    inlines = [ BlockInline, ]

admin.site.register(Template, TemplateAdmin)
