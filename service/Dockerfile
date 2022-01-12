FROM python:3.9-slim as base

RUN useradd -ms /bin/bash user --home /app

WORKDIR /app
ENV PYTHONPATH=/app

COPY reqs/base.txt requirements.txt
RUN pip install -r requirements.txt


FROM base as unit-tests

RUN apt-get update -qy && apt-get install -qy curl

WORKDIR /src
ENV PYTHONPATH=/src/app

COPY reqs/test.txt requirements.test.txt
RUN  pip install -r requirements.test.txt

COPY . /src
ENTRYPOINT ["sh", "-c"]
CMD ["/src/app/tests-start.sh"]


FROM base as run

COPY scripts/start.sh /start.sh
COPY scripts/gunicorn_conf.py /gunicorn_conf.py
COPY app /app

USER user

EXPOSE 8000
ENTRYPOINT ["/start.sh"]
