FROM luyaochen/midn_server:20220711

MAINTAINER Luyao Chen <luyao.chen@uth.tmc.edu>

add --chown=www-data ./MIDN_Server /MIDN_Server

add  ./demo.key  /root/ssl.key
add  ./demo.cer  /root/ssl.cer

add  ./nginx_central /etc/nginx/sites-available/default

WORKDIR /MIDN_Server

RUN mkdir -p /var/log/uwsgi

COPY run_midn_server.sh /bin/.

RUN chmod +x /bin/run_midn_server.sh

CMD ["/bin/run_midn_server.sh"]

#CMD "/bin/bash"
