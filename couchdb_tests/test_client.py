# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from couchdb_client import Database, Server, Client, CouchdbException
import pytest


def test_client():
    c = Client("http://admin:123456@127.0.0.1:5984")
    with pytest.raises(CouchdbException) as ex:
        c.request("GET", "/_design/{ddoc}/_view/{view}",
                  path_params=['ddoc', 'view'],
                  params=dict(ddoc='user', view='email'))
        assert ex.status_code == 404
