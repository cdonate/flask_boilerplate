import os
import unittest
from mock import mock
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from app import database

os.environ.update({
    'APP_SETTINGS': 'app.config.TestingConfig',
    'DATABASE_URL': 'postgresql+psycopg2://boilerplateuser:boilerplatepassword@localhost/boilerplatedatabasetests',
    'API-TOKEN': 'API-TOKEN-TEST',
})

test_app = Flask(__name__)
test_app.config.from_object('app.config.TestingConfig')
database.AppRepository.db = SQLAlchemy(test_app)


class TestCase(unittest.TestCase):
    mock = mock
    client = test_app.test_client()
