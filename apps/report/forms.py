from django import forms
from django.core.validators import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin import widgets
from collections import OrderedDict

from .models import ReportValue
from ..checklist.models import Item
from ..dictionary.models import Value

class ReportValueModelForm(forms.ModelForm):
    realvalue = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ReportValueModelForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            item = self.instance.item
            if item.type == 'check':
                realvalue = forms.NullBooleanField(initial = self.instance.boolean_value)
            elif item.type == 'dict':
                realvalue = forms.ModelChoiceField(Value.objects.filter(dictionary=self.instance.item.dictionary), initial = self.instance.key_value)
            elif item.type == 'int':
                realvalue = forms.IntegerField(initial = self.instance.int_value)
            elif item.type == 'date':
                realvalue = forms.DateField(initial = self.instance.date_value, widget = widgets.AdminDateWidget())
            elif item.type == 'datetime':
                realvalue = forms.DateTimeField(initial = self.instance.date_value, widget = widgets.AdminSplitDateTime())
            else:
                realvalue = forms.CharField(initial = self.instance.string_value)

            realvalue.required = False
            self.fields['realvalue'] = realvalue


    class Meta:
        model = ReportValue
        fields = '__all__'

