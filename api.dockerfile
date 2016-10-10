FROM daocloud.io/python:3-alpine
COPY api/requires.txt /tmp/
RUN pip install -r /tmp/requires.txt
EXPOSE 80 5000
WORKDIR /api
CMD ["gunicorn", "--config", "gunicorn.cfg", "index:app"]
