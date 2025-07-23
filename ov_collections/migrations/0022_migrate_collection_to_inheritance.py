# Migration to add collectionpage_ptr field to Collection model
# Data migration was performed manually via SQL

import django.db.models.deletion
from django.db import migrations, models


def populate_collectionpage_ptr(apps, schema_editor):
    """
    Populate the collectionpage_ptr field with existing page_ptr values.
    This assumes CollectionPage records already exist from manual migration.
    """
    with schema_editor.connection.cursor() as cursor:
        # Update collection to point to the CollectionPage using the same ID
        cursor.execute(
            """
            UPDATE ov_collections_collection 
            SET collectionpage_ptr_id = page_ptr_id 
            WHERE collectionpage_ptr_id IS NULL
            """
        )

        print("Updated collectionpage_ptr fields")


def reverse_populate_collectionpage_ptr(apps, schema_editor):
    """
    Reverse the population by setting collectionpage_ptr to NULL.
    """
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE ov_collections_collection 
            SET collectionpage_ptr_id = NULL
            """
        )


class Migration(migrations.Migration):

    dependencies = [
        ("ov_collections", "0021_add_collection_page_model"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        # Step 1: Add collectionpage_ptr field as nullable
        migrations.AddField(
            model_name="collection",
            name="collectionpage_ptr",
            field=models.OneToOneField(
                auto_created=True,
                null=True,  # Allow null temporarily
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                serialize=False,
                to="ov_collections.collectionpage",
            ),
        ),
        # Step 2: Populate the collectionpage_ptr field
        migrations.RunPython(
            populate_collectionpage_ptr,
            reverse_populate_collectionpage_ptr,
        ),
    ]
