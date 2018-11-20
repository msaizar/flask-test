FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN groupadd -r flasktest \
    && useradd -r -g flasktest flasktest

# Requirements are installed here to ensure they will be cached.
COPY ./flask-test/requirements /requirements
RUN pip install --no-cache-dir -r /requirements/local.txt \
    && rm -rf /requirements

COPY ./compose/production/flask-test/gunicorn.sh /gunicorn.sh
RUN sed -i 's/\r//' /gunicorn.sh
RUN chmod +x /gunicorn.sh
RUN chown flasktest /gunicorn.sh

COPY ./compose/production/flask-test/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chown flasktest /entrypoint.sh


COPY . /application

RUN chown -R flasktest /application

USER flasktest

WORKDIR /application

ENTRYPOINT ["/entrypoint.sh"]
