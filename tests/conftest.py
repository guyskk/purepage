# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from kkblog import create_app, couch, db
from couchdb_client import util
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)


@pytest.yield_fixture(scope="session")
def app():
    app = create_app("kkblog.config_test")
    util.load_designs(db, "design")
    yield app
    db.delete()
