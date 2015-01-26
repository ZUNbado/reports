# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=10, choices=[(b'string', b'String'), (b'check', b'Check Box'), (b'dict', b'Dictionary'), (b'int', b'Integer'), (b'date', b'Date'), (b'datetime', b'Date & time')])),
                ('sort', models.IntegerField(default=20)),
                ('dictionary', models.ForeignKey(blank=True, to='dictionary.Dictionary', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('sort', models.IntegerField(default=20)),
                ('checklist', models.ForeignKey(to='checklist.Checklist')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='section',
            field=models.ForeignKey(to='checklist.Section'),
            preserve_default=True,
        ),
    ]
