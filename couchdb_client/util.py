# coding:utf-8
from __future__ import unicode_literals, absolute_import, print_function
import os
import json
import logging
from couchdb_client import CouchdbException


def dump_designs(db, path):
    params = {
        "startkey": '"_design/"',
        "endkey": '"_design0"',
        "include_docs": True
    }
    data = db.get_all_docs(params=params)
    for row in data["rows"]:
        name = os.path.basename(row["id"])
        design = row["doc"]
        del design["_rev"]
        with open(os.path.join(path, "%s.json" % name), "w") as f:
            json.dump(design, f)


def load_designs(db, path):
    designs = []
    for filename in os.listdir(path):
        name, ext = os.path.splitext(filename)
        if ext == ".json":
            try:
                design = db.get_doc(params={"docid": "_design/%s" % name})
            except CouchdbException as ex:
                if ex.status_code == 404:
                    design = {"_id": "_design/%s" % name}
                else:
                    raise
            with open(os.path.join("design", filename)) as f:
                design.update(json.load(f))
                designs.append(design)
    import pdb;pdb.set_trace()
    result = db.post_bulk_docs(data=designs)
    succeed = 0
    for (success, docid, rev_or_exc) in result:
        if success:
            succeed += 1
        else:
            logging.info("Error %s: %s" % (docid, rev_or_exc))
    logging.info("Succeed/Total = %s/%s" % (succeed, len(result)))
