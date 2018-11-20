FROM python:3.6

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./flask-test/requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/flask-test/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/local/flask-test/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

WORKDIR /application

ENTRYPOINT ["/entrypoint.sh"]
