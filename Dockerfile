FROM python:3-alpine
# 1. musl-dev for pillow:
# http://stackoverflow.com/questions/30624829/no-such-file-
# or-directory-limits-h-when-installing-pillow-on-alpine-linux
# 2. libffi for misaka
RUN apk add --update\
    bash\
    git\
    musl-dev\
    jpeg-dev zlib-dev\
    python3-dev\
    libffi libffi-dev\
    build-base\
    && rm -rf /var/cache/apk/*
ENV LIBRARY_PATH=/lib:/usr/lib
ADD requires.txt /tmp/ 
RUN pip install --no-cache-dir -r /tmp/requires.txt
WORKDIR /code
EXPOSE 5000
CMD ["gunicorn", "--config", "file:/code/gunicorn.cfg", "manage:app"]
# CMD ["python", "manage.py", "runserver", "-d", "-h", "0.0.0.0", "-p", "5000"]


