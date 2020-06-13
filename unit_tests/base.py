# -*- coding: utf-8 -*-

import unittest, os
from mock import mock

os.environ.update({
    'APP_SETTINGS': 'app.config.TestingConfig',
    'DATABASE_URL': 'postgresql+psycopg2://boilerplateuser:boilerplatepassword@localhost/boilerplatedatabasetests',
    'API-TOKEN': 'API-TOKEN-TEST',
})

from app import initialize


class TestCase(unittest.TestCase):
    mock = mock
