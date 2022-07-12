uwsgi --ini  MIDN_server.ini --die-on-term --honour-stdin  --touch-reload=touch-gui.ini --master --daemonize /var/log/uwsgi/MIDN_Server.log
