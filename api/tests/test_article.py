import pytest


@pytest.fixture(name="article")
def fixture_article(root):
    def _article(name, user=root, catalog="test", title="test",
                 summary="test", tags=None, content="test"):
        resp = user.article.post({
            "name": name,
            "catalog": catalog,
            "title": title,
            "summary": summary,
            "tags": tags or [],
            "content": content
        })
        return resp["id"]
    return _article


def test_post(user, article):
    article("hello-root")
    jack = user("jack")
    article("hello-jack", user=jack)


def test_get(article, user, res):
    aid = article("hello-root")
    jack = user("jack")
    resp = jack.article.get({"id": aid})
    assert res.article.get({"id": aid}) == resp
    assert resp["name"] == "hello-root"
    assert resp["tags"] == []
    assert resp["content"] == "test"
    assert resp["user"]["username"] == "root"


def test_put(article, user, root, assert_error):
    jack = user("jack")
    aid = article("hello-jack", user=jack)
    art = root.article.get({"id": aid})
    new_art = art.copy()
    new_art["tags"] = ["jack"]
    with assert_error(403):
        root.article.put(new_art)
    jack.article.put(new_art)
    resp = jack.article.get({"id": aid})
    assert resp["name"] == "hello-jack"
    assert resp["tags"] == ["jack"]


def test_patch(article, user, root, assert_error):
    jack = user("jack")
    aid = article("hello-jack", user=jack)
    with assert_error(403):
        root.article.patch({"id": aid, "name": "hello-root"})
    jack.article.patch({"id": aid, "tags": ["jack"]})
    resp = jack.article.get({"id": aid})
    assert resp["name"] == "hello-jack"
    assert resp["tags"] == ["jack"]


def test_get_top(article, user, res):
    jack = user("jack")
    for i in range(6):
        article("hello-%d" % i, user=jack)
    resp = jack.article.get_top({"page": 2, "per_page": 4})
    assert res.article.get_top({"page": 2, "per_page": 4}) == resp
    assert len(resp) == 2


def test_get_list(article, user, res):
    jack = user("jack")
    tom = user("tom")
    article("hello-jack1", user=jack)
    article("hello-jack2", user=jack, tags=["jack"])
    article("hello-jack3", user=jack, catalog="jack")
    article("hello-tom", user=tom)

    def query(**kwargs):
        return len(res.article.get_list(kwargs))

    assert query(username="jack") == 3
    assert query(username="jack", tag="jack") == 1
    assert query(username="jack", catalog="jack") == 1
    assert query(username="tom") == 1
    assert query(username="tom", catalog="unknown") == 0
