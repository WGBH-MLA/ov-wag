from .views import author_chooser_viewset

AuthorChooserBlock = author_chooser_viewset.get_block_class(
    name='AuthorChooserBlock', module_path='authors.blocks'
)
