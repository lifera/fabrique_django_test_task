# Generated by Django 2.2.10 on 2021-02-10 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_answer_answer_text'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('question', 'answered_by')},
        ),
    ]
