# coding:utf-8

from markdown import Markdown, util
import os
from StringIO import StringIO


class Article(object):

    """docstring for Article"""

    def __init__(self, path, html, meta):
        super(Article, self).__init__()
        self.path = path
        self.html = html
        self.meta = meta


def read(dir, name):
    path = os.path.join(dir, name)
    if not isinstance(path, util.text_type):
        path = path.decode("utf-8")
    md = Markdown(
        extensions=["markdown.extensions.toc", "markdown.extensions.meta"])
    output = StringIO()
    try:
        md.convertFile(path, output, encoding="utf-8")
        arti = Article(path, output.getvalue(), md.Meta)
        return arti
    finally:
        output.close()


if __name__ == '__main__':
    print read("../oth", "传输文件.md").meta
