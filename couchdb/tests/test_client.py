from couchdb import CouchDB
from couchdb.http import CouchdbException, NotFound
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


def put_delete(db):
    doc = {'_id': 'guyskk'}
    result = db.post(doc)
    assert result['ok']
    doc['_rev'] = result['rev']
    doc['_deleted'] = True
    result = db.put(doc)
    assert result['ok']
    with pytest.raises(NotFound):
        db.get('guyskk')


def test_post(db):
    doc = {'_id': 'guyskk'}
    result = db.post(doc)
    assert result['ok']
    assert result['id'] == 'guyskk'
    assert db.get('guyskk')['_id'] == 'guyskk'

    result = db.post({})
    assert result['ok']
    assert db.get(result['id'])['_id'] == result['id']


def test_remove(db):
    doc = {'_id': 'guyskk'}
    result = db.post(doc)
    assert result['ok']
    result = db.remove('guyskk', rev=result['rev'])
    assert result['ok']
    with pytest.raises(NotFound):
        db.get('guyskk')

    doc = {'_id': 'guyskk'}
    result = db.post(doc)
    assert result['ok']
    doc['_rev'] = result['rev']
    result = db.remove(doc)
    assert result['ok']
    with pytest.raises(NotFound):
        db.get('guyskk')


def test_bulk_docs(db):
    doc = {'_id': 'guyskk'}
    result = db.bulk_docs([doc])
    assert len(result) == 1
    assert result[0]['ok']

    # bulk update
    doc['_rev'] = result[0]['rev']
    doc['name'] = 'kk'
    result = db.bulk_docs([doc])
    assert len(result) == 1
    assert result[0]['ok']
    assert db.get('guyskk')['_id'] == 'guyskk'
    assert db.get('guyskk')['name'] == 'kk'

    # bulk delete
    doc['_rev'] = result[0]['rev']
    doc['_deleted'] = True
    result = db.bulk_docs([doc])
    assert len(result) == 1
    assert result[0]['ok']
    with pytest.raises(NotFound):
        db.get('guyskk')


def test_all_docs(db):
    doc = {'_id': 'guyskk'}
    result = db.post(doc)
    assert result['ok']
    result = db.all_docs(keys=['guyskk'])
    assert result['total_rows'] == 1
    assert result['rows'][0]['id'] == 'guyskk'

    result = db.all_docs(startkey='"guyskk"')
    assert result['total_rows'] == 1
    assert result['rows'][0]['id'] == 'guyskk'


@pytest.mark.skip(reason='Not support')
def test_query_tempview(db):
    doc = {'_id': 'guyskk'}
    result = db.post(doc)
    assert result['ok']
    view = {'map': "function(doc){emit(doc._id,null);}"}
    result = db.query(view)
    assert result['total_rows'] == 1
    assert result['rows'][0]['key'] == 'guyskk'


def test_query_design(db):
    design = {
        '_id': '_design/user',
        'views': {
            'by_id': {
                'map': "function(doc){emit(doc._id,null);}"
            }
        }
    }
    result = db.post(design)
    assert result['ok']
    doc = {'_id': 'guyskk'}
    result = db.post(doc)
    assert result['ok']

    result = db.query(('user', 'by_id'))
    assert result['total_rows'] == 1
    assert result['rows'][0]['key'] == 'guyskk'


def test_bulk_get(db):
    pass


def test_info(db):
    assert db.info()
