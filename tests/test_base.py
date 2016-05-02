import pytest


def test_info(app):
    with app.test_client() as c:
        resp = c.get("/api/info")
        assert resp.status_code == 200
        resp = c.get("/api/info/400")
        assert resp.status_code == 400
        resp = c.get("/api/info/403")
        assert resp.status_code == 403
        resp = c.get("/api/info/404")
        assert resp.status_code == 404
        with pytest.raises(ValueError) as exinfo:
            c.get("/api/info/500")
        assert exinfo.value.args[0] == 'test'


def test_base(guest, res):
    assert guest.info.get().status_code == 200
    assert guest.info.get_400().status_code == 400
    assert guest.info.get_403().status_code == 403
    assert guest.info.get_404().status_code == 404
    with pytest.raises(ValueError) as exinfo:
        guest.info.get_500()
    assert exinfo.value.args[0] == 'test'

    assert guest.user.get_me().status_code == 403
    assert guest.article.get_list().status_code == 200
    assert guest.comment.post().status_code == 403

    assert res.user.get_me().status_code == 200
    assert res.article.get_list().status_code == 200
    assert res.comment.post().status_code == 400
