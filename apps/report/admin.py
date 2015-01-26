from django.contrib import admin
from django.conf.urls import patterns
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from datetime import datetime

from .models import Report, ReportValue
from .forms import ReportValueModelForm
from ..template.models import Block, Replace

class ReportValueInline(admin.TabularInline):
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



class ReportAdmin(admin.ModelAdmin):
    def preview_template(self, obj):
        return '<a href="preview/%i/">Preview</a>' % obj.id
    preview_template.allow_tags = True
    preview_template.short_description = 'Preview'

    inlines = [ ReportValueInline, ]
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
        contentreplaced = []
        for block in Block.objects.filter(template=report.checklist).order_by('sort'):
            for replace in Replace.objects.filter(block=block):
                value = ReportValue.objects.get(item=replace.item, report=report)
                if not value.isnull():
                    block.content = block.content.replace(replace.replace, value.getValue())
            block.content = block.content.split('\n')
            contentreplaced.append(block)


        return render_to_response('report/preview.html', {
            'report' : report,
            'blocks' : contentreplaced,
            }, context_instance=RequestContext(request))





admin.site.register(Report, ReportAdmin)
