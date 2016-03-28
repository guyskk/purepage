# coding:utf-8

import os
from kkblog import create_app
from flask_script import Manager
from kkblog.article_util import read_repo, read_articles

app = create_app()
manage = Manager(app)


@manage.command
@manage.option("-u", "--url", dest="url")
def readrepo(url):
    print(read_repo(url, "data"))

@manage.command
@manage.option("-p", "--path", dest="path")
def readarticles(path):
    print(list(read_articles(path)))

if __name__ == '__main__':
    manage.run()
