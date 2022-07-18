
1. Prerequisite:
   
   Please refer to  https://docs.docker.com/get-docker/ to install docker service on your testing machine.


2. Pull the latest docker images:

    The docker images have been commited to dockerhub
    
    run the below commands to get the latest program update:
    ```
    #On Central Machine:
    sudo docker pull luyaochen/midn_central:latest
    
    #On Remote Machine
    sudo docker pull luyaochen/midn_remote:latest
    ```

3. Plan the networking

   Before setup the network, we need to determine the some network information:
   
   Here is a sample to be used for a 1 central + 1 remote experientment
   
   **For Central Machine:** 
   
   Local IP address: 192.168.0.23
   Port listening for web application / MIDN Central Controller: 443 
   Port listening for MIDN Computing: 6600 - 6700
   
   Public IP: 129.103.12.18 
   Port listening for web application: 5443 
   Port listening for MIDN Computing: 6600 - 6700   ( depends on how many remote sites paticipanted. In this sample, we open 6600 only)
   
   **For Remote Machine: **
   
   Local IP address: 192.168.1.15
   Port listening for MIDN Remote Controller: 80 
   Port listening for MIDN Computing: 6000  
   
   Public IP: 202.18.15.63
   Port listening for MIDN Computing: 6000   ( Remote site with different public IP address can use the same port)
   
   
4. Create and run dokcer container on  central site machine
     ```
     # create and start a docker container to run the central site applications
     sudo docker run  -it -d -p 443:443 -p 6600-6700:6600-6700 --name=midn_central luyaochen/midn_central
     ```    
    
    The central site MIDN Controller can be accessed by:
    
    https://192.168.0.23/midn_central/
    
    (The SSL certification is local signed for testing, please ignore the error when enter this URL )

     <picture>
     <img alt="Screen capture of central machine inital login in." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_Ini.JPG" width="60%" height="60%">
 
     </picture>
     
5. Create and run dokcer container on remote site machine
   ```  
    sudo docker run  -it -d -p 80:80 -p 6000:6000 --name=midn_remote luyaochen/midn_remote
   ```    
   
     The remote site MIDN Controller can now be accessed by:

       http://192.168.1.15   

     There is a onetime setup on remote site:

        <picture>
        <img alt="Screen capture of onetime remote site setup." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Remote_Config.JPG"  width="60%" height="60%">
        </picture>

      The below information is reuiqred:

      Remote Site name  - To idenfiry the site name

      Central Site Web Applicaiton URL: The public IP address and port of the central mahine

      Remote site public IP address: The program will try to idenfify the public IP address. But, if it is not accurate, manual update is reuqired.
    
6. Add a task on central site machine
   
   By clicking "Refresh" under the "Task list", we can find and list the detail of tasks registired 
   
    <picture>
     <img alt="Screen capture of task list." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_task_admin_1.JPG"  width="60%" height="60%">
     </picture>    
    
   
   To add a new task, enter all the computation parameters.
     <picture>
     <img alt="Screen capture of add a task." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_task_admin_2.JPG"  width="60%" height="60%">
     </picture>       
      
   A task ID will be genereated. The central site need to send this ID to all remote site for there acknowledgement (eg, by email the task ID to remote sites.).
 
 * Acknowledge a task on remote site machine
   
   By entering the "task id" and clicking "Get Task Detail", the remote side get read the task detail; by enter the remote site public IP address and port, the remote site acknowledges the task.
   
   Note: the remote must "Acknowledge" (again) before running the job, even they had acknowledged before.
      
    <picture>
     <img alt="Screen capture of acknowledge a task." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Remote_job.JPG"  width="60%" height="60%">
     </picture> 
   
   By uploadin a data file, the remote site can run the remote job. There is an explnation of all the buttons:
   
   Run - start a remote site job. User must click "Acknowledge" before run the job each time.
   
   Refresh - Get the status of current job.
   
   Stop - Stop the job
   
   Kill all R process -  Kill all runnning R programs. It is userful of the screen get refreshed or quite when a job is running (in this case, we lost the track of process ID and have to kill all R process). 
   
 7. Run the job on central site machine
   
   Once all remote sites acknowledge the task and start their job, central site can run the job by uploading its own file.
   After job finising, the central site can download the zipped result sets.

   <picture>
   <img alt="Screen capture of central job." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_job.JPG"  width="60%" height="60%">
   </picture> 
   
   
