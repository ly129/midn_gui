#!/bin/bash
service nginx start
cd  /MIDN_Server
./uwsgi_start.sh

cd /MIDN_Server/streamlit
nohup streamlit run midn_central_site_st.py  --server.port=8881 &


/bin/bash
