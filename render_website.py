import json
import os
from urllib.parse import quote, quote_from_bytes, urlencode, quote_plus

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from math import ceil

directory = 'media'
file_name = 'books_catalog.json'
pages_directory = 'pages'

os.makedirs(pages_directory, exist_ok=True)


def get_catalog(directory, file_name):
    catalog_directory = os.path.join(directory, file_name)
    with open(catalog_directory, 'r') as file:
        catalog_file = file.read()
        books_catalog = json.loads(catalog_file)
        return books_catalog


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    books_catalog = get_catalog(directory, file_name)
    pages = chunked(books_catalog, 20)
    all_pages = list(pages)
    site_pages = len(all_pages)

    for page_num, page in enumerate(all_pages, 1):
        half_page = len(page) / 2
        first_catalog, second_catalog = chunked(page, ceil(half_page))

        rendered_page = template.render(
            first_books=first_catalog,
            second_books=second_catalog,
            all_pages=site_pages,
            current_page=page_num,

        )
        index_directory = os.path.join(pages_directory, f'index{page_num}.html')
        with open(index_directory, 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
