# Generated by Django 3.2.9 on 2021-11-29 15:36

from django.db import migrations

from wagtail import fields


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=fields.RichTextField(blank=True),
        ),
    ]
