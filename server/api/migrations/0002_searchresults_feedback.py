# Generated by Django 3.1.3 on 2020-11-10 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresults',
            name='feedback',
            field=models.IntegerField(null=True),
        ),
    ]