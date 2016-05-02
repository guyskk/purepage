import os
import json
import logging
from .http import NotFound


class UtilMixin:

    def dump_designs(self, path):
        params = {
            "startkey": '"_design/"',
            "endkey": '"_design0"',
            "include_docs": True
        }
        data = self.all_docs(**params)
        for row in data["rows"]:
            name = os.path.basename(row["id"])
            design = row["doc"]
            del design['_rev']
            with open(os.path.join(path, "%s.json" % name), "w") as f:
                json.dump(design, f)

    def load_designs(self, path):
        designs = []
        for filename in os.listdir(path):
            name, ext = os.path.splitext(filename)
            if ext == ".json":
                try:
                    design = self.get("_design/%s" % name)
                except NotFound:
                    design = {"_id": "_design/%s" % name}
                with open(os.path.join("design", filename)) as f:
                    design.update(json.load(f))
                    designs.append(design)
        result = self.bulk_docs(designs)
        succeed = 0
        for (success, docid, rev_or_exc) in result:
            if success:
                succeed += 1
            else:
                logging.info("Error %s: %s" % (docid, rev_or_exc))
        logging.info("Succeed/Total = %s/%s" % (succeed, len(result)))

    def count(self, view, key):
        """统计key的数量"""
        result = self.query(view, key=key, group=True)['rows']
        if result:
            assert len(result) == 1
            return result[0][key].value
        else:
            return 0
