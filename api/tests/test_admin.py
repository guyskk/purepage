def test_get(root, user):
    user("jack", email="jack@purepage.org")
    jack = root.admin.get({"account": "jack"})
    assert root.admin.get({"account": "jack@purepage.org"}) == jack
    assert jack["email"] == "jack@purepage.org"
    assert "lastlogin_ip" in jack


def test_put(root, user, res):
    user("jack")
    jack = root.admin.get({"account": "jack"})
    jack["role"] = "admin"
    jack["email"] = "jack1234@purepage.org"
    root.admin.put(jack)
    jack = root.admin.get({"account": "jack"})
    assert jack["role"] == "admin"
    assert jack["email"] == "jack1234@purepage.org"
    # jack现在是管理员
    res.user.post_login({
        "account": "jack",
        "password": "123456"
    })
    # 确认管理员权限
    res.admin.get({"account": "jack"})


def test_get_list(root, user):
    resp = root.admin.get_list({})
    assert len(resp) == 1
    user("jack")
    resp = root.admin.get_list({})
    assert len(resp) == 2


def test_delete(root, user, res, assert_error):
    jack = user("jack")
    jack_id = root.admin.get({"account": "jack"})["id"]
    root.admin.delete({"id": jack_id})
    with assert_error(403):
        jack.user.get_me()
    with assert_error(403):
        res.user.post_login({"account": "jack", "password": "123456"})
