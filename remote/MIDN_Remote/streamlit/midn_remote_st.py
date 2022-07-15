
import streamlit as st
import datetime,os,time,psutil
from streamlit import session_state
import json
from app import app
import requests


with open('config.json', 'r') as f:
    config = json.load(f)


st.title( "MIDistNet Remote Site Management Tools")

st.header('MIDistNet Remote site configure information')

client_name = st.text_input('Remote site name:', config['host_name'])
server_app_addr =   st.text_input('Central Site Web Applicaiton URL:', config['server_app'])
if config['remote_public_ip'] == '127.0.0.1':
    config['remote_public_ip'] = app.config['public_ip']
remote_public_ip =   st.text_input('remote public IP address:', config['remote_public_ip'])
save_config_clicked  = st.button('Save configuration')

if save_config_clicked: 
    config['host_name'] = client_name.strip()
    config['server_app'] = server_app_addr.strip()
    config['remote_public_ip'] = remote_public_ip.strip()
    with open('config.json', 'w') as f:
        json.dump(config, f)


st.header('MIDistNet Remote Site Job')

if 'task_id' not in st.session_state:
    st.session_state['task_id'] = ''

if 'task_detail' not in st.session_state:
    st.session_state['task_detail'] = {}

if 'server_data' not in st.session_state:
    st.session_state['server_data'] = {}

task_id = st.text_input('task_id').strip()
client_ip = st.text_input('Remote Site Public IP:', remote_public_ip)
client_port = st.text_input('Remote Site Public Port:',  app.config['client_port'])

get_task_id_clicked = st.button('Get Task Detail')
if get_task_id_clicked and len(task_id) > 10:
    post_curl = '{}/read_task/{}'.format(server_app_addr,task_id)
    r = requests.get(post_curl)
    r_json = json.loads(r.json()['data'])
    if len(r_json) == 0 :
        st.write("Task does not exist")
        st.session_state['task_id']  = ''
    else:
        task_detail =  r_json['0']
        st.session_state['task_id'] = task_detail['task_id']
        st.session_state['task_detail'] = task_detail
#        st.write (task_detail)
if  st.session_state['task_id'] != '':
        task_detail = st.session_state['task_detail']
        st.write("Task ID: ", task_detail['task_id'])
        st.write("Total planned Remote Sites: ", str(task_detail["total_remote_sites"]))
        st.write("Acknowledged Remote Sites :", str(task_detail["registered_remote_sites"]))
        st.write("Method: ", task_detail["method"])
        st.write("Missing variables in column: " ,  task_detail["missing_variables"])
        st.write("Model: ", task_detail["model"])
#        st.write("Task Status: ", task_detail["status"])
        st.write("Central Site Public IP: ", task_detail["server_ip"])
#        st.write("Central Site Public Port: ", task_detail["server_port_from"])

regisiter_button = st.button('Acknowledge')

if regisiter_button :        
    if len(task_id) > 10 : 
        jsondata = {'task_id':task_id,
            'client_ip':client_ip,
            'client_port':client_port,
            'client_name':client_name 
           }
        r_reg = requests.post(server_app_addr+'/register', json=jsondata)
        st.session_state['server_data'] = r_reg.json() 
#        st.write(st.session_state['server_data'])
        st.write(r_reg.json()['message'])

data_file = './data/dummy.txt'
uploaded_file = st.file_uploader("Specify local file")


if uploaded_file is not None:
    data_file = './data/' + client_ip + '_' + client_port + '_' + uploaded_file.name
    with open(data_file,"wb") as f:
         f.write(uploaded_file.getbuffer())

cols_1 = st.columns(6)

run_button = cols_1[1].button('Run')
refresh_button = cols_1[2].button('Refresh')
stop_button = cols_1[3].button('Stop')
clear_all_R = cols_1[4].button('Kill All R porcess')
cols_1[0].write('Remote job:')

status_placeholder = st.empty()
status_text  = status_placeholder.text_area('Runing Status', value=f' ',key='Status', disabled =  True )


import subprocess

if 'pid' not in st.session_state:
    st.session_state['pid'] = None

def run_command(args):

    status_text  = status_placeholder.text_area('Runing Status', value=f"Running '{' '.join(args)}'",key='Status', disabled =  True )

    running_logs  =  open(st.session_state['log_file'], 'w')
    st.session_state['log'] = running_logs

    p = subprocess.Popen(args, cwd="./code/",shell=False, stdout=running_logs,stderr=running_logs) # subprocess.PIPE

    st.session_state['pid'] = p

    stdout=None
    stderr=None
    time.sleep(2)

    try:
        stdout, stderr = p.communicate(timeout = 2)
    except:
        display_text = f"Running '{' '.join(args)}' \n" 
        display_text += ' Job with PID {} is runing at background \n'.format(p.pid)
        if stdout :
            display_text += stdout.decode('utf-8') + '\n'
        if stderr :
            display_text += stderr.decode('utf-8') + '\n'
        status_text  = status_placeholder.text_area('Runing Status', value=display_text ,key='Status', disabled =  True )
    else:
        display_text  = 'Job Finished \n'
        if stdout :
            display_text += stdout.decode('utf-8') + '\n'
        if stderr :
            display_text += stderr.decode('utf-8') + '\n'
        log_text=''
        if st.session_state['log']:
            st.session_state['log'].flush()
            with  open(st.session_state['log_file'], 'r') as f:
                log_text = f.read()
        display_text = ' Job with PID {} was aborted unexpected \n Click stop to clear it. \n {} '.format(st.session_state['pid'].pid,log_text)
        status_text  = status_placeholder.text_area('Runing Status', value=display_text ,key='Status', disabled =  True )


#    try:
#        result.check_returncode()
#        status_text  = status_placeholder.text_area('Runing Status', value= result.stdout ,key='Status',  disabled =  True )
#    except subprocess.CalledProcessError as e:
#        status_text  = status_placeholder.text_area('Runing Status', value= result.stderr ,key='Status', disabled =  True )
#        raise e

def run_command_debug(args):
    status_placeholder = st.empty()
    status_text  = status_placeholder.text_area('Runing Status', value=f"Running '{' '.join(args)}'",key='Status', disabled =  True )

    result = subprocess.run(args, cwd="./code/", capture_output=True, text=True)
    st.session_state['pid'] = result

    try:
        result.check_returncode()
        status_text  = status_placeholder.text_area('Runing Status', value= result.stdout ,key='Status',  disabled =  True )
    except subprocess.CalledProcessError as e:
        status_text  = status_placeholder.text_area('Runing Status', value= result.stderr ,key='Status', disabled =  True )
#        raise e

 
if run_button :

# this is not working
#    if debug_option:
#        refresh_button.enabled = False
#        stop_button.enabled = False
        

    R_runtime_file =  client_ip + '_' + client_port + '_r_runtime.R' 

    if  'ICE' in st.session_state['server_data']['core_function'] :
        R_func_str = """

source("{method}/{method}Remote.R")
args = commandArgs(trailingOnly=TRUE)
X=as.matrix(read.table(file=args[1]))
colnames(X) <- NULL

{method}Remote(X,"{client_port}","{server_ip}","{server_port}")

    """.format(method =  st.session_state['server_data']['core_function'],
        client_port =  st.session_state['server_data']['client_port'],
        server_ip =  st.session_state['server_data']['server_ip'],
        server_port =  st.session_state['server_data']['server_port']
        )

    else:
        R_func_str = """

source("{method}/{method}Remote.R")
args = commandArgs(trailingOnly=TRUE)

X=as.matrix(read.table(file=args[1]))
colnames(X) <- NULL

{method}Remote(X,{missing},"{client_port}","{server_ip}","{server_port}")

    """.format(method =  st.session_state['server_data']['core_function'],
        missing =   st.session_state['server_data']['missing_variables'],
        client_port =  st.session_state['server_data']['client_port'],
        server_ip =  st.session_state['server_data']['server_ip'],
        server_port =  st.session_state['server_data']['server_port']
        )


    with open('./code/'+R_runtime_file,"w") as f:
         f.write(R_func_str)

#    st.write(R_func_str)

#    if debug_option:
#        run_command_debug(['Rscript','--vanilla', R_runtime_file, '../'+ data_file])
#    else:

    log_file = './code/{}.txt'.format(R_runtime_file)
    st.session_state['log_file'] = log_file

    run_command(['Rscript','--vanilla', R_runtime_file, '../'+ data_file]) 

if refresh_button:
  if st.session_state['pid'] :
    stdout=None
    stderr=None

    try:
        stdout, stderr = p.communicate(timeout = 1 )
    except:
        proc = psutil.Process(st.session_state['pid'].pid)
#        st.write( proc.status())
        if proc.status() == psutil.STATUS_ZOMBIE:
            if st.session_state['log']:
                 st.session_state['log'].flush()
            log_text=''
            with  open(st.session_state['log_file'], 'r') as f:
                log_text = f.read()
            display_text = ' Job with PID {} was aborted unexpected \n Click stop to clear it. \n {} '.format(st.session_state['pid'].pid,log_text)
        else:    
          display_text = ' Job with PID {} is runing at background \n'.format(st.session_state['pid'].pid)
          if stdout :
            display_text += stdout.decode('utf-8') + '\n'
          if stderr :
            display_text += stderr.decode('utf-8') + '\n'
        status_text  = status_placeholder.text_area('Runing Status', value=display_text ,key='Status', disabled =  True )
    else:
        display_text  = 'Job Finished \n'
        if stdout :
            display_text += stdout.decode('utf-8') + '\n'
        if stderr :
            display_text += stderr.decode('utf-8') + '\n'
        status_text  = status_placeholder.text_area('Runing Status', value=display_text ,key='Status', disabled =  True )

def findandKillProcessIdByName(processName):
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # print(pinfo)
           # Check if process name contains the given name string.
           if processName == pinfo['name']  :
               listOfProcessObjects.append(pinfo['pid'])
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    for x in listOfProcessObjects:
        p_R = psutil.Process(x)
        p_R.kill()
    return listOfProcessObjects;
   
if clear_all_R:
    findandKillProcessIdByName('R')
   
if  stop_button :
    if st.session_state['pid'] :
        status_text  = status_placeholder.text_area('Runing Status', value="Stopped process with pid: {}".format(st.session_state['pid'].pid) ,key='Status', disabled =  True )
#        st.write("Stopped process with pid:", st.session_state['pid'].pid )
        st.session_state['pid'].kill()
        st.session_state['pid'] = None

