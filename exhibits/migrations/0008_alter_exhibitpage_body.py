# Generated by Django 4.2.10 on 2024-02-07 23:27

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail_footnotes.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("exhibits", "0007_alter_exhibitpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exhibitpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("text", wagtail_footnotes.blocks.RichTextBlockWithFootnotes()),
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