
def test_signup(user, assert_error):
    user("test")
    with assert_error(400, "Conflict"):
        user("test")


def test_login(res, user, assert_error):
    with assert_error(403, "UserNotFound"):
        res.user.post_login({"username": "jack", "password": "123456"})
    user("jack", email="jack@purepage.org")
    with assert_error(403, "WrongPassword"):
        res.user.post_login({"username": "jack", "password": "xxxxxx"})
    res.user.post_login({
        "username": "jack@purepage.org",
        "password": "123456"
    })


def test_get_me(res, user, assert_error):
    jack = user("jack")
    me = jack.user.get_me()
    assert me["username"] == "jack"
    with assert_error(403):
        res.user.get_me()


def test_get(user):
    jack = user("jack")
    jack_id = jack.user.get_me()["id"]
    tom = user("tom")
    assert tom.user.get({"id": jack_id})["username"] == "jack"


def test_put(user):
    jack = user("jack")
    me = jack.user.get_me()
    assert me["github"] == ""
    assert me["avatar"] == "http://purepage.org/static/avatar-default.png"
    jack.user.put({
        "github": "https://github.com/jack",
        "avatar": "http://purepage.org/static/logo.png"
    })
    me = jack.user.get_me()
    assert me["github"] == "https://github.com/jack"
    assert me["avatar"] == "http://purepage.org/static/logo.png"


def test_put_email(res, user, assert_error):
    jack = user("jack")
    with assert_error(403):
        res.user.post_login({
            "username": "jack@purepage.org",
            "password": "123456"
        })
    jack.user.put_email({
        "email": "jack@purepage.org",
        "password": "123456"
    })
    res.user.post_login({
        "username": "jack@purepage.org",
        "password": "123456"
    })


def test_put_password(res, user, assert_error):
    jack = user("jack")
    with assert_error(403):
        res.user.post_login({
            "username": "jack",
            "password": "jack1234"
        })
    jack.user.put_password({
        "new_password": "jack1234",
        "password": "123456"
    })
    res.user.post_login({
        "username": "jack",
        "password": "jack1234"
    })
    with assert_error(403):
        res.user.post_login({
            "username": "jack",
            "password": "123456"
        })


def test_forgot_reset(res, user, assert_error):
    import re
    from purepage.ext import mail
    user("tom")
    with assert_error(400, "UserNotFound"):
        res.user.post_forgot({"email": "tom@purepage.org"})
    user("jack", email="jack@purepage.org")
    with mail.record_messages() as outbox:
        res.user.post_forgot({"email": "jack@purepage.org"})
    assert outbox[0].subject == "PurePage重置密码"
    token = re.findall(r'http://purepage.org/reset/(.*)"', outbox[0].html)
    assert token
    token = token[0]
    with assert_error(403, "InvalidToken"):
        res.user.post_reset({
            "token": "xxxxxx",
            "password": "1234"
        })
    res.user.post_reset({
        "token": token,
        "password": "jack1234"
    })
    # Token只能用一次
    with assert_error(403, "InvalidToken"):
        res.user.post_reset({
            "token": token,
            "password": "1234"
        })
    res.user.post_login({
        "username": "jack",
        "password": "jack1234"
    })
    with assert_error(403):
        res.user.post_login({
            "username": "jack",
            "password": "123456"
        })
