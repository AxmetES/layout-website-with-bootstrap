from livereload import Server, shell
import json
import os
import urllib
from urllib.parse import urlencode
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

directory = 'dest_folder/json'
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

    for num, page in enumerate(pages):
        first_catalog, second_catalog = chunked(page, 10)
        rendered_page = template.render(
            first_books=first_catalog,
            second_books=second_catalog,
        )
        index_directory = os.path.join(pages_directory, f'index{num}.html')
        with open(index_directory, 'w', encoding="utf8") as file:
            file.write(rendered_page)
        print('site rebuilded')


on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
