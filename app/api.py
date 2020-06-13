# -*- coding: utf-8 -*-

"""
This module define all the api endpoints
"""

from flask_restful import Api


def create_api(app):
    """
    Used when creating a Flask App to register the REST API and its resource
    """
    from app import resource

    api = Api(app)
