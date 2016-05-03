from purepage import mail


def test_get(guest):
    resp = guest.user.get(dict(userid='guyskk'))
    assert resp.status_code == 200
    assert resp.json['_id'] == 'guyskk'


def test_get_me(res):
    resp = res.user.get_me()
    assert resp.status_code == 200
    assert resp.json['_id'] == 'guyskk'


def test_verify(guest):
    resp = guest.user.post_verify(
        dict(userid='guyskk', email='guyskk@qq.com'))
    assert resp.status_code == 400
    resp = guest.user.post_verify(
        dict(userid='guyskk2', email='guyskk@qq.com'))
    assert resp.status_code == 400
    with mail.record_messages() as outbox:
        resp = guest.user.post_verify(
            dict(userid='guyskk2', email='guyskk2@qq.com'))
        assert resp.status_code == 200
        assert len(outbox) == 1
        assert 'guyskk2@qq.com' in outbox[0].recipients
