from django.contrib import admin
from .models import Template, Block, Replace
from ..checklist.models import Checklist, Section, Item
from grappelli_nested.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline


class ReplaceInline(NestedTabularInline):
    model = Replace
    extra = 0

    def formfield_for_foreignkey(self, field, request, **kwargs):
        if request.META['PATH_INFO'].strip('/').split('/')[-1] != 'add':
            template = self.get_object(request, Template)
            queryset = None
            if field.name == "item":
                kwargs["queryset"] = Item.objects.filter(section__in=Section.objects.filter(checklist=template.checklist))
        return super(ReplaceInline, self).formfield_for_foreignkey(field, request, **kwargs)

    def get_object(self, request, model):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        return model.objects.get(pk=object_id)

class BlockInline(NestedStackedInline):
    model = Block
    extra = 0
    inlines = [ ReplaceInline, ]

class TemplateAdmin(NestedModelAdmin):
    inlines = [ BlockInline, ]
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [ 'checklist' ]
        return []

admin.site.register(Template, TemplateAdmin)
