def test_get(guest):
    resp = guest.article.get(
        dict(userid='guyskk', catalog='2016', article='hello'))
    assert resp.status_code == 200
    assert resp.json['title'] == 'hello world'
    assert resp.json['tags'] == ['python', 'purepage']


def test_get_list(guest):
    resp = guest.article.get_list()
    assert resp.status_code == 200
    assert len(resp.json['rows']) == 2
    resp = guest.article.get_list(dict(userid='guyskk'))
    assert resp.status_code == 200
    assert len(resp.json['rows']) == 1
    resp = guest.article.get_list(dict(userid='guyskk', catalog='xxx'))
    assert resp.status_code == 200
    assert len(resp.json['rows']) == 0
    resp = guest.article.get_list(dict(userid='guyskk', tag='xxx'))
    assert resp.status_code == 200
    assert len(resp.json['rows']) == 0
    resp = guest.article.get_list(dict(tag='python'))
    assert resp.status_code == 200
    assert len(resp.json['rows']) == 1
