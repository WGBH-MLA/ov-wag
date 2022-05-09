from django.db import models
from wagtail.api import APIField
from wagtail.core.fields import RichTextField


class Author(models.Model):
    """Author of a page"""

    name = models.CharField(max_length=100, help_text='Author name')
    # email = models.CharField(max_length=100, blank=True, help_text='author email')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    bio = RichTextField(blank=True, help_text='Brief author bio')

    api_fields = [
        APIField('name'),
        APIField('image'),
        APIField('bio'),
    ]

    def __str__(self):
        """str representation of this Author"""
        return self.name
