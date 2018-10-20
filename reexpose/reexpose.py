#! /usr/bin/env python3

from flask import Flask
from gevent.pywsgi import WSGIServer

VER = 1.0

def app_setup():
    app = Flask(__name__)

    @app.route('/')
    def info():
        return 'ReExpose version {}'.format(VER)

    return app

if __name__ == '__main__':
    app = app_setup()
    WSGIServer(('127.0.0.1', 5000), app).serve_forever()
