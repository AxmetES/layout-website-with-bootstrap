import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

directory = 'dest_folder/json'
file_name = 'books_catalog.json'


def get_catalog(directory, file_name):
    catalog_directory = os.path.join(directory, file_name)
    with open(catalog_directory, 'r') as file:
        catalog_file = file.read()
        books_catalog = json.loads(catalog_file)
        return books_catalog


books_catalog = get_catalog(directory, file_name)


rendered_page = template.render(
    books=books_catalog,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
