from flask_script import Manager
from purepage import create_app, db
from purepage.util import read_repo, read_articles
from couchdb_client.util import load_designs, dump_designs


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


@manage.command
def initdb():
    load_designs(db, "design")


@manage.command
def savedb():
    dump_designs(db, "design")

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    manage.run()
