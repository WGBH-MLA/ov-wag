from django.shortcuts import redirect
from wagtail import hooks
from wagtail.admin import messages


@hooks.register('before_publish_page')
def before_publish_page(request, page):
    # Ensure Exhibits and Collections have a cover image and hero image
    page_type = page.content_type.name
    print('before_publish_page', request, page, page_type)
    error = False
    if page_type in ('exhibit page', 'collection page'):
        if not page.cover_image:
            messages.error(request, f'{page_type} must have a cover image')
            error = True

        if not page.hero_image:
            messages.error(request, f'{page_type} must have a hero image')
            error = True
        if error:
            messages.error(request, 'Error publishing page')
            return redirect('wagtailadmin_pages:edit', page.id)
    return None
