# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-23 15:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=120)),
                ('currency', models.CharField(choices=[('$', 'US Dollars ($)')], default='$', max_length=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('product_database', models.CharField(choices=[('db_1', 'database1'), ('db_2', 'database2'), ('db_3', 'database3'), ('db_4', 'database4'), ('db_5', 'database5'), ('user', 'user'), ('default', 'dafault')], max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=150)),
                ('signup_confirmation', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=150)),
                ('age', models.IntegerField()),
                ('database_access', models.CharField(max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
