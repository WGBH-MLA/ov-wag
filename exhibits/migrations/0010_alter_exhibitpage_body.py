# Generated by Django 4.2.10 on 2024-02-07 23:44

from django.db import migrations
import exhibits.models
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("exhibits", "0009_alter_exhibitpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exhibitpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("text", exhibits.models.RichTextFootnotesBlock()),
                    (
                        "heading",
                        wagtail.blocks.RichTextBlock(
                            features=["italic"], form_classname="title", icon="title"
                        ),
                    ),
                    (
                        "subheading",
                        wagtail.blocks.RichTextBlock(
                            features=["italic"], form_classname="title", icon="title"
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
