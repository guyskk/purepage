def test_get(root, user):
    user("jack", "jack@purepage.org")
    jack = root.admin.get({"username": "jack"})
    assert root.admin.get({"username": "jack@purepage.org"}) == jack
    assert jack["email"] == "jack@purepage.org"
    assert "lastlogin_ip" in jack


def test_put(root, user, res):
    user("jack")
    jack = root.admin.get({"username": "jack"})
    jack["username"] = "jack1234"
    jack["role"] = "admin"
    jack["email"] = "jack1234@purepage.org"
    root.admin.put(jack)
    # jack现在是管理员
    jack = res.user.post_login({
        "username": "jack1234",
        "password": "123456"
    })
    jack = root.admin.get({"username": "jack1234"})
    assert jack["email"] == "jack1234@purepage.org"
    assert jack["role"] == "admin"
    # 确认管理员权限
    assert res.admin.get({"username": "jack1234"})


def test_get_list(root, user):
    resp = root.admin.get_list({})
    assert len(resp) == 1
    user("jack")
    resp = root.admin.get_list({})
    assert len(resp) == 2


def test_delete(root, user, res, assert_error):
    jack = user("jack")
    jack_id = root.admin.get({"username": "jack"})["id"]
    root.admin.delete({"id": jack_id})
    with assert_error(403):
        jack.user.get_me()
    with assert_error(403):
        res.user.post_login({"username": "jack", "password": "123456"})
