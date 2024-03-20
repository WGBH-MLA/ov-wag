# Generated by Django 4.1.2 on 2022-10-13 18:14

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('ov_collections', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='content',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title')), ('text', wagtail.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('Interviews', wagtail.blocks.StructBlock([('interviews', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('interview', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='The title of this content', max_length=1024, required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('link', wagtail.blocks.URLBlock(required=True))]))])))]))], use_json_field=True),
        ),
    ]