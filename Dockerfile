FROM python:3.9-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -i https://mirrors.cloud.tencent.com/pypi/simple Flask gunicorn httpx lxml ujson

CMD exec gunicorn --bind :80 --workers 1 --threads 1 --timeout 0 main:app