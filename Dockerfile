FROM python:3-alpine
# musl-dev:
# http://stackoverflow.com/questions/30624829/no-such-file-
# or-directory-limits-h-when-installing-pillow-on-alpine-linux
RUN apk add --update\
    bash\
    nginx\
    musl-dev\
    jpeg-dev zlib-dev\
    python3-dev\
    build-base\
    && rm -rf /var/cache/apk/*
ENV LIBRARY_PATH=/lib:/usr/lib
ADD requires.txt /tmp/ 
RUN pip install --no-cache-dir -r /tmp/requires.txt
ADD gunicorn.cfg /usr/
ADD nginx.conf /usr/
CMD gunicorn --config=file:/usr/gunicorn.cfg manage:app &&\
    nginx -c /usr/nginx.conf

