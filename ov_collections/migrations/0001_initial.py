# Generated by Django 4.1.2 on 2022-10-06 20:24

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('wagtailcore', '0077_alter_revision_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('about', wagtail.fields.RichTextField(blank=True)),
                ('content', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title')), ('text', wagtail.blocks.TextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=True)),
                ('cover_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
