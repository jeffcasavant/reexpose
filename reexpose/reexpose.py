#! /usr/bin/env python3

import logging
import os
import sys

import requests
from flask import Flask, Response
from gevent.pywsgi import WSGIServer
from yaml import safe_load

def load_config():

    config_file = 'config.yaml'
    if len(sys.argv) > 1:
        config_file = os.path.join(os.getcwd(),
                                   sys.argv[1])

    logging.info('Loading config from %s', config_file)
    with open(config_file) as config:
        config = safe_load(config)
        logging.info('Loaded %d sites', len(config))
        return config

def app_setup():
    app = Flask(__name__)

    @app.route('/')
    def info():
        return 'ReExpose'

    config = load_config()

    for site in config['sites']:
        logging.info('Setting up endpoint for %s', site['name'])
        @app.route('/{}'.format(site.get('endpoint', site['name'])))
        def render_site():
            resp = requests.get(site['url'],
                                auth=(site['creds']['user'],
                                      site['creds']['pass']))

            flask_resp = Response(resp.text)
            flask_resp.headers = {**flask_resp.headers,
                                  **resp.headers}

            return flask_resp, resp.status_code

    logging.info('Setup complete')
    return app

def main():
    logging.basicConfig(level=logging.DEBUG)

    app = app_setup()
    logging.info('Starting app')
    WSGIServer(('127.0.0.1', 5000), app).serve_forever()
