from wagtail.snippets.widgets import AdminSnippetChooser
from wagtail.images.models import SourceImageIOError
from contextlib import suppress


class AdminAuthorChooser(AdminSnippetChooser):
    """Custom Author chooser widget with avatar display"""

    template_name = 'authors/widgets/author_chooser.html'

    def __init__(self, **kwargs):
        # Import here to avoid circular imports
        from .models import Author  # noqa: PLC0415

        # Allow model to be passed in (for viewset usage) or default to Author
        model = kwargs.pop('model', Author)
        super().__init__(model=model, **kwargs)

    def get_value_data_from_instance(self, instance):
        """Include extra data about the author for the widget template"""
        data = super().get_value_data_from_instance(instance)
        data['author_title'] = instance.title or ''
        data['image_url'] = None
        if instance.image:
            with suppress(SourceImageIOError):
                # TODO: Log error or handle missing image file as needed
                data['image_url'] = instance.image.get_rendition('fill-40x40').url
        return data

    def get_context(self, name, value_data, attrs):
        """Override to pass extra author data to the template"""
        context = super().get_context(name, value_data, attrs)
        # Add our custom fields from value_data to the template context
        context['image_url'] = value_data.get('image_url')
        context['author_title'] = value_data.get('author_title', '')
        return context
