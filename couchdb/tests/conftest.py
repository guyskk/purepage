import pytest
from couchdb import CouchDB
from couchdb.http import NotFound
from time import time


@pytest.fixture(scope='session')
def dburl():
    n = int(time() * 1000000)
    return "http://admin:123456@127.0.0.1:5984/couchdb-test%d" % n


@pytest.yield_fixture(scope='function')
def db(dburl):
    db = CouchDB(dburl)
    yield db
    try:
        db.destroy()
    except NotFound:
        pass
