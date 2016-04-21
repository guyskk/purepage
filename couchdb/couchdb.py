
class CouchDB():

    def __init__(self, name, ajax=None, auth=None, skip_setup=False):
        """
        name: database url, eg: http://localhost:5984/dbname
        """
        pass

    def destroy(self):
        pass

    def put(self, doc, id, rev):
        pass

    def post(self, doc):
        pass

    def get(self, id, rev=None, attachments=False, binary=False):
        pass

    def remove(self, doc_or_id, rev=None):
        pass

    def bulkdocs(self, docs):
        pass

    def alldocs(self, **options):
        pass

    def changes(self, **options):
        pass

    def replicate(self, source, target):
        pass

    def sync(self):
        pass

    def put_attachment(self, id,  attachment_id, rev, attachment, type):
        pass

    def get_attachment(self, id,  attachment_id, rev=None):
        pass

    def remove_attachment(self, id,  attachment_id, rev):
        pass

    def query(self, fun, **options):
        pass

    def view_cleanup(self):
        pass

    def info(self):
        pass

    def compact(self):
        pass

    def revs_diff(self):
        pass

    def bulk_get(self, docs):
        pass

    def on(self, event):
        pass
