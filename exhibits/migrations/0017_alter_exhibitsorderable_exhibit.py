# Generated by Django 5.1.4 on 2024-12-16 23:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exhibits", "0016_alter_exhibitpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exhibitsorderable",
            name="exhibit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="exhibits.exhibitpage"
            ),
        ),
    ]
