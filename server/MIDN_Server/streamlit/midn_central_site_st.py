import streamlit as st
import pandas as pd
import numpy as np
import datetime
from streamlit import session_state
import json
import uuid
from app import app
import requests
import os, glob
import zipfile


import socket
 

st.title ( "MIDistNet Central Site Management Tools")

from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=False, enableValue=True, enablePivot=False
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection



# task_selected = aggrid_interactive_table(df=)

#if selection:
#    st.write("You selected:")
#    st.json(selection["selected_rows"])



with st.expander("MIDistNet Task Admintration"):

    if 'missing_val_model' not in st.session_state:
        st.session_state['missing_val_model'] = {}

    st.caption("Central Host container local IP: {}".format(app.config['server_ip']))
    st.caption("Central Host public IP: {}   (The public IP address may not be accurate due to local IT policy)".format(app.config['public_ip']))

    st.header('Task list')
    
# https://share.streamlit.io/streamlit/example-app-interactive-table/main 
    refresh_clicked = st.button('Refresh' )
    r = requests.post('{}/read_tasks'.format( app.config['server_app']), verify=False)
    r_data = json.loads(r.json()['data'])
    df = pd.DataFrame(r_data)
    task_selected = aggrid_interactive_table(df=df)

    if len(task_selected["selected_rows"])> 0 :
        st.write("You selected:",task_selected["selected_rows"][0]["task_id"])
        deletet_task_clicked = st.button('Delete Task' )
        if deletet_task_clicked:
            post_curl = '{}/delete_task/{}'.format(app.config['server_app'],task_selected["selected_rows"][0]["task_id"])
            r = requests.get(post_curl, verify=False)
            r_json = json.loads(r.json()['message'])
            if r_json = 'Task Deleted':
                st.write("Task Deleted")
        st.write("Acknowledged remote sites:")
        rj = requests.get('{}/read_job/{}'.format( app.config['server_app'],task_selected["selected_rows"][0]["task_id"]), verify=False)
        rj_data = json.loads(rj.json()['data'])
        df_job = pd.DataFrame(rj_data).T
        st.write(df_job)


#    with st.form(key='new_task_form_1'):
    if 1 == 1:
        task_id_placeholder = st.empty()
#        new_task_id_clicked = st.form_submit_button('Generatea a new task ID')
#       if new_task_id_clicked:

        task_id = task_id_placeholder.text_input('Task Id',value='',disabled = True, key='task_id')
        
        method = st.selectbox('Method',['AVGMMI','AVGMMICE','CSLMI','CSLMICE','IMI','IMICE','SIMI','SIMICE'],key='method')

        iteration_until_first_imputation=0
        iteration_between_imputation = 0
        total_remote_sites= 1
        server_ip= app.config['server_ip']
        server_port_from=app.config['server_port_from']

        if method not in ('IMI','IMICE'): 

            cols_1 = st.columns(4)
            total_remote_sites = cols_1[0].number_input('Total Remote Sites',key='total_remote_sites',value = 1 )
            server_ip = cols_1[1].text_input('Central Site Public IP',key='server_ip',value = app.config['public_ip'] )
            server_port_from = cols_1[2].text_input('Public Port from',key='server_port_from',max_chars = 5,value = app.config['server_port_from'] )

        cols_2 = st.columns(4) 
        impute_datasets = cols_2[0].number_input('Imputed Datasets Output',key='impute_datasets',value = 10)
        
        if 'ICE' in  method :
            missing_variables = cols_2[1].multiselect('Missing Variables',[str(x) for x in range(1,21)], key='missing_variables')
        else :
            missing_variable =  cols_2[1].selectbox('Missing Variables',[str(x) for x in range(1,21)], key='missing_variables')
            missing_variables = [missing_variable]
#        model = cols_2[3].multiselect('Model',["Gaussian" for x in range(5)]+[ "logistic" for x in range(5)], key='model')

#        st.session_state['missing_val_model']
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        for xx in list(st.session_state['missing_val_model']):
            if xx not in missing_variables:
                 del st.session_state['missing_val_model'][xx]

        for xx in missing_variables:
            val_label = 'Missing variable {} model'.format(xx)
            val_key = 'model_'+xx
            if  xx in st.session_state['missing_val_model']:
                if  st.session_state['missing_val_model'] [xx] == "Gaussian":
                    selected_index = 0
                else:
                    selected_index = 1
                st.session_state['missing_val_model'][xx] = st.radio(val_label,options=["Gaussian","logistic"], index = selected_index,key=val_key)
            else:
                st.session_state['missing_val_model'][xx] = st.radio(val_label,options=["Gaussian","logistic"], key=val_key)
    
        if 'ICE' in  method :

            cols_3 = st.columns(4)
            iteration_between_imputation = cols_3[0].number_input('Iteration between Imputation',key='iteration_between_imputation',value = 10 )
            iteration_until_first_imputation = cols_3[1].number_input('Iteration until first imputation',key='iteration_until_first_imputation',value = 20 )

        model=[]
        for xx in missing_variables:
            model.append( st.session_state['missing_val_model'][xx])

        submitted = st.button('Add A new Task' )

        if  submitted :
            if not task_id:
                task_id = str(uuid.uuid4())
                task_id_placeholder.text_input('Task Id',value=task_id,disabled = True, key='task_id')

            new_task_info  = {
                'task_id':task_id,
                'total_remote_sites':total_remote_sites,
                'method': method,
                'impute_datasets':impute_datasets,
                'missing_variables': ','.join(missing_variables),
                'model': ','.join(model),
                'iteration_until_first_imputation':iteration_until_first_imputation,
                'iteration_between_imputation':iteration_between_imputation,
                'server_ip': server_ip,
                'server_port_from':server_port_from,
                'job_creation_dttm': datetime.datetime.now()
            }
            new_task_info = json.dumps(new_task_info,indent = 4, default=str) 
            post_curl = '{}/init'.format(app.config['server_app'])
            r = requests.post(post_curl,data=new_task_info, verify=False)            
            r_json = r.json()
            st.write(r_json['message'])


with st.expander("Central Site Job Management"):

    st.header('MIDistNet Central Site Job')

    if 'task_detail' not in st.session_state:
        st.session_state['task_detail'] = {}

    if 'run_status' not in st.session_state:
        st.session_state['run_status'] = False


    task_id = st.text_input('task_id').strip()

    get_task_id_clicked = st.button('Get Task Detail')
    if get_task_id_clicked and len(task_id) > 10:
        post_curl = '{}/read_task/{}'.format(app.config['server_app'],task_id)
        r = requests.get(post_curl, verify=False)
        r_json = json.loads(r.json()['data'])
        if len(r_json) == 0 :
            st.write("Task does not exist")
            st.session_state['task_id']  = ''
        else:
            task_detail =  r_json['0']
            st.session_state['task_detail'] = task_detail
#            st.write (task_detail)
    if  len( st.session_state['task_detail']) > 0 :
        task_detail = st.session_state['task_detail']
        st.write("Task ID: ", task_detail['task_id'])
        st.write("Total Planned Remote Sites: ", str(task_detail["total_remote_sites"]))
        st.write("Acknowledged Remote Sites :", str(task_detail["registered_remote_sites"]))
        st.write("Method: ", task_detail["method"])
        st.write("Missing variables in column: " ,  task_detail["missing_variables"])
        st.write("Model: ", task_detail["model"])
        st.write("Task Status: ", task_detail["status"])
        st.write("Central Site Public IP: ", task_detail["server_ip"])
#        st.write("Central Site Public Port: ", task_detail["server_port_from"])


    data_file = './data/dummy.txt'
    uploaded_file = st.file_uploader("Specify local data file")


    if uploaded_file is not None:
        data_file = './data/' +  uploaded_file.name
        with open(data_file,"wb") as f:
             f.write(uploaded_file.getbuffer())

    run_button = st.button('Run')


    import subprocess

    def run_command(args):

        status_placeholder = st.empty()
        status_text  = status_placeholder.text_area('Runing Status', value=f"Running '{' '.join(args)}'",key='Status', disabled =  True )
    
        result = subprocess.run(args, cwd="./code/", capture_output=True, text=True)

        try:
            result.check_returncode()
            status_text  = status_placeholder.text_area('Runing Status', value= result.stdout ,key='Status',  disabled =  True )
            st.session_state['run_status'] = True
        except subprocess.CalledProcessError as e:
            st.session_state['run_status'] =  False
            status_text  = status_placeholder.text_area('Runing Status', value= result.stderr ,key='Status', disabled =  True )
    #        raise e


    if run_button :

      if  st.session_state['task_detail']['total_remote_sites'] != st.session_state['task_detail']['registered_remote_sites'] and  not st.session_state['task_detail']['method'].startswith('IMI') :
        st.write("Not all remote sites acknowledged!")

      else:
        r = requests.get('{}/read_task_jobs/{}'.format( app.config['server_app'],task_id), verify=False)
        r_data = json.loads(r.json()['data'])
        df = pd.DataFrame(r_data)

        for filename in glob.glob("./data/Result_*"):
            os.remove(filename) 

        client_ports = []
        server_ports = []
        client_ips = []
        for index,row in df.iterrows():
            client_ports.append('"{}"'.format(row.client_port))
            client_ips.append('"{}"'.format(row.client_ip))
            server_ports.append('"{}"'.format(row.server_port))
        client_ports = 'c(' +  ", ".join(client_ports) + ')'
        client_ips =  'c(' + ", ".join(client_ips) + ')'
        server_ports = 'c(' + ", ".join(server_ports)  + ')'

        if ',' in   st.session_state['task_detail']['model'] :
            model_list =  [ '"{}"'.format(x) for x in st.session_state['task_detail']['model'].split(',') ]
            models =  "c({})".format ( ', '.join(model_list))
        else:
            models =  '"{}"'.format( st.session_state['task_detail']['model'])

        if ',' in   st.session_state['task_detail']['missing_variables'] :
            missing_variables =  'c(' +  ', '.join( st.session_state['task_detail']['missing_variables'].split(',')) + ')'
        else:
            missing_variables =  st.session_state['task_detail']['missing_variables'] 

        R_runtime_file = 'server_r_runtime.R'

        if 'ICE' in  st.session_state['task_detail']['method']:
            
            if  st.session_state['task_detail']['method'] == 'IMICE':

                R_func_str = """

source("{method}/{method}Central.R")

args = commandArgs(trailingOnly=TRUE)
X=as.matrix(read.table(file=args[1]))
colnames(X) <- NULL

imp = {method}Central(X,{imputes},{missing},{model}, {iteration_between_imputation}, {iteration_until_first_imputation})

#options(max.print=1000000)
#print(imp)

for (i in 1:length(imp)) {{
  write.table(imp[i],file= paste('../data/','Result_',i,'.txt', sep=""))
}}

            """.format(method =  st.session_state['task_detail']['method'],
                imputes =  st.session_state['task_detail']['imputed_datasets'],
                missing  =  missing_variables,
                model  =  models,
                iteration_until_first_imputation = st.session_state['task_detail']['iteration_until_first_imputation'],
                iteration_between_imputation = st.session_state['task_detail']['iteration_between_imputation']
                )


            else:

                R_func_str = """

source("{method}/{method}Central.R")

args = commandArgs(trailingOnly=TRUE)
X=as.matrix(read.table(file=args[1]))
colnames(X) <- NULL

imp = {method}Central(X,{imputes},{missing},{model}, {iteration_between_imputation}, {iteration_until_first_imputation},{client_ips},{client_ports},{server_ports})

#options(max.print=1000000)
#print(imp)

for (i in 1:length(imp)) {{
  write.table(imp[i],file= paste('../data/','Result_',i,'.txt', sep=""))
}}

            """.format(method =  st.session_state['task_detail']['method'],
                imputes =  st.session_state['task_detail']['imputed_datasets'],
                missing  =  missing_variables,
                model  =  models,
                iteration_until_first_imputation = st.session_state['task_detail']['iteration_until_first_imputation'],
                iteration_between_imputation = st.session_state['task_detail']['iteration_between_imputation'],
                client_ports = client_ports,
                client_ips = client_ips,
                server_ports = server_ports
                )

        else:
            if st.session_state['task_detail']['method'] == 'IMI':

                R_func_str = """
source("{method}/{method}Central.R")

args = commandArgs(trailingOnly=TRUE)
X=as.matrix(read.table(file=args[1]))
colnames(X) <- NULL

imp = {method}Central(X,{imputes},{missing},{model})

#options(max.print=1000000)
#print(imp)

for (i in 1:length(imp)) {{
  write.table(imp[i],file= paste('../data/','Result_',i,'.txt', sep=""))
}}

            """.format(method =  st.session_state['task_detail']['method'],
                imputes =  st.session_state['task_detail']['imputed_datasets'],
                missing  =  missing_variables,
                model  =  models
                )



            else:

                R_func_str = """
source("{method}/{method}Central.R")

args = commandArgs(trailingOnly=TRUE)
X=as.matrix(read.table(file=args[1]))
colnames(X) <- NULL

imp = {method}Central(X,{imputes},{missing},{model},{client_ips},{client_ports},{server_ports})

#options(max.print=1000000)
#print(imp)

for (i in 1:length(imp)) {{
  write.table(imp[i],file= paste('../data/','Result_',i,'.txt', sep=""))
}}

            """.format(method =  st.session_state['task_detail']['method'],
                imputes =  st.session_state['task_detail']['imputed_datasets'],
                missing  =  missing_variables,
                model  =  models,
                client_ports = client_ports,
                client_ips = client_ips,
                server_ports = server_ports
                )


        with open('./code/'+R_runtime_file,"w") as f:
             f.write(R_func_str )

        #st.write(R_func_str)
        run_command(['Rscript','--vanilla', R_runtime_file, '../'+ data_file])

        if st.session_state['run_status'] :
          with zipfile.ZipFile('./data/result.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir('./data'):
                f = os.path.join('./data', filename)
                if os.path.isfile(f) and 'Result' in f:
                    zipf.write(f)
          with open("./data/result.zip", "rb") as fp:
            btn = st.download_button(
                label="Download result ZIP",
                data=fp,
                file_name="result.zip",
                mime="application/zip"
                )
    else:
        st.write('click to run the job')

