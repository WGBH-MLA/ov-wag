# Generated by Django 4.1.2 on 2022-10-14 21:56

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('ov_collections', '0003_alter_collection_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='content',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title')), ('text', wagtail.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('interviews', wagtail.blocks.StructBlock([('interviews', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('interview', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))])), ('archival_footage', wagtail.blocks.StructBlock([('footage', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('footage', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))])), ('photographs', wagtail.blocks.StructBlock([('photos', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('photos', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))])), ('original_footage', wagtail.blocks.StructBlock([('footage', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('footage', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))])), ('programs', wagtail.blocks.StructBlock([('programs', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('programs', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))])), ('related_content', wagtail.blocks.StructBlock([('content', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('related_content', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))])), ('credits', wagtail.blocks.StructBlock([('credits', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('credits', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))]))], use_json_field=True),
        ),
    ]