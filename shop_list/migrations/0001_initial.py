# Generated by Django 3.1.5 on 2021-01-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopname', models.CharField(max_length=200)),
                ('treatbland', models.CharField(max_length=200)),
                ('treatused', models.BooleanField(default=False)),
                ('genre', models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'other')])),
                ('address', models.CharField(max_length=200)),
                ('hpURL', models.URLField()),
            ],
        ),
        
    ]