# Generated by Django 3.1.5 on 2021-02-10 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_list', '0008_treatblands'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='treat_bland',
            field=models.ManyToManyField(blank=True, related_name='取扱ブランド', to='shop_list.TreatBlands'),
        ),
    ]
