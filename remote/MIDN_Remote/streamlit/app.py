from flask import Flask

import socket


CUSTOM_OUTPUT_PATH =  'data/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['custom_output_PATH'] = CUSTOM_OUTPUT_PATH

try :
    hostname = socket.getfqdn()
    ip_addr = socket.gethostbyname_ex(hostname)[2][0]
except:
    app.config['client_ip'] = '172.17.0.32'
else:   
    app.config['client_ip'] = ip_addr 	
app.config['client_port'] = '6000'
app.config['client_name'] = 'Default Site'

app.config['server_app'] = 'http://172.17.0.28'


