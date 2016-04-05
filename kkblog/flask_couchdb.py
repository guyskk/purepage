# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
import os
import couchdb
import json
import logging


class CouchDB(object):
    """CouchDB"""

    def __init__(self, app=None):
        self.server = None
        self.db = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.server = couchdb.Server(app.config["DATABASE_URL"])
        database = app.config["DATABASE_NAME"]
        if database not in self.server:
            self.server.create(database)
        self.db = self.server[database]

    def dump_designs(self, path):
        params = {
            "startkey": '"_design/"',
            "endkey": '"_design0"',
            "include_docs": True
        }
        __, __, data = self.db.resource("_all_docs").get_json(**params)
        for row in data["rows"]:
            name = os.path.basename(row["id"])
            design = row["doc"]
            del design["_rev"]
            with open(os.path.join(path, "%s.json" % name), "w") as f:
                json.dump(design, f)

    def load_designs(self, path):
        designs = []
        for filename in os.listdir(path):
            name, ext = os.path.splitext(filename)
            if ext == ".json":
                design = self.db.get("_design/%s" %
                                     name, {"_id": "_design/%s" % name})
                with open(os.path.join("design", filename)) as f:
                    design.update(json.load(f))
                    designs.append(design)
        result = self.db.update(designs)
        succeed = 0
        for (success, docid, rev_or_exc) in result:
            if success:
                succeed += 1
            else:
                logging.info("Error %s: %s" % (docid, rev_or_exc))
        logging.info("Succeed/Total = %s/%s" % (succeed, len(result)))
