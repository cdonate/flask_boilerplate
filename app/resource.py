# -*- coding: utf-8 -*-
import json
import re

from functools import wraps
from flask import request, g, Response
from flask_restful import Resource

from app import exceptions
from app.domain import user_domain


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = getattr(g, 'authenticated', False)
        if not authenticated:
            return Response('{"result": "Not Authorized"}', 401, content_type='application/json')
        return f(*args, **kwargs)
    return decorated_function


def not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return Response('{"result": "Method not allowed"}', 405, content_type='application/json')
    return decorated_function


class ResourceBase(Resource):
    entity_key = None

    class UserNotLogged(Exception):
        pass

    def __init__(self):
        self._me = None
        if self.logged_user is not None:
            self._me = user_domain.User.create_with_logged(self.logged_user)

    @property
    def me(self):
        return self._me

    @staticmethod
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def snake_to_camel(name):
        result = []
        for index, part in enumerate(name.split('_')):
            if index == 0:
                result.append(part.lower())
            else:
                result.append(part.capitalize())
        return ''.join(result)

    def transform_key(self, data, method):
        if isinstance(data, dict):
            return {method(key): self.transform_key(value, method) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {method(key): self.transform_key(value, method) for key, value in item.items()}
        return data

    @property
    def payload(self):
        payload = {}

        if request.method != 'GET' and request.json:
            payload.update(self.transform_key(request.json, self.camel_to_snake))
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
        if request.args:
            payload.update(self.transform_key(request.args, self.camel_to_snake))
        return payload

    @property
    def payload_with_files(self):
        payload = {}
        if request.json:
            dict = json.loads(request.form['payload'])
            payload.update(self.transform_key(dict, self.camel_to_snake))
        if request.form:
            dict = json.loads(request.form['payload'])
            payload.update(self.transform_key(dict, self.camel_to_snake))
        if request.args:
            dict = json.loads(request.form['payload'])
            payload.update(self.transform_key(dict, self.camel_to_snake))
        payload['files'] = request.files
        return payload

    @property
    def headers(self):
        return request.headers

    @property
    def request(self):
        return {'path': request.path, 'method': request.method, 'endpoint': request.endpoint}

    @property
    def logged_user(self):
        return getattr(g, 'user', None)

    @property
    def files(self):
        return request.files

    def response(self, data_dict):
        return self.transform_key(data_dict, self.snake_to_camel)

    @login_required
    @not_allowed
    def get(self, **kwargs):
        pass

    @login_required
    @not_allowed
    def post(self, **kwargs):
        pass

    @login_required
    @not_allowed
    def put(self, **kwargs):
        pass

    @login_required
    @not_allowed
    def delete(self, **kwargs):
        pass

    def return_unexpected_error(self):
        return {'result': 'error', 'error': 'Internal Server Error', 'exception': 'An unexpected error occurred'}, 500

    def return_ok(self, **extra):
        result = {'result': 'OK'}
        if extra is not None:
            result.update(extra)
        return result
