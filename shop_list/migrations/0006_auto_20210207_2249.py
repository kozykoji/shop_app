# Generated by Django 3.1.5 on 2021-02-07 13:49

from django.db import migrations,  models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_list', '0005_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='post1',
            new_name='post',
        ),
    ]