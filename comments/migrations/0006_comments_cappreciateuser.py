# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-07-25 09:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0005_comments_cappreciatenum'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='cappreciateuser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hascappreciate_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
