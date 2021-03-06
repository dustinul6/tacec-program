# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsheet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='parallelOrder',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='session',
            name='slot',
            field=models.CharField(default='session', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='moderator',
            field=models.ManyToManyField(related_name='sessionsm', to='gsheet.Staff'),
        ),
        migrations.AddField(
            model_name='session',
            name='organizer',
            field=models.ManyToManyField(related_name='sessions', to='gsheet.Staff'),
        ),
        migrations.AddField(
            model_name='session',
            name='room',
            field=models.ManyToManyField(to='gsheet.Room'),
        ),
    ]
