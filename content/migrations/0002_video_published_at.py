# Generated by Django 4.1.3 on 2022-11-29 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
