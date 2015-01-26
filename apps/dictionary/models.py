from django.db import models


class Dictionary(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.name

class Value(models.Model):
    dictionary = models.ForeignKey(Dictionary)
    value = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.value
