# Generated by Django 5.1.5 on 2025-02-07 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ov_collections", "0019_alter_collection_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="featured",
            field=models.BooleanField(default=False),
        ),
    ]
