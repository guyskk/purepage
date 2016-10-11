
def test_client(client):
    assert client.get("/").status_code == 200


def test_root(root):
    me = root.user.get_me()
    assert me["username"] == "root"
    assert me["role"] == "root"


def test_user(user):
    res = user("guyskk", email="guyskk@purepage.org")
    me = res.user.get_me()
    assert me["username"] == "guyskk"
    assert me["role"] == "normal"
    assert "email" not in me
