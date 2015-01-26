from django.db import models

from ..checklist.models import Checklist, Item

class Template(models.Model):
    name = models.CharField(max_length=200)
    checklist = models.ForeignKey(Checklist)

    def __unicode__(self):
        return u'%s' % self.name

class Block(models.Model):
    title = models.CharField(max_length=200)
    template = models.ForeignKey(Template)
    content = models.TextField()
    sort = models.IntegerField(default=15)

class Replace(models.Model):
    name = models.CharField(max_length=200)
    block = models.ForeignKey(Block)
    replace = models.CharField(max_length=200)
    item = models.ForeignKey(Item)
