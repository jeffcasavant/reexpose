''' ReExpose HTTP basic auth endpoints as unauthenticated ones on localhost '''

#! /usr/bin/env python3

import pdb

import argparse
import logging

import requests
from flask import Flask, Response
from gevent.pywsgi import WSGIServer
from yaml import safe_load

def load_config(config_file):

    ''' Load config from open file handle '''

    config = safe_load(config_file)
    logging.info('Sites loaded: %d', len(config))
    return config

def app_setup(**kwargs):

    ''' Create endpoints based on config file. '''

    app = Flask(__name__)

    @app.route('/')
    def info():
        # pylint: disable=unused-variable
        return 'ReExpose'

    config = load_config(kwargs['config'])

    @app.route('/sites/<site_name>')
    def render_site(site_name):
        site = config['sites'].get(site_name, None)

        if not site:
            logging.warn('Request for nonexistent site %s', site_name)
            return 'Site not found: {}'.format(site_name), 404

        url = site['url']
        creds = (site['creds']['user'],
                 site['creds']['pass'])

        resp = requests.get(url, auth=creds)

        flask_resp = Response(resp.text)
        flask_resp.headers = {**flask_resp.headers,
                              **resp.headers}

        return flask_resp, resp.status_code

    logging.info('Setup complete')
    return app

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='ReExpose HTTP basic auth endpoints as unauthenticated ones')
    parser.add_argument('--config', '-c', type=argparse.FileType('r'), help='Config file')
    parser.add_argument('--port', '-p', type=int, help='Port to listen on', default=5000)
    args = parser.parse_args()

    app = app_setup(**vars(args))
    logging.info('Starting app')
    WSGIServer(('127.0.0.1', args.port), app).serve_forever()
