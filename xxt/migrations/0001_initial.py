# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-11-25 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Xxt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xxt_full_url', models.CharField(max_length=500)),
                ('xxt_course_url', models.CharField(default='', max_length=500)),
            ],
            options={
                'db_table': 'xxt',
            },
        ),
    ]