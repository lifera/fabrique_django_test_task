# Generated by Django 2.2.10 on 2021-02-09 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='poll',
            name='start_date',
            field=models.DateField(auto_now=True),
        ),
    ]
