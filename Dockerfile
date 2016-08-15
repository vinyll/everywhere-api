FROM phusion/baseimage

CMD ["/sbin/my_init"]

RUN apt-get update && \
    apt-get remove python && \
    apt-get install -y git nginx uwsgi uwsgi-plugin-python3 python3-dev python3-pip python3-setuptools
RUN pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN useradd nginx

# application folder
ENV APP_DIR /app

# app dir
RUN mkdir ${APP_DIR} \
	&& chown -R nginx:nginx ${APP_DIR} \
	&& chmod 777 /run/ -R \
	&& chmod 777 /root/ -R
VOLUME [${APP_DIR}]
WORKDIR ${APP_DIR}

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# copy config files into filesystem
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/app.ini /app.ini
COPY docker/entrypoint.sh /entrypoint.sh

# execute start up script
ENTRYPOINT ["/entrypoint.sh"]
