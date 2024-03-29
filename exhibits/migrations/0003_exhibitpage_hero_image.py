# Generated by Django 4.0.4 on 2022-05-12 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('exhibits', '0002_exhibitpage_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitpage',
            name='hero_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
