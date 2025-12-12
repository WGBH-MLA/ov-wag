import django

django.setup()
from wagtail.models import Page

ov = Page.objects.get(id=3)
aapb = Page.objects.get(id=59)

from cmless.models import Collection
import json
from aapb_collections.models import AAPBCollection, AAPBRecordsBlock
import re
from typing import List, Dict


def markdownify(text: str) -> str:
    """
    Converts markdown text to HTML string
    """
    from markdown import markdown

    return str(markdown(text))


def parse_cmless_thumbnail(markdown_string: str) -> List[Dict[str, str]]:
    """
    Parse a markdown string containing cmless images into a list of objects.

    Args:
        markdown_string (str): The markdown string to parse

    Returns:
        List[Dict[str, str]]: List of dictionaries with 'title' and 'image_url' keys
    """
    # Pattern to match ![title](url)
    pattern = r'\!\[([^\]]*)\]\(([^\)]*)\)'
    matches = re.findall(pattern, markdown_string)

    cmless_images = []
    for match in matches:
        title, url = match
        cmless_images.append({'title': title.strip(), 'url': url.strip().split(' ')[0]})

    return cmless_images


def parse_featured_markdown(markdown_string: str) -> List[Dict[str, str]]:
    """
    Parse a markdown string containing featured items into a list of objects.

    Expected format: [![title](image_url)](link_url)

    Args:
        markdown_string (str): The markdown string to parse

    Returns:
        List[Dict[str, str]]: List of dictionaries with 'title', 'image_url', and 'link_url' keys
    """
    # Pattern to match [![title](image_url)](link_url)
    pattern = r'\[\!\[([^\]]*)\]\(([^\)]*)\)\]\(([^\)]*)\)'

    matches = re.findall(pattern, markdown_string)

    featured_items = []
    for match in matches:
        title, image_url, link_url = match
        guid = link_url.split('/')[-1].split('#')[0]  # Extract guid from link_url
        start_time = link_url.split('#at_')[-1] if '#at_' in link_url else None
        featured_items.append(
            {
                'title': title.strip(),
                # 'thumbnail': image_url.strip(),
                'guids': guid.strip(),
                'start_time': (
                    start_time.strip().replace('_s', '') if start_time else None
                ),
            }
        )

    return featured_items


from wagtail.images.models import Image


def download_image(url: str, title: str | None = None) -> Image | None:
    import requests
    from django.core.files.base import ContentFile
    from wagtail.images import get_image_model

    ImageModel = get_image_model()
    response = requests.get(url)
    if not title:
        title = url.split("/")[-1]
    if response.status_code == 200:
        image = Image(file=ContentFile(response.content, name=title), title=title)
        image.save()
        return image
    else:
        print(f"Failed to download image from {url}")
        return None


from aapb_collections.models import AAPBCollection


def create_collection_page(collection):
    if collection.funders:
        funders = ''
        for funder in parse_cmless_thumbnail(collection.funders.strip()):
            image = (
                download_image(funder['url'], title=funder['title']) if funder else None
            )
            if image:
                funders += f'<embed alt="{funder["title"]}" embedtype="image" format="fullwidth" id="{image.id}"/>'
    content = [
        (
            ('background', markdownify(collection.background))
            if collection.background
            else None
        ),
        ('help', markdownify(collection.help)) if collection.help else None,
        (
            ('resources', markdownify(collection.resources))
            if collection.resources
            else None
        ),
        ('terms', markdownify(collection.terms)) if collection.terms else None,
        ('timeline', markdownify(collection.timeline)) if collection.timeline else None,
        ('funders', funders) if 'funders' in locals() else None,
    ]
    content = [item for item in content if item is not None]
    if collection.sort:
        sort = collection.sort.split('+')
        sort_by = sort[0] if len(sort) > 0 else None
        if sort_by == 'asset_date':
            sort_by = 'date'
        elif sort_by == 'asset_title':
            sort_by = 'title'
        sort_order = sort[1] if len(sort) > 1 else None
    if collection.featured:
        featured = parse_featured_markdown(collection.featured)
        featured_items = [('records', record) for record in featured]
    if collection.title.find('<em>') != -1 or collection.title.find('*') != -1:
        display_title = collection.title
        title = (
            collection.title.replace('<em>', '').replace('</em>', '').replace('*', '')
        )

    if collection.thumbnail:
        image = parse_cmless_thumbnail(collection.thumbnail)[0]
        thumbnail = (
            download_image(
                image['url'], title=title if 'title' in locals() else image['title']
            )
            if image
            else None
        )

    # return content
    page = AAPBCollection(
        title=title if 'title' in locals() else collection.title,
        display_title=(
            markdownify(display_title) if 'display_title' in locals() else None
        ),
        introduction=markdownify(collection.summary),
        content=content,
        featured_items=featured_items if 'featured_items' in locals() else None,
        sort_by=sort_by if 'sort_by' in locals() else None,
        sort_order=sort_order if 'sort_order' in locals() else None,
        hero_image=thumbnail if 'thumbnail' in locals() else None,
    )
    return page


if __name__ == '__main__':
    with open('collections.json') as f:
        data = json.load(f)
        collections = [Collection(**item) for item in data]

    for collection in collections:
        page = create_collection_page(collection)
        print(f"Creating collection: {page}")
        aapb.add_child(instance=page)
        print(f"Added collection: {collection.title}")
