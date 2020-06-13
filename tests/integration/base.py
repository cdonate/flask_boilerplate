# -*- coding: utf-8 -*-
import json
import os
import shutil
import unittest
import re

from mock import mock
from app import initialize, database, models


def read_json(name, directory='create_json'):
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def transform_key(data):
        if isinstance(data, dict):
            return {camel_to_snake(key): transform_key(value) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {camel_to_snake(key): transform_key(value) for key, value in item.items()}
        return data

    return transform_key(json.loads(open('{}/{}.json'.format(directory, name)).read()))


class TestCase(unittest.TestCase):
    mock = mock
    app = initialize.web_app.test_client()
    url = None
    payload = {}

    def setUp(self):
        database.AppRepository.db.create_all()
        self.payload = {}
        self.__cookies = {}
        self.__headers = {'Content-Type': 'application/json', 'Cookie': self.cookies}

    @property
    def cookies(self):
        cookie = ''
        for key, value in self.__cookies.iteritems():
            cookie += '{}={};'.format(key, value)
        return cookie

    @cookies.setter
    def cookies(self, cookies):
        self.__cookies = cookies

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers):
        self.__headers = headers

    @property
    def response_get(self):
        return self.app.get(self.url, data=json.dumps(self.payload), headers=self.headers)

    @property
    def response_post(self):
        return self.app.post(self.url, data=json.dumps(self.payload), headers=self.headers)

    @property
    def response_post_upload(self):
        return self.app.post(self.url, data=self.payload, headers={'Content-Type': 'multipart/form-data'})

    @property
    def response_put(self):
        return self.app.put(self.url, data=json.dumps(self.payload), headers=self.headers)

    @property
    def response_delete(self):
        return self.app.delete(self.url)

    def tearDown(self):
        # Delete all rows for every table
        # for something in models.Something.query.all():
        #     something.delete_db()

        database.AppRepository.db.session.remove()
        database.AppRepository.db.drop_all()
