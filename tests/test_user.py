import re
from purepage import mail, auth


def parse_email(html):
    """find token in email content"""
    result = re.findall(r'token=(.*)"', html)
    if not result:
        raise ValueError('token not in html:%s' % html)
    return result[0]


def test_get(guest):
    resp = guest.user.get(dict(userid='guyskk'))
    assert resp.status_code == 200
    assert resp.json['_id'] == 'guyskk'


def test_get_me(res):
    resp = res.user.get_me()
    assert resp.status_code == 200
    assert resp.json['_id'] == 'guyskk'


def test_signup(guest):
    # test verify
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
        token = parse_email(outbox[0].html)
    # test signup
    resp = guest.user.post_signup(dict(token='123', password='123456'))
    assert resp.status_code == 400
    resp = guest.user.post_signup(dict(token=token, password='123456'))
    assert resp.status_code == 201
    assert auth.auth_header in resp.headers
    resp = guest.user.post_signup(dict(token=token, password='123456'))
    assert resp.status_code == 400
    assert auth.auth_header not in resp.headers


def test_login(guest):
    resp = guest.user.post_login(dict(userid='guyskk', password='123456'))
    assert resp.status_code == 200
    assert auth.auth_header in resp.headers
    resp = guest.user.post_login(dict(userid='guyskk2', password='123456'))
    assert resp.status_code == 403
    assert auth.auth_header not in resp.headers
    resp = guest.user.post_login(dict(userid='guyskk', password='1234567'))
    assert resp.status_code == 403
    assert auth.auth_header not in resp.headers
    resp = guest.user.post_login(dict(userid='guyskk2', password='1234562'))
    assert resp.status_code == 403
    assert auth.auth_header not in resp.headers
