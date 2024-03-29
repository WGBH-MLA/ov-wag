# Generated by Django 4.1.12 on 2023-10-30 19:42

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('ov_collections', '0007_rename_about_collection_introduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='content',
            field=wagtail.fields.StreamField([('interviews', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))], icon='openquote', label='Interview'), icon='openquote')), ('archival_footage', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))], icon='form', label='Footage'), icon='form')), ('photographs', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))], icon='image', label='Photograph'), icon='image')), ('original_footage', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))], icon='doc-full-inverse', label='Footage'), icon='doc-full-inverse')), ('programs', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True))], icon='clipboard-list', label='Program'), icon='clipboard-list')), ('related_content', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True))], icon='list-ul', label='Content'), icon='list-ul')), ('credits', wagtail.blocks.RichTextBlock()), ('heading', wagtail.blocks.CharBlock(form_classname='title')), ('text', wagtail.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=True),
        ),
    ]
