docker run -d\
    -v /home/guyskk/kkblog/data/couchdb:/usr/local/var/lib/couchdb\
    --name couchdb\
    -p 5984:5984 klaemo/couchdb:2.0-dev\
    --admin=admin:123456\
    --with-haproxy
