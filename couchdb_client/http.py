# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CouchdbException(Exception):

    def __init__(self, resp):
        self.status_code = resp.status_code
        self.resp = resp
        if resp.content:
            self.json = resp.json()
            self.error = self.json['error']
            self.reason = self.json['reason']
        else:
            self.json = None
            self.error = None
            self.reason = None


class HttpRequestsImpl():

    def request(self, method, url, **kwargs):
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
