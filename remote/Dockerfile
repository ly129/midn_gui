FROM luyaochen/midn_remote:20220711

MAINTAINER Luyao Chen <luyao.chen@uth.tmc.edu>

add --chown=www-data ./MIDN_Remote /MIDN_Remote

WORKDIR /MIDN_Remote

RUN mkdir -p /var/log/uwsgi

COPY run_midn_remote.sh /bin/.

RUN chmod +x /bin/run_midn_remote.sh

CMD ["/bin/run_midn_remote.sh"]

#CMD "/bin/bash"
