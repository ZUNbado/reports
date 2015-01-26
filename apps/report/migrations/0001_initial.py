# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
        ('checklist', '0002_item_sort'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('checklist', models.ForeignKey(to='checklist.Checklist')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string_value', models.CharField(max_length=200, null=True, blank=True)),
                ('boolean_value', models.NullBooleanField()),
                ('int_value', models.IntegerField(null=True, blank=True)),
                ('date_value', models.DateTimeField(null=True, blank=True)),
                ('item', models.ForeignKey(to='checklist.Item')),
                ('key_value', models.ForeignKey(blank=True, to='dictionary.Value', null=True)),
                ('report', models.ForeignKey(to='report.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
