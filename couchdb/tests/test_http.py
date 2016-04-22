from couchdb import http
import json
import mock
import requests
import pytest


def test_request_data():
    impl = http.HttpRequestsImpl()
    ret = requests.Response()
    ret.__setstate__(dict(status_code=200, _content=b'"hello"'))
    with mock.patch("requests.request", return_value=ret) as req:
        impl.request("POST", "http://127.0.0.1:5984", data={"中文": "中文"})
        args = req.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "http://127.0.0.1:5984"
        assert args[1]['data'] == json.dumps(
            {"中文": "中文"}, ensure_ascii=False).encode("utf-8")


def test_request_success():
    impl = http.HttpRequestsImpl()
    ret = requests.Response()
    ret.__setstate__(dict(status_code=200, _content=b'"hello"'))
    with mock.patch("requests.request", return_value=ret):
        data = impl.request("POST", "http://127.0.0.1:5984")
        assert data == 'hello'


def test_request_error():
    impl = http.HttpRequestsImpl()
    ret = requests.Response()
    ret.__setstate__(dict(status_code=400, _content=b'"bad hello"'))
    with mock.patch("requests.request", return_value=ret):
        with pytest.raises(http.BadRequest) as ex:
            impl.request("POST", "http://127.0.0.1:5984", data={"中文": "中文"})
            assert ex.status_code == 400
            assert ex.json == 'bad hello'
