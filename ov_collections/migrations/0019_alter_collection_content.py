# Generated by Django 5.1.4 on 2025-01-14 21:23

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ov_collections", "0018_alter_collection_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="content",
            field=wagtail.fields.StreamField(
                [
                    ("interviews", 9),
                    ("archival_footage", 10),
                    ("photographs", 11),
                    ("original_footage", 12),
                    ("programs", 13),
                    ("related_content", 14),
                    ("credits", 15),
                    ("heading", 16),
                    ("text", 17),
                    ("html", 18),
                ],
                block_lookup={
                    0: (
                        "wagtail.blocks.TextBlock",
                        (),
                        {
                            "help_text": "AAPB record IDs, separated by whitespace",
                            "required": True,
                        },
                    ),
                    1: (
                        "wagtail.blocks.TextBlock",
                        (),
                        {"help_text": "Special collections IDs", "required": False},
                    ),
                    2: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "default": True,
                            "help_text": "Show asset title(s) for this block",
                            "required": False,
                        },
                    ),
                    3: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "default": True,
                            "help_text": "Show asset thumbnail(s) for this block",
                            "required": False,
                        },
                    ),
                    4: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "default": True,
                            "help_text": "Include title in sidebar",
                            "required": False,
                        },
                    ),
                    5: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": ["italic"],
                            "help_text": "The title of this group",
                            "max_length": 1024,
                            "required": False,
                        },
                    ),
                    6: (
                        "ov_collections.blocks.DurationBlock",
                        (),
                        {"help_text": "Start time for the group", "required": False},
                    ),
                    7: (
                        "ov_collections.blocks.DurationBlock",
                        (),
                        {"help_text": "End time for the group", "required": False},
                    ),
                    8: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("all", "All"),
                                ("digitized", "Digitized"),
                                ("online", "Online"),
                            ],
                            "help_text": "Access level for AAPB search links in this block",
                        },
                    ),
                    9: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("guids", 0),
                                ("special_collections", 1),
                                ("show_title", 2),
                                ("show_thumbnail", 3),
                                ("show_sidebar", 4),
                                ("title", 5),
                                ("start_time", 6),
                                ("end_time", 7),
                                ("access_level", 8),
                            ]
                        ],
                        {"icon": "openquote", "label": "Interviews"},
                    ),
                    10: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("guids", 0),
                                ("special_collections", 1),
                                ("show_title", 2),
                                ("show_thumbnail", 3),
                                ("show_sidebar", 4),
                                ("title", 5),
                                ("start_time", 6),
                                ("end_time", 7),
                                ("access_level", 8),
                            ]
                        ],
                        {"icon": "clipboard-list", "label": "Archival Footage"},
                    ),
                    11: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("guids", 0),
                                ("special_collections", 1),
                                ("show_title", 2),
                                ("show_thumbnail", 3),
                                ("show_sidebar", 4),
                                ("title", 5),
                                ("start_time", 6),
                                ("end_time", 7),
                                ("access_level", 8),
                            ]
                        ],
                        {"icon": "copy", "label": "Photographs"},
                    ),
                    12: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("guids", 0),
                                ("special_collections", 1),
                                ("show_title", 2),
                                ("show_thumbnail", 3),
                                ("show_sidebar", 4),
                                ("title", 5),
                                ("start_time", 6),
                                ("end_time", 7),
                                ("access_level", 8),
                            ]
                        ],
                        {"icon": "doc-full-inverse", "label": "Original Footage"},
                    ),
                    13: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("guids", 0),
                                ("special_collections", 1),
                                ("show_title", 2),
                                ("show_thumbnail", 3),
                                ("show_sidebar", 4),
                                ("title", 5),
                                ("start_time", 6),
                                ("end_time", 7),
                                ("access_level", 8),
                            ]
                        ],
                        {"icon": "desktop", "label": "Programs"},
                    ),
                    14: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("guids", 0),
                                ("special_collections", 1),
                                ("show_title", 2),
                                ("show_thumbnail", 3),
                                ("show_sidebar", 4),
                                ("title", 5),
                                ("start_time", 6),
                                ("end_time", 7),
                                ("access_level", 8),
                            ]
                        ],
                        {"icon": "table", "label": "Related Content"},
                    ),
                    15: ("wagtail.blocks.RichTextBlock", (), {"icon": "form"}),
                    16: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": ["italic"],
                            "form_classname": "title",
                            "icon": "title",
                        },
                    ),
                    17: ("wagtail.blocks.RichTextBlock", (), {}),
                    18: ("wagtail.blocks.RawHTMLBlock", (), {"label": "HTML"}),
                },
            ),
        ),
    ]
