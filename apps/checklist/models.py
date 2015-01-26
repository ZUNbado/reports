from django.db import models

from ..dictionary.models import Dictionary

class Checklist(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.name

class Section(models.Model):
    name = models.CharField(max_length=200)
    checklist = models.ForeignKey(Checklist)
    sort = models.IntegerField(default=20)

    def __unicode__(self):
        return u'%s' % self.name

class Item(models.Model):
    name = models.CharField(max_length=200)
    section = models.ForeignKey(Section)
    type = models.CharField(max_length=10,choices=(
            ( 'string', 'String' ),
            ( 'check', 'Check Box' ),
            ( 'dict', 'Dictionary' ),
            ( 'int', 'Integer' ),
            ( 'date', 'Date' ),
            ( 'datetime', 'Date & time' ),
        )
    )
    dictionary = models.ForeignKey(Dictionary, null=True, blank=True)
    sort = models.IntegerField(default=20)

    def __unicode__(self):
        return u'%s' % self.name
