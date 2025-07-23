# Generated manually to handle model inheritance split

import django.db.models.deletion
import wagtail.fields
import wagtail_headless_preview.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ov_collections", "0020_collection_featured"),
        ("wagtailcore", "0094_alter_page_locale"),
        ("wagtailimages", "0027_image_description"),
    ]

    operations = [
        # First, create the CollectionPage model
        migrations.CreateModel(
            name="CollectionPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("introduction", wagtail.fields.RichTextField(blank=True)),
                ("featured", models.BooleanField(default=False)),
                (
                    "cover_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "hero_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail_headless_preview.models.HeadlessMixin, "wagtailcore.page"),
        ),
    ]
