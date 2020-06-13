# -*- coding: utf-8 -*-
from importlib import import_module

from app import config as config_module


config = config_module.get_config()


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class Service(object):
    _domain = None

    class InvalidDomain(Exception):
        pass

    @classproperty
    def domain(cls):
        if cls._domain is None:
            raise cls.InvalidDomain('You should use a specific service implementation')
        try:
            return import_module(cls._domain)
        except Exception as ex:
            pass
