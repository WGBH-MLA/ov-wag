# Generated by Django 4.1.2 on 2022-10-19 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ov_collections', '0006_alter_collection_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='about',
            new_name='introduction',
        ),
    ]