# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
from couchdb_client.http import HttpRequestsImpl
from base64 import b64encode
from requests.auth import AuthBase
from six.moves.urllib import parse


def extract_credentials(url):
    """
    Extract authentication (user name and password) credentials from the
    given URL.
    >>> extract_credentials('http://localhost:5984/_config/')
    ('http://localhost:5984/_config/', None)
    >>> extract_credentials('http://joe:secret@localhost:5984/_config/')
    ('http://localhost:5984/_config/', ('joe', 'secret'))
    >>> extract_credentials('http://joe%40example.com:secret@'
    ...                      'localhost:5984/_config/')
    ('http://localhost:5984/_config/', ('joe@example.com', 'secret'))
    """
    parts = parse.urlsplit(url)
    netloc = parts[1]
    if '@' in netloc:
        creds, netloc = netloc.split('@')
        credentials = tuple(parse.unquote(i) for i in creds.split(':'))
        parts = list(parts)
        parts[1] = netloc
    else:
        credentials = None
    return parse.urlunsplit(parts), credentials


class CouchdbBaseAuth(AuthBase):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        token = b64encode(('%s:%s' % (self.username, self.password)).encode('ascii'))
        self.token = (b'Basic %s' % token.strip()).decode('ascii')

    def __call__(self, r):
        r.headers['Authorization'] = self.token
        return r


class Client(object):

    def __init__(self, url, http=None):
        self.init(url, http)

    def init(self, url, http=None):
        url, credentials = extract_credentials(url)
        if credentials:
            auth = CouchdbBaseAuth(*credentials)
            self.auth = auth
        else:
            self.auth = None
        self.url = url
        if http is None:
            http = HttpRequestsImpl()
        self.http = http

    def request(self, method, url_tmpl, path_params, params, **kwargs):
        url_tmpl = self.url + url_tmpl
        path_params = {k: params.pop(k) for k in path_params}
        url = url_tmpl.format(**path_params)
        return self.http.request(method, url, params=params,
                                 auth=self.auth, **kwargs)


class Server(Client):

    def get(self, params=None, **kwargs):
        url = '/'
        return self.request('GET', url, [], params, **kwargs)

    def get_active_tasks(self, params=None, **kwargs):
        url = '/_active_tasks'
        return self.request('GET', url, [], params, **kwargs)

    def get_all_dbs(self, params=None, **kwargs):
        url = '/_all_dbs'
        return self.request('GET', url, [], params, **kwargs)

    def get_db_updates(self, params=None, **kwargs):
        url = '/_db_updates'
        return self.request('GET', url, [], params, **kwargs)

    def get_log(self, params=None, **kwargs):
        url = '/_log'
        return self.request('GET', url, [], params, **kwargs)

    def post_replicate(self, params=None, **kwargs):
        url = '/_replicate'
        return self.request('POST', url, [], params, **kwargs)

    def post_restart(self, params=None, **kwargs):
        url = '/_restart'
        return self.request('POST', url, [], params, **kwargs)

    def get_stats(self, params=None, **kwargs):
        """/_stats/{section}/{statistic}"""
        url = '/_stats'
        if params is not None and 'section' in params:
            section = params.pop('section')
            url = url + '/' + section
            if 'statistic' in params:
                statistic = params.pop('statistic')
                url = url + '/' + statistic
        return self.request('GET', url, [], params, **kwargs)

    def get_uuids(self, params=None, **kwargs):
        url = '/_uuids'
        return self.request('GET', url, [], params, **kwargs)


class Database(Client):

    def head(self, params=None, **kwargs):
        url = '/'
        return self.request('HEAD', url, [], params, **kwargs)

    def get(self, params=None, **kwargs):
        url = '/'
        return self.request('GET', url, [], params, **kwargs)

    def put(self, params=None, **kwargs):
        url = '/'
        return self.request('PUT', url, [], params, **kwargs)

    def delete(self, params=None, **kwargs):
        url = '/'
        return self.request('DELETE', url, [], params, **kwargs)

    def get_all_docs(self, params=None, **kwargs):
        url = '/_all_docs'
        return self.request('GET', url, [], params, **kwargs)

    def post_all_docs(self, params=None, **kwargs):
        url = '/_all_docs'
        return self.request('POST', url, [], params, **kwargs)

    def post_bulk_docs(self, params=None, **kwargs):
        url = '/_bulk_docs'
        return self.request('POST', url, [], params, **kwargs)

    def get_changes(self, params=None, **kwargs):
        url = '/_changes'
        return self.request('GET', url, [], params, **kwargs)

    def post_changes(self, params=None, **kwargs):
        url = '/_changes'
        return self.request('POST', url, [], params, **kwargs)

    def post_compact(self, params=None, **kwargs):
        url = '/_compact'
        return self.request('POST', url, [], params, **kwargs)

    def post_compact_design(self, params=None, **kwargs):
        url = '/_compact/{ddoc}'
        return self.request('POST', url, ['ddoc'], params, **kwargs)

    def post_ensure_full_commit(self, params=None, **kwargs):
        url = '/_ensure_full_commit'
        return self.request('POST', url, [], params, **kwargs)

    def post_view_cleanup(self, params=None, **kwargs):
        url = '/_view_cleanup'
        return self.request('POST', url, [], params, **kwargs)

    def get_security(self, params=None, **kwargs):
        url = '/_security'
        return self.request('GET', url, [], params, **kwargs)

    def put_security(self, params=None, **kwargs):
        url = '/_security'
        return self.request('PUT', url, [], params, **kwargs)

    def post_temp_view(self, params=None, **kwargs):
        url = '/_temp_view'
        return self.request('POST', url, [], params, **kwargs)

    def post_purge(self, params=None, **kwargs):
        url = '/_purge'
        return self.request('POST', url, [], params, **kwargs)

    def post_missing_revs(self, params=None, **kwargs):
        url = '/_missing_revs'
        return self.request('POST', url, [], params, **kwargs)

    def post_revs_diff(self, params=None, **kwargs):
        url = '/_revs_diff'
        return self.request('POST', url, [], params, **kwargs)

    def get_revs_limit(self, params=None, **kwargs):
        url = '/_revs_limit'
        return self.request('GET', url, [], params, **kwargs)

    def put_revs_limit(self, params=None, **kwargs):
        url = '/_revs_limit'
        return self.request('PUT', url, [], params, **kwargs)

    # document
    def head_doc(self, params=None, **kwargs):
        url = '/{docid}'
        return self.request('HEAD', url, ['docid'], params, **kwargs)

    def get_doc(self, params=None, **kwargs):
        url = '/{docid}'
        return self.request('GET', url, ['docid'], params, **kwargs)

    def put_doc(self, params=None, **kwargs):
        url = '/{docid}'
        return self.request('PUT', url, ['docid'], params, **kwargs)

    def delete_doc(self, params=None, **kwargs):
        url = '/{docid}'
        return self.request('DELETE', url, ['docid'], params, **kwargs)

    def copy_doc(self, params=None, **kwargs):
        url = '/{docid}'
        return self.request('COPY', url, ['docid'], params, **kwargs)

    def post_doc(self, params=None, **kwargs):
        url = '/'
        return self.request('POST', url, [], params, **kwargs)

    def head_attach(self, params=None, **kwargs):
        url = '/{docid}/{attname}'
        return self.request('HEAD', url, ['docid', 'attname'],
                            params, **kwargs)

    def get_attach(self, params=None, **kwargs):
        url = '/{docid}/{attname}'
        return self.request('GET', url, ['docid', 'attname'], params, **kwargs)

    def put_attach(self, params=None, **kwargs):
        url = '/{docid}/{attname}'
        return self.request('PUT', url, ['docid', 'attname'], params, **kwargs)

    def delete_attach(self, params=None, **kwargs):
        url = '/{docid}/{attname}'
        return self.request('DELETE', url, ['docid', 'attname'],
                            params, **kwargs)

    def get_local(self, params=None, **kwargs):
        url = '/_local/{docid}'
        return self.request('GET', url, ['docid'], params, **kwargs)

    def put_local(self, params=None, **kwargs):
        url = '/_local/{docid}'
        return self.request('GET', url, ['docid'], params, **kwargs)

    def delete_local(self, params=None, **kwargs):
        url = '/_local/{docid}'
        return self.request('GET', url, ['docid'], params, **kwargs)

    def copy_local(self, params=None, **kwargs):
        url = '/_local/{docid}'
        return self.request('GET', url, ['docid'], params, **kwargs)

    # design
    def get_design_info(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_info'
        return self.request('GET', url, ['ddoc'], params, **kwargs)

    def get_view(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_view/{view}'
        return self.request('GET', url, ['ddoc', 'view'], params, **kwargs)

    def post_view(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_view/{view}'
        return self.request('POST', url, ['ddoc', 'view'], params, **kwargs)

    def get_show(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_show/{func}'
        if params is not None and 'docid' in params:
            url = url + '/' + params.pop('docid')
        return self.request('GET', url, ['ddoc', 'func'], params, **kwargs)

    def post_show(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_show/{func}'
        if params is not None and 'docid' in params:
            url = url + '/' + params.pop('docid')
        return self.request('POST', url, ['ddoc', 'func'], params, **kwargs)

    def get_list(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_list/{func}/{view}'
        return self.request('GET', url, ['ddoc', 'func', 'view'],
                            params, **kwargs)

    def post_list(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_list/{func}/{view}'
        return self.request('POST', url, ['ddoc', 'func', 'view'],
                            params, **kwargs)

    def get_list_other(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_list/{func}/{other}/{view}'
        return self.request('GET', url, ['ddoc', 'func', 'other', 'view'],
                            params, **kwargs)

    def post_list_other(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_list/{func}/{other}/{view}'
        return self.request('POST', url, ['ddoc', 'func', 'other', 'view'],
                            params, **kwargs)

    def post_update(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_update/{func}'
        return self.request('POST', url, ['ddoc', 'func'],
                            params, **kwargs)

    def put_update(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_update/{func}/{docid}'
        return self.request('POST', url, ['ddoc', 'func', 'docid'],
                            params, **kwargs)

    def post_rewrite(self, params=None, **kwargs):
        url = '/_design/{ddoc}/_rewrite/{path}'
        return self.request('POST', url, ['ddoc', 'path'], params, **kwargs)
