from pydoc import html
import os
from flask import Flask, request, session

app = Flask(__name__)

# Инициализация сессии
app.secret_key = 'your_secret_key'


def route(route, path_to_include, methods=None):
    if methods is None:
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    if request.method in methods:
        callback = path_to_include
        if not callable(callback):
            if not path_to_include.endswith('.py'):
                path_to_include += '.py'

            if route == "/404":
                return app.send_static_file(path_to_include)

        request_url = request.path
        route_parts = route.strip('/').split('/')
        request_url_parts = request_url.strip('/').split('/')

        if len(route_parts) != len(request_url_parts):
            return

        parameters = {}

        for i in range(len(route_parts)):
            route_part = route_parts[i]

            if route_part.startswith('$'):
                route_part = route_part[1:]
                parameters[route_part] = request_url_parts[i]

        if callable(callback):
            return callback(**parameters)
        else:
            return app.send_static_file(path_to_include)


def out(text):
    return html.escape(text)


@app.route('/set_csrf')
def set_csrf():
    if 'csrf' not in session:
        session['csrf'] = os.urandom(32).hex()
    return '<input type="hidden" name="csrf" value="{}">'.format(session['csrf'])


@app.route('/is_csrf_valid', methods=['POST'])
def is_csrf_valid():
    if 'csrf' not in session or 'csrf' not in request.form:
        return 'false'
    if session['csrf'] != request.form['csrf']:
        return 'false'
    return 'true'


if __name__ == '__main__':
    app.run()