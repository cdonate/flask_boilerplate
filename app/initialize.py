# -*- coding: utf-8 -*-
import json
import os
import datetime

from flask import Flask, g, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from app import config as config_module
from app import api, database

config = config_module.get_config()

web_app = Flask(__name__)
web_app.config.from_object(config)
database.AppRepository.db = SQLAlchemy(web_app)

api.create_api(web_app)


@web_app.before_request
def before_request():
    # TODO: Aqui precisaremos ir no módulo de validação para fazer isso
    # Imagino que outros micro serviços também precisarão. Poderiamos jogar isso num pypi privado nosso
    # mas por hora imagino que seria bacana tomar o cuidado de fazer isso de maneira beeeem isolada, para futuramente
    # ser um ctrl+c ctrl+v
    pass


@web_app.after_request
def add_cache_header(response):
    """
    Add response headers for Cache Control
    """
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@web_app.after_request
def add_token_header(response):
    # TODO: ver se vai precisar de alguma coisa aqui
    return response


# If you want to serve your files using python
# Only use it for development
# if config.ENVIROMENT == 'development':
#     def index():
#         return send_from_directory(os.environ.get('WWW_FOLDER', ''), 'index.html')
#
#     def www(custom_path):
#         return send_from_directory(os.environ.get('WWW_FOLDER', ''), custom_path)
#
#     web_app.add_url_rule('/', 'index', index)
#     web_app.add_url_rule('/<path:custom_path>', 'www', www)


def run():
    """
    Run the flask app in a development enviroment
    """
    web_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
