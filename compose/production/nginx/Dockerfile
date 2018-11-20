FROM nginx

COPY ./compose/production/nginx/sites-enabled/flasktest.conf /etc/nginx/conf.d/default.conf

COPY ./compose/production/nginx/start.sh /usr/local/bin/start.sh

RUN chmod +x /usr/local/bin/start.sh

CMD [ "/usr/local/bin/start.sh" ]