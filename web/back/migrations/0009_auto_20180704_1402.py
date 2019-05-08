# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-04 14:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0008_authuserinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuserinfo',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户id'),
        ),
    ]