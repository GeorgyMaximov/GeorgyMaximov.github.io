import argparse
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    parser = argparse.ArgumentParser()
    parser.add_argument('--books_info_path', default='.')
    args = parser.parse_args()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    
    row_number = 5
    books_in_row = 2
    with open(f'{args.books_info_path}/books_info.json', 'r', encoding='utf8') as file:
        book_row = list(chunked(json.load(file), books_in_row))

    books_info = list(chunked(book_row, row_number))
    for page_number, page_books in enumerate(books_info):
        rendered_page = template.render(page_books=page_books, page=page_number, page_number=len(books_info))
        with open(f'pages/index{page_number}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()