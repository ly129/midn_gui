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
    app.config['server_ip'] = '172.17.0.32'
else:   
    app.config['server_ip'] = ip_addr 	

app.config['server_port_from'] = '6600'

app.config['server_app'] = 'https://127.0.0.1'
