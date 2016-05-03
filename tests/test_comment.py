import time


def test_get(guest):
    resp = guest.comment.get(dict(article='guyskk.2016.hello'))
    assert resp.status_code == 200
    assert len(resp.json['rows']) == 1
    assert resp.json['rows'][0]['user']['_id'] == 'guyskk'
    assert resp.json['rows'][0]['content'] == 'good'


def test_post(res, guest):
    resp = res.comment.post(dict(article='guyskk.2016.hello', content='test'))
    assert resp.status_code == 200
    assert resp.json['content'] == 'test'
    assert resp.json['user']['_id'] == 'guyskk'
    assert resp.json['user']['photo'] == 'http://www.purepage.org/logo.png'

    time.sleep(0.1)  # delay 100ms
    resp = res.comment.get(dict(article='guyskk.2016.hello'))
    assert resp.status_code == 200
    assert len(resp.json['rows']) == 2
    resp = guest.comment.get(dict(article='guyskk.2016.hello'))
    assert resp.status_code == 200
    assert len(resp.json['rows']) == 2
