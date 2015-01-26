from django.contrib import admin
from django.conf.urls import patterns
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from datetime import datetime
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline


from .models import Report, ReportSection, ReportValue
from .forms import ReportValueModelForm
from ..template.models import Template, Block, Replace

class ReportValueInline(NestedTabularInline):
    model = ReportValue
    extra = 0
    max_num = 0
    readonly_fields = [ 'item' ]
    form = ReportValueModelForm

    fieldsets = (
            (None, {
                'fields' : [ 'item', 'realvalue' ]
                }),
            )

class ReportSectionInline(NestedStackedInline):
    model = ReportSection
    extra = 0
    max_num = 0
    inlines = [ ReportValueInline, ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [ 'section' ]
        return []

class ReportAdmin(NestedModelAdmin):
    def preview_template(self, obj):
        return '<a href="preview/%i/">Preview</a>' % obj.id
    preview_template.allow_tags = True
    preview_template.short_description = 'Preview'

    inlines = [ ReportSectionInline, ]
    list_display = [ 'name', 'checklist', 'status', 'preview_template' ]
    fieldsets = (
            (None, {
                'fields' : [ 'name', 'checklist'  ]
                }),
            )

    def save_formset(self, request, form, formset, change):
        super(ReportAdmin, self).save_formset(request, form, formset, change)
        formset.save()
        for check in formset.forms:
            if isinstance(check.instance, ReportValue):
                value = check.cleaned_data['realvalue']
                itemvalue = check.cleaned_data['id']

                if itemvalue.item.type == 'check':
                    itemvalue.boolean_value = value
                elif itemvalue.item.type == 'dict':
                    itemvalue.key_value = value
                elif itemvalue.item.type == 'int':
                    itemvalue.int_value = value
                elif itemvalue.item.type in [ 'date', 'datetime' ]:
                    itemvalue.date_value = value
                else:
                    itemvalue.string_value = value

                itemvalue.save()

    def get_urls(self):
        urls = super(ReportAdmin, self).get_urls()
        my_urls = patterns('',
                (r'^preview/(?P<report_id>\d+)/send/$', self.send_report),
                (r'^preview/(?P<report_id>\d+)/$', self.preview)
                )
        return my_urls + urls

    def send_report(self, request, report_id):
        report = get_object_or_404(Report, pk=report_id)
        if request.method == 'POST':
            form = SendToReport(request.POST)
            if form.is_valid():
                report.save()

        return redirect(reverse('admin:report_report_changelist'))

    def preview(self, request, report_id):
        report = get_object_or_404(Report, pk=report_id)
        template = Template.objects.get(checklist=report.checklist)
        contentreplaced = []
        print report
        for block in Block.objects.filter(template=template).order_by('sort'):
            print "block %s" % block
            for replace in Replace.objects.filter(block=block):
                value = ReportValue.objects.get(item=replace.item, reportsection__in=ReportSection.objects.filter(report=report))
                print value
                if not value.isnull():
                    block.content = block.content.replace(replace.replace, value.getValue())
            block.content = block.content.split('\n')
            contentreplaced.append(block)


        return render_to_response('report/preview.html', {
            'report' : report,
            'blocks' : contentreplaced,
            }, context_instance=RequestContext(request))


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [ 'checklist' ]
        return []



admin.site.register(Report, ReportAdmin)
