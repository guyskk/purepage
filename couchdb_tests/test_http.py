# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from couchdb_client import http
import json
import mock
import requests


def test_as_bytes():
    data_expect = [
        ('中文', '中文'.encode('utf-8')),
        ('中文'.encode('utf-8'), '中文'.encode('utf-8')),
        ('abc123', b'abc123'),
        ({'name': '中文'}, json.dumps({'name': '中文'},
                                    ensure_ascii=False).encode('utf-8')),
        ({'中文': '中文'}, json.dumps({'中文': '中文'},
                                  ensure_ascii=False).encode('utf-8')),
        ('', b''),
        (123, json.dumps(123).encode('utf-8')),
        (None, json.dumps(None).encode('utf-8')),
        ({}, json.dumps({}).encode('utf-8')),
    ]
    for data, expect in data_expect:
        assert http.as_bytes(data) == expect, "%s: %s" % (data, expect)


def test_request():
    impl = http.HttpRequestsImpl()
    ret = requests.Response()
    ret.__setstate__(dict(status_code=200, _content=b'"hello"'))
    with mock.patch("requests.request", return_value=ret) as req:
        data = impl.request("POST", "http://127.0.0.1:5984", data={"中文": "中文"})
        assert data == 'hello'
        args = req.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "http://127.0.0.1:5984"
        assert args[1]['data'] == json.dumps(
            {"中文": "中文"}, ensure_ascii=False).encode("utf-8")
