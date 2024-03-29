# Generated by Django 4.1.2 on 2022-10-17 18:54

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('ov_collections', '0004_alter_collection_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='content',
            field=wagtail.fields.StreamField([('interviews', wagtail.blocks.StructBlock([('interviews', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('interview', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))]))])))])), ('archival_footage', wagtail.blocks.StructBlock([('footage', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('footage', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))]))])))])), ('photographs', wagtail.blocks.StructBlock([('photos', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('photos', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))]))])))])), ('original_footage', wagtail.blocks.StructBlock([('footage', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('footage', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))]))])))])), ('programs', wagtail.blocks.StructBlock([('programs', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('programs', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))])), ('related_content', wagtail.blocks.StructBlock([('content', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('related_content', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))])), ('credits', wagtail.blocks.RichTextBlock()), ('heading', wagtail.blocks.CharBlock(form_classname='title')), ('text', wagtail.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=True),
        ),
    ]
