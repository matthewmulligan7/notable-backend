FROM 5thcolumn/docker-restapi:v1.0.1
LABEL Maintainer: matt <matt>

COPY api /api
ARG CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip3 install -r /api/requirements.txt
ADD docker/uwsgi.ini /etc/uwsgi/
ADD docker/nginx.conf /etc/nginx/conf.d/default.conf
RUN mkdir /etc/supervisor.d/
ADD docker/api_supervisor.ini /etc/supervisor.d/
ADD docker/run.sh /

EXPOSE 80

CMD ["/run.sh"]
