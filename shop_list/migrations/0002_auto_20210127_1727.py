# Generated by Django 3.1.5 on 2021-01-27 08:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_list', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='hpURL',
        ),
        migrations.AddField(
            model_name='list',
            name='hpurl',
            field=models.TextField(blank=True, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='list',
            name='genre',
            field=models.CharField(choices=[('メンズ', 'メンズ'), ('ウィメンズ', 'ウィメンズ'), ('両方', '両方')], max_length=200),
        ),
        migrations.AlterField(
            model_name='list',
            name='treatused',
            field=models.CharField(choices=[('有', '有'), ('無', '無')], max_length=200),
        ),
    ]