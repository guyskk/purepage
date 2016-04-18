# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
import requests
import logging
import json
import six

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CouchdbException(Exception):

    def __init__(self, resp):
        self.status_code = resp.status_code
        self.resp = resp
        if resp.content:
            self.json = resp.json()
            self.error = self.json.get('error')
            self.reason = self.json.get('reason')
        else:
            self.json = None
            self.error = None
            self.reason = None

    def __repr__(self):
        return "<CouchdbException %s %s>: %s" %\
            (self.status_code, self.error or '', self.reason or '')

    def __str__(self):
        return "<%s %s>: %s" %\
            (self.status_code, self.error or '', self.reason or '')


def as_bytes(data):
    if not (isinstance(data, six.string_types) or
            isinstance(data, six.binary_type)):
        data = json.dumps(data, ensure_ascii=False)
        data = data.encode('utf-8')
    elif not isinstance(data, six.binary_type):
        data = data.encode('utf-8')
    return data


class HttpRequestsImpl():

    def request(self, method, url, **kwargs):
        kwargs.setdefault("headers", {})
        kwargs["headers"].setdefault('Accept', 'application/json')
        kwargs["headers"].setdefault('Content-Type', 'application/json')
        if "data" in kwargs:
            kwargs["data"] = as_bytes(kwargs["data"])
        logger.debug('"%s %s"\n%s' % (method, url, kwargs))
        resp = requests.request(method, url, **kwargs)
        stream = kwargs.get('stream', False)
        if resp.status_code >= 200 and resp.status_code <= 299:
            if not stream:
                if resp.content:
                    return resp.json()
                else:
                    return None
            else:
                return resp
        else:
            raise CouchdbException(resp)
