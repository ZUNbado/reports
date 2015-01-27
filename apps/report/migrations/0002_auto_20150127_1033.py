# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0001_initial'),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='checklist',
        ),
        migrations.AddField(
            model_name='report',
            name='template',
            field=models.ForeignKey(default=1, to='template.Template'),
            preserve_default=False,
        ),
    ]
