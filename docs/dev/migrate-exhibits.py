# %%
import django

django.setup()
from wagtail.models import Page

ov = Page.objects.get(id=3)
aapb = Page.objects.get(id=59)

# %%
import json

with open('exhibits.json') as f:
    exhibits = json.load(f)
len(exhibits)

# %%
from cmless.models import Exhibit

exhibits = [Exhibit(**exhibit) for exhibit in exhibits]

# %%
pages = 0
for exhibit in exhibits:
    # print(exhibit.title, len(exhibit.children))
    pages += len(exhibit.children)
    # for n, p in enumerate(exhibit.children):
    # print(f'  {n+1}: {p.title} - {p.page}')

pages

# %%
from wagtail.images.models import Image


# TODO: standardize image download function across migrate scripts
def download_image(
    url: str, title: str | None = None, alt: str | None = None
) -> Image | None:
    import requests
    from django.core.files.base import ContentFile
    from wagtail.images import get_image_model

    ImageModel = get_image_model()
    response = requests.get(url)
    if not title:
        title = url.split("/")[-1]
    if response.status_code == 200:
        image = Image(
            file=ContentFile(response.content, name=title),
            title=title,
            description=alt[:255] if alt else '',
        )
        image.save()
        return image
    else:
        print(f"Failed to download image from {url}")
        return None


# %%
from cmless.parse import (
    parse_cmless_thumbnail,
    parse_records_markdown,
    pasre_authors_markdown,
    markdownify,
)

from bs4 import BeautifulSoup


# %%
def extract_subheadings(md: str) -> list[tuple[str, str]]:
    # First split by main headings (###)
    main_heading_pattern = r'###\s+(.+?)\s*\n'
    main_parts = split(main_heading_pattern, md)

    if len(main_parts) == 1:
        return [('text', markdownify(md))]

    sections = []
    # Skip the first element (content before any heading) and pair up headings with content
    for i in range(1, len(main_parts), 2):
        if i < len(main_parts) - 1:
            heading = main_parts[i].strip()
            content = main_parts[i + 1].strip()

            if not content:
                continue

            # Add the main heading
            sections.append(('heading', markdownify(heading)))

            # Now check if this content has subheadings (####)
            subheading_pattern = r'####\s+([^\n]+)'
            sub_parts = split(subheading_pattern, content)

            # If there are subheadings, parse them
            if len(sub_parts) > 1:
                # First part is text before any subheading
                main_text = sub_parts[0].strip()
                if main_text:
                    sections.append(('text', markdownify(main_text)))

                # Parse subheading pairs
                for j in range(1, len(sub_parts), 2):
                    sub_heading = sub_parts[j].strip()
                    sections.append(('subheading', markdownify(sub_heading)))
                    # Check if there's content after this subheading
                    if j + 1 < len(sub_parts):
                        sub_text = sub_parts[j + 1].strip()
                        if sub_text:
                            sections.append(('text', markdownify(sub_text)))
            else:
                # No subheadings, just add the content as text
                sections.append(('text', markdownify(content)))
    return sections


# %%
from aapb_exhibits.models import AAPBExhibit, AAPBExhibitsChildOrder
from authors.models import Author, AAPBAuthorsOrderable
from re import split


def create_exhibit_page(exhibit: Exhibit) -> AAPBExhibit:

    body = []
    if exhibit.main:
        body += extract_subheadings(exhibit.main)
    if exhibit.extended:
        body += extract_subheadings(exhibit.extended)
    if exhibit.resources:
        body.append(('heading', 'Resources'))
        body.append(('text', markdownify(exhibit.resources)))
    if exhibit.records:
        records = parse_records_markdown(exhibit.records)
        if records:
            # body.append(('heading', 'Records'))
            body.append(('records', {'guids': '\n'.join(records)}))

    if exhibit.title.find('<em>') >= 0 or exhibit.title.find('*') >= 0:
        display_title = markdownify(exhibit.title)
    title = exhibit.title.replace('<em>', '').replace('</em>', '').replace('*', '')

    if exhibit.cover:
        cover = BeautifulSoup(exhibit.cover)
        if cover.img:
            cover_image = download_image(
                url=cover.img.get('src'),
                title=cover.img.get('title', exhibit.title),
                alt=cover.img.get('alt'),
            )
    page = AAPBExhibit(
        title=title,
        display_title=(display_title if 'display_title' in locals() else None),
        slug=exhibit.slug,
        introduction=markdownify(exhibit.summary) if exhibit.summary else '',
        body=body,
        cover_image=(cover_image if 'cover_image' in locals() else None),
        # gallery = exhibit.gallery,
    )
    if exhibit.authors:
        authors_markdown = pasre_authors_markdown(exhibit.authors)
        authors = []
        for author in authors_markdown:
            author_obj, created = Author.objects.get_or_create(name=author.name)
            if created:
                author_obj.title = author.title
                if author.image:
                    author_obj.image = download_image(
                        url=author.image,
                        title=author.name,
                        alt=author.name,
                    )
                # author_obj.bio =
                author_obj.save()
            author_ord = AAPBAuthorsOrderable(
                author=author_obj,
                page=page,
            )
            authors.append(author_ord)

        page.authors.set(authors)
    return page


# %%
# Debug: Show the actual content being split
for exhibit in exhibits:
    if '####' in exhibit.main:
        print(f"Exhibit: {exhibit.title}\n")

        from re import split

        main_heading_pattern = r'###\s+(.+?)\s*\n'
        main_parts = split(main_heading_pattern, exhibit.main)

        # Check the Acknowledgements section specifically
        for i in range(1, len(main_parts), 2):
            if i < len(main_parts) - 1:
                heading = main_parts[i].strip()
                if 'Acknowledge' in heading:
                    content = main_parts[i + 1]
                    print(f"Section: {heading}")
                    print(f"Content (last 300 chars):\n{content[-300:]}")
                    print("\n" + "=" * 80)

                    # Try splitting
                    subheading_pattern = r'####\s+([^\n]+)\n'
                    sub_parts = split(subheading_pattern, content)
                    print(f"\nSplit into {len(sub_parts)} parts:")
                    for j, part in enumerate(sub_parts):
                        print(f"\n[{j}] ({'HEADING' if j % 2 == 1 else 'TEXT'}):")
                        print(repr(part[:150]) if part else "(empty)")
        break

# %%
for exhibit in exhibits:
    print(f'Creating exhibit: {exhibit.title}')
    page = create_exhibit_page(exhibit)
    aapb.add_child(instance=page)
    page.save_revision().publish()
    child_pages = []
    for child in exhibit.children:
        print(f'  Creating child page {child.page}: {child.title}')
        child_page = create_exhibit_page(child)
        page.add_child(instance=child_page)
        child_page.save_revision().publish()
        # Add child order entry
        child_order_entry = AAPBExhibitsChildOrder(
            exhibit=child_page,
            page=page,
        )
        child_pages.append(child_order_entry)
    page.child_order.set(child_pages)
    page.save_revision().publish()
