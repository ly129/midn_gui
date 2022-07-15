import os,re
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, jsonify, Response
from werkzeug.utils import secure_filename
import time
import uuid
from datetime import datetime
import requests
import json
import pandas as pd
import sqlite3


from subprocess import Popen, PIPE

def run_R(R_file,task_id):
  # COMMAND WITH ARGUMENTS  cmd = ["Rscript", R_file]
  log = open('./data/{}.txt'.format(task_id), 'w')
#  p = Popen(cmd, cwd="./code/",stdin=PIPE, stdout=PIPE, stderr=PIPE)
  p = Popen(cmd, cwd="./code/",stdin=log, stdout=log, stderr=log)
#  output, error = p.communicate()

  # PRINT R CONSOLE OUTPUT (ERROR OR NOT)
#  if p.returncode == 0:
#      print('R OUTPUT:\n {0}'.format(output))
#  else:
#      print('R ERROR:\n {0}'.format(error))


data_folder = 'data/'

con = sqlite3.connect('controller.db')

cur = con.cursor()

# Create table

cur.execute( '''DROP TABLE IF EXISTS tasks''')
cur.execute( '''DROP TABLE IF EXISTS jobs''')

cur.execute('''CREATE TABLE IF NOT EXISTS tasks 
               (task_id text, total_remote_sites  integer, registered_remote_sites integer,  method text,imputed_datasets integer, missing_variables  text, 
                model text, iteration_between_imputation integer,iteration_until_first_imputation integer, server_ip text, server_port_from text, job_creation_dttm text,  status text )''')


cur.execute('''CREATE TABLE IF NOT EXISTS jobs
               (task_id text, client_name text,client_ip text, client_port text, server_port text, status text )''')



# Save (commit) the changes
con.commit()
con.close()

@app.route('/init')
def init_form():
    return render_template('init.html',server_ip=app.config['server_ip'],server_port_from=app.config['server_port_from'])

@app.route('/init', methods=['POST'])
def init_update():
    post_json = request.data.decode("utf-8")
    post_json = json.loads(post_json)
    print(post_json)

    con = sqlite3.connect('controller.db')
    cur = con.cursor()

# {'task_id': '838435da-0fe2-45f8-b23f-b66420bf7a78', 'total_remote_sites': 1, 'method': 'AVGMMI', 'impute_datasets': 10, 'missing_variables': '', 
#'model': 'Gaussian', 'server_ip': '172.17.0$




    cur.execute("INSERT INTO tasks VALUES ('{}',{},{},'{}',{},'{}','{}',{},{},'{}','{}','{}','{}')".format(
        post_json['task_id'],
        post_json['total_remote_sites'],
        0,
        post_json['method'],
        post_json['impute_datasets'],
        post_json['missing_variables'],
        post_json['model'],
        post_json['iteration_between_imputation'],
        post_json['iteration_until_first_imputation'],
        post_json['server_ip'],
        post_json['server_port_from'],
        post_json['job_creation_dttm'],
        'New'
        ))
    con.commit()
    con.close()

    return  jsonify ( {'message': '{} job created'.format(post_json['task_id'])} )

@app.route('/register')
def register_form():
    return render_template('register.html')


#windows test curl -H "Content-Type: application/json" -X POST http://129.106.31.45:7796/register  -d "{\"task_id\":\"c5028fed-febf-4533-8532-9f57f0c87227\", \"client_ip\":\"test\",\"client_port\":\"test\"}"
 
@app.route('/register', methods=['POST'])
def register_update():
    message=''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        message =  'Content-Type not supported!'

    print(json)
    task_id = json['task_id']
    print(task_id)
    client_ip = json['client_ip']
    client_port= json['client_port']
    client_name= json['client_name']

    con = sqlite3.connect('controller.db')
    cur = con.cursor()
    message = '' 
 
    cur.execute("select * from tasks where task_id = '{}'".format(task_id))
    row = cur.fetchone()
    print(row)
    if row is None:
        message = 'No such task found'
        return  jsonify ({'task_id':task_id, 'message': message})
    else:
        cur.execute("select * from jobs where task_id = '{}' and client_name = '{}'".format(task_id, client_name))
        job_row = cur.fetchone()
        if job_row is not None:
            server_port = job_row[3]
            cur.execute("update jobs set status='New', client_ip='{}',client_port = '{}',server_port = '{}'  where task_id = '{}' and client_name = '{}'".format(client_ip,client_port,server_port,task_id,client_name))
            message = 'Job Updated'
        else:
            server_port = row[10]
            if row[2]>= row[1]:
                message = 'max clients reached'
                return  jsonify ({'task_id':task_id, 'message': message})
            else:
                if row[1] == (row[2] + 1) :
                    cur.execute("update tasks set registered_remote_sites  = registered_remote_sites + 1 , server_port_from = server_port_from + 1,  status = 'acknowledged' where task_id = '{}' ".format(task_id))
                else:
                    cur.execute("update tasks set registered_remote_sites  = registered_remote_sites  + 1 , server_port_from = server_port_from + 1 , status = 'acknowledging' where task_id = '{}' ".format(task_id))
                cur.execute("INSERT INTO jobs VALUES ('{}','{}','{}','{}','{}','{}')".format(task_id,client_name,client_ip,client_port,server_port,'New'))
                message = 'Job Added'   
    con.commit()
    con.close()
    return  jsonify ({'task_id':task_id,'core_function':row[3],'server_ip':row[9],'server_port':server_port, 'client_port':client_port,'missing_variables':row[5], 'message': message})


def start_central(task_id):

    con = sqlite3.connect('controller.db')
    cur = con.cursor()
    message = ''

    cur.execute("select count(*) from jobs  where task_id = '{}' and  status= 'running'".format(task_id))
    row = cur.fetchone()
    runing_jobs = row[0]

    cur.execute("select total_clients,status from tasks  where task_id = '{}' ".format(task_id))
    row = cur.fetchone()
    total_clients  = row[0]
    tasks_status = row [1]

    if runing_jobs == total_clients : #and  tasks_status != 'runnnig' :
        cur.execute("update tasks set status = 'runnnig' where task_id = '{}' ".format(task_id))
        with open('./code/SIMI/SIMIConfCentral','w') as f:
            for row in cur.execute("select client_name,client_ip, client_port, server_port from jobs  where task_id = '{}' ".format(task_id)):
               f.write('{} {} {}\n'.format(row[0],row[1],row[2]))

    con.commit()
    con.close()

   
    run_R("SIMI/SIMIScriptCentral.R",task_id)


    return


@app.route('/start_job', methods=['POST'])
def start_job():
    message=''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        message =  'Content-Type not supported!'
        return  jsonify ({"message":message})

    print(json)
    task_id = json['task_id']
    print(task_id)
    client_ip = json['client_ip']
    client_port= json['client_port']

    con = sqlite3.connect('controller.db')
    cur = con.cursor()
    message = ''

    cur.execute("select * from jobs where task_id = '{}' and client_ip = '{}'".format(task_id, client_ip))
    row = cur.fetchone()
    if row is None:
        message = 'No such job found'
    else:
        cur.execute("update jobs set status = 'running' where task_id = '{}' and client_ip = '{}'".format(task_id, client_ip))
        message = 'Job set to run'
    con.commit()
    con.close()
    
    start_central(task_id)

    json['message'] = message
    return  jsonify (json)




@app.route('/read_tasks', methods=['POST'])
def read_tasks():
    con = sqlite3.connect('controller.db')
    cur = con.cursor()
    df = pd.read_sql_query("SELECT task_id, total_remote_sites as total_planned_remote_sites, registered_remote_sites as acknowledged_remote_sites,method ,imputed_datasets, missing_variables,model , iteration_between_imputation ,iteration_until_first_imputation , server_ip as central_public_ip, server_port_from as central_public_port_from, job_creation_dttm from tasks", con)
    result = df.to_json(orient="records")
    con.close()
    return jsonify ( {'data': result})


@app.route('/read_task/<task_id>')
def read_task(task_id):
    con = sqlite3.connect('controller.db')
    df = pd.read_sql_query("SELECT * FROM tasks where task_id = '{}'".format(task_id), con)
    con.close()
    return  jsonify ({'task_id':task_id,'data': df.to_json(orient="index")})

@app.route('/read_job/<task_id>')
def read_job(task_id):
    con = sqlite3.connect('controller.db')
    df = pd.read_sql_query("SELECT client_name as remote_site, client_ip as remote_site_public_ip, client_port as remote_site_public_port, server_port as central_site_public_port FROM jobs where task_id = '{}'".format(task_id), con)
    con.close()
    return  jsonify ({'task_id':task_id,'data': df.to_json(orient="index")})


@app.route('/read_jobs')
def read_jobs():
    con = sqlite3.connect('controller.db')
    cur = con.cursor()
    messages=''
    for row in cur.execute('SELECT * FROM jobs'):
        print (row)
        messages = messages + '{} - {} - {} - {} - {}'.format(row[0],row[1],row[2],row[3],row[4]) + '<br>'
    con.commit()
    con.close()
    return messages
 
@app.route('/display/<path>/<filename>')
def display_image(path,filename):
        #print('display_image filename: ' + filename)
        return redirect(url_for('custom_output', filename=path +'/' + filename), code=301)

# Custom static data
@app.route('/custom_output/<path:filename>')
def custom_output(filename):
    return send_from_directory(app.config['custom_output_PATH'], filename)

#  Check job status Summary
@app.route('/status_summary/<session_id>')
def check_status_summary(session_id):
        return jsonify({'session_id': session_id})




#  Check job status
@app.route('/status/<session_id>')
def check_status(session_id):
        return jsonify({'session_id': session_id})



if __name__ == "__main__":
    app.run( host='0.0.0.0',port=80)
