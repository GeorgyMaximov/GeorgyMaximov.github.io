from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('result/books_info.json', 'r', encoding='utf8') as file:
        books_info = file.read()

    books_info = list(chunked(list(chunked(json.loads(books_info), 2)), 5))

    for page, books_info in enumerate(books_info):
        rendered_page = template.render(books_info=books_info, page=page, page_number=len(books_info)*2)
        with open(f'pages/index{page}.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index0.html')


if __name__ == '__main__':
    main()