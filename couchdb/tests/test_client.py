from couchdb import CouchDB
from couchdb.http import CouchdbException
import pytest


def test_init_skip_setup(dburl):
    db = CouchDB(dburl, skip_setup=True)
    with pytest.raises(CouchdbException) as excinfo:
        db.info()
    assert excinfo.value.status_code == 404


def test_init_auth(dburl):
    with pytest.raises(CouchdbException) as excinfo:
        CouchDB(dburl, auth=('guyskk', '123456'))
    assert excinfo.value.status_code == 401


def test_request(db):
    assert db.request('GET', db.url, params={'q': '1'})
    assert db.request('POST', db.url, data={'q': '1'})
    with pytest.raises(CouchdbException) as excinfo:
        db.request('GET', 'http://127.0.0.1:5984/xxx')
    assert excinfo.value.status_code == 404


def test_destroy(db):
    db.destroy()
    with pytest.raises(CouchdbException) as excinfo:
        db.info()
    assert excinfo.value.status_code == 404


def test_put_get(db):
    doc = {'_id': 'guyskk'}
    result = db.put(doc)
    assert result['ok']
    assert result['id'] == 'guyskk'
    assert db.get('guyskk')['_id'] == 'guyskk'

    # test update document
    rev = result['rev']
    result = db.put({}, id='guyskk2')
    assert result['ok']
    assert result['id'] == 'guyskk2'
    doc['name'] = 'kk'
    result = db.put(doc, rev=rev)
    assert result['ok']
    assert db.get(result['id'])['name'] == 'kk'
    rev = result['rev']
    doc['name'] = 'kkkk'
    result = db.put(doc, rev=rev)
    assert db.get(result['id'])['name'] == 'kkkk'

    # test unicode id
    doc = {'_id': '关闭'}
    result = db.put(doc)
    assert result['ok']
    assert result['id'] == '关闭'
    assert db.get('关闭')['_id'] == '关闭'


def test_info(db):
    assert db.info()
