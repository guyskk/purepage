from urllib.parse import urlsplit, unquote, urlunsplit
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
from .http import HttpRequestsImpl, NotFound


def extract_credentials(url):
    """
    Extract authentication (username and password) credentials from the
    given URL.
    >>> extract_credentials('http://localhost:5984/_config/')
    ('http://localhost:5984/_config/', None)
    >>> extract_credentials('http://joe:secret@localhost:5984/_config/')
    ('http://localhost:5984/_config/', ('joe', 'secret'))
    >>> extract_credentials('http://joe%40example.com:secret@'
    ...                      'localhost:5984/_config/')
    ('http://localhost:5984/_config/', ('joe@example.com', 'secret'))
    """
    parts = urlsplit(url)
    netloc = parts[1]
    if '@' in netloc:
        creds, netloc = netloc.split('@')
        credentials = tuple(unquote(i) for i in creds.split(':'))
        parts = list(parts)
        parts[1] = netloc
    else:
        credentials = None
    return urlunsplit(parts), credentials


class CouchDB():

    def __init__(self, name, http=None, auth=None, skip_setup=False):
        """
        name: database url, eg: http://localhost:5984/dbname
        http: an object implement request method
        auth: (username, password)
        skip_setup: skip checks the database exists and tries to create it
        """
        self.init(name, http, auth, skip_setup)

    def init(self, name, http=None, auth=None, skip_setup=False):
        if auth is None:
            url, credentials = extract_credentials(name)
        else:
            url = name
            credentials = auth
        if credentials:
            self.auth = HTTPBasicAuth(*credentials)
        else:
            self.auth = None
        self.url = url
        if http is None:
            http = HttpRequestsImpl()
        self.http = http
        if not skip_setup:
            try:
                self.request('HEAD', self.url)
            except NotFound:
                self.request('PUT', self.url)

    def request(self, method, url, **kwargs):
        """Send request with auth"""
        return self.http.request(method, url, auth=self.auth, **kwargs)

    def destroy(self):
        """Delete the database"""
        return self.request('DELETE', self.url)

    def put(self, doc, id=None, rev=None):
        """Create a new document or update an existing document"""
        if id is None:
            if '_id' not in doc:
                raise ValueError('_id is required in doc')
            id = doc.pop('_id')
        if rev is not None:
            doc['_rev'] = rev
        url = self.url + '/' + id
        return self.request('PUT', url, data=doc)

    def post(self, doc):
        """Create a new document and let CouchDB auto-generate an _id"""
        return self.request('POST', self.url, data=doc)

    def get(self, id, **options):
        """Fetch a document"""
        url = self.url + '/' + id
        return self.request('GET', url, params=options)

    def remove(self, doc_or_id, rev=None):
        """Delete a document"""
        if isinstance(doc_or_id, str):
            id = doc_or_id
            if rev is None:
                raise ValueError('rev is required')
        else:
            id = doc_or_id['_id']
            if rev is None:
                if '_rev' not in doc_or_id:
                    raise ValueError('_rev is required in doc')
                rev = doc_or_id['_rev']
        return self.request('DELETE', id, params={'rev': rev})

    def bulk_docs(self, docs, new_edits=False):
        """Create/update a batch of documents"""
        url = self.url + '/_bulk_docs'
        params = {'new_edits': new_edits}
        return self.request('POST', url, data=docs, params=params)

    def all_docs(self, **options):
        """Fetch a batch of documents"""
        url = self.url + '/_all_docs'
        return self.request('POST', url, params=options)

    def changes(self, **options):
        """TODO"""

    def replicate(self, source, target):
        """Replicate a database"""
        url = urljoin(self.url, '_replicate')
        data = {
            'source': source,
            'target': target
        }
        return self.request('POST', url, data=data)

    def sync(self):
        """TODO"""

    def put_attachment(self, id, attachment_id, rev, attachment):
        """Save an attachment"""
        url = '%s/%s/%s' % (self.url, id, attachment_id)
        params = {'rev': rev}
        return self.request('PUT', url, data=attachment, params=params)

    def get_attachment(self, id,  attachment_id, rev=None):
        """Get an attachment"""
        url = '%s/%s/%s' % (self.url, id, attachment_id)
        params = {'rev': rev}
        return self.request('GET', url, params=params)

    def remove_attachment(self, id,  attachment_id, rev):
        """Delete an attachment"""
        url = '%s/%s/%s' % (self.url, id, attachment_id)
        params = {'rev': rev}
        return self.request('DELETE', url, params=params)

    def query(self, view, **options):
        """
        Query the database
        view: (design, view)
        """
        url = '%s/_design/%s/_view/%s' % (self.url, *view)
        return self.request('GET', url, params=options)

    def view_cleanup(self):
        """Cleans up any stale map/reduce indexes"""
        url = self.url + '/_view_cleanup'
        return self.request('POST', url)

    def info(self):
        """Get database information"""
        return self.request('GET', self.url)

    def compact(self):
        """Compact the database"""
        url = self.url + '/_compact'
        return self.request('POST', url)

    def revs_diff(self, diff):
        """Document revisions diff"""
        url = self.url + '/_revs_diff'
        return self.request('POST', url, data=diff)

    def bulk_get(self, docs):
        """Document bulk get"""
        url = self.url + '/_all_docs'
        return self.request('POST', url, data=docs)

    def on(self, event):
        """TODO"""
