FROM python:3-alpine
RUN apk add --update git
COPY api/requires.txt /tmp/
RUN pip install -r /tmp/requires.txt
EXPOSE 80 5000
WORKDIR /api
CMD ["gunicorn", "--config", "gunicorn.cfg", "index:app"]
