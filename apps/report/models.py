from django.db import models
from ..checklist.models import Checklist, Item
from ..dictionary.models import Value


class Report(models.Model):
    name = models.CharField(max_length=200)
    checklist = models.ForeignKey(Checklist)

    def __unicode__(self):
        return u'%s' % self.name

    def status(self):
        values = ReportValue.objects.filter(report=self)
        total = float(len(values))
        completed = float(0)
        for value in values:
            if not value.isnull():
                completed = completed + 1
        status = completed / total * 100
        return u'%.2f %%' % status

    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)
        for item in Item.objects.filter(checklist=self.checklist):
            ReportValue.objects.get_or_create(report=self, item=item)


class ReportValue(models.Model):
    report = models.ForeignKey(Report)
    item = models.ForeignKey(Item)
    string_value = models.CharField(max_length=200,blank=True,null=True)
    boolean_value = models.NullBooleanField(null=True, blank=True)
    key_value = models.ForeignKey(Value, null=True, blank=True)
    int_value = models.IntegerField(null=True, blank=True)
    date_value = models.DateTimeField(null=True, blank=True)

    def isnull(self):
        if self.item.type == 'string' and self.string_value is not None:
            return False
        elif self.item.type == 'check' and self.boolean_value is not None:
            return False
        elif self.item.type == 'dict' and self.key_value is not None:
            return False
        elif self.item.type == 'int' and self.int_value is not None:
            return False
        elif self.item.type in [ 'date', 'datetime', 'time'] and self.date_value is not None:
            return False
        else:
            return True

    def getValue(self):
        if self.item.type == 'string' and self.string_value is not None:
            value = self.string_value
        elif self.item.type == 'check' and self.boolean_value is not None:
            value = self.boolean_value
        elif self.item.type == 'dict' and self.key_value is not None:
            value = self.key_value.name
        elif self.item.type == 'int' and self.int_value is not None:
            value = self.int_value
        elif self.item.type in [ 'date', 'datetime', 'time'] and self.date_value is not None:
            value = self.date_value
        else:
            value = None

        return u'%s' % value
