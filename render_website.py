import json
import os
import glob
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from math import ceil

json_directory = 'media'
catalog_name = 'books_catalog.json'
pages_directory = Path('pages')
files_catalog = set()

os.makedirs(pages_directory, exist_ok=True)


def get_catalog(directory, file_name):
    catalog_directory = os.path.join(directory, file_name)
    with open(catalog_directory, 'r') as file:
        catalog_file = file.read()
        books_catalog = json.loads(catalog_file)
        return books_catalog


def remove_old_files(files_catalog, files_in_directory):
    for file in files_in_directory:
        if str(file) not in files_catalog:
            os.remove(file)


def on_reload():
    books_on_page = 20
    files_in_directory = pages_directory.glob('*.html')

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    books_catalog = get_catalog(json_directory, catalog_name)
    pages = chunked(books_catalog, books_on_page)
    all_pages = list(pages)
    pages_count = len(all_pages)

    for page_num, page in enumerate(all_pages, 1):
        half_page = len(page) / 2
        first_catalog, second_catalog = chunked(page, ceil(half_page))

        rendered_page = template.render(
            first_books=first_catalog,
            second_books=second_catalog,
            pages_count=pages_count,
            current_page=page_num,
        )

        file_name = f'index{page_num}.html'
        index_directory = os.path.join(pages_directory, file_name)
        files_catalog.add(index_directory)

        with open(index_directory, 'w', encoding="utf8") as file:
            file.write(rendered_page)

    remove_old_files(files_catalog, files_in_directory)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
