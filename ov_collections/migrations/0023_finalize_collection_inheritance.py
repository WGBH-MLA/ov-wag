# Complete the Collection inheritance by making collectionpage_ptr the primary key
# and removing duplicate fields

import django.db.models.deletion
from django.db import migrations, models


def make_collectionpage_ptr_primary_key(apps, schema_editor):
    """
    Use raw SQL to properly handle primary key transition.
    """
    with schema_editor.connection.cursor() as cursor:
        # First, make collectionpage_ptr non-nullable
        cursor.execute(
            """
            ALTER TABLE ov_collections_collection 
            ALTER COLUMN collectionpage_ptr_id SET NOT NULL
            """
        )

        # Drop the existing primary key constraint
        cursor.execute(
            """
            ALTER TABLE ov_collections_collection 
            DROP CONSTRAINT ov_collections_collection_pkey
            """
        )

        # Add the new primary key constraint
        cursor.execute(
            """
            ALTER TABLE ov_collections_collection 
            ADD PRIMARY KEY (collectionpage_ptr_id)
            """
        )

        print("Updated primary key to collectionpage_ptr_id")


def reverse_primary_key_change(apps, schema_editor):
    """
    Reverse the primary key change.
    """
    with schema_editor.connection.cursor() as cursor:
        # Drop the collectionpage_ptr primary key
        cursor.execute(
            """
            ALTER TABLE ov_collections_collection 
            DROP CONSTRAINT ov_collections_collection_pkey
            """
        )

        # Restore the page_ptr primary key
        cursor.execute(
            """
            ALTER TABLE ov_collections_collection 
            ADD PRIMARY KEY (page_ptr_id)
            """
        )

        # Make collectionpage_ptr nullable again
        cursor.execute(
            """
            ALTER TABLE ov_collections_collection 
            ALTER COLUMN collectionpage_ptr_id DROP NOT NULL
            """
        )


class Migration(migrations.Migration):

    dependencies = [
        ("ov_collections", "0022_migrate_collection_to_inheritance"),
    ]

    operations = [
        # Use raw SQL to handle primary key transition
        migrations.RunPython(
            make_collectionpage_ptr_primary_key,
            reverse_primary_key_change,
        ),
        # Remove the duplicate fields from Collection (they now exist in CollectionPage)
        migrations.RemoveField(
            model_name="collection",
            name="cover_image",
        ),
        migrations.RemoveField(
            model_name="collection",
            name="featured",
        ),
        migrations.RemoveField(
            model_name="collection",
            name="hero_image",
        ),
        migrations.RemoveField(
            model_name="collection",
            name="introduction",
        ),
        migrations.RemoveField(
            model_name="collection",
            name="page_ptr",
        ),
    ]
