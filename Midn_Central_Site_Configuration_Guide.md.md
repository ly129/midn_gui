
1. Prerequisite:
   
   Docker is the only software required to run the GUI version of MIDN network. 
   
      [Install Docker](Prerequisite_Docker.MD)
   

2. Plan the central site network

   * To run the central site of a MIDN network, the site must expose two type of the ports to the public internet:
   
      * API port - The API is used for central and remote site(s) to exchange the information of computation protocol and network setup.

      * MIDN network port - The central site has one dedicate port to listen to each remote site. Thus, if there are 10 remote sites involved in computation, the central site needs 10 computation ports open to public.

   
    * There are 3 IP addresses are involved in the networking   
        
       *   The public IP address:  The remote site will use the central site public IP address to communicate with central site

       *   The central site machine host IP address:  This is the IP address of the machine running the Docker. The user on the central site will use this IP address to access the GUI application 
       
       *   The Docker container IP address: While running the MIDN Central site, the Docker will create a container (instance) to run the application. There is an internal IP address was assigned to this container. Unless we try the MIDN network central and remote sites on the same host (this scenario will be explained in a separate document), this IP address is transparent to the users.

    * Here is a sample to be used for a 1 central site + 1 remote site experiment. The IP address (not real, for the purpose of explanation only) in this diagram will be used in the below configuration. 
   
      <picture>
      <img alt="Sample network diagram" src="https://github.com/Luyaochen1/midn_gui/blob/main/MIDN%20Netwok%20Diagram.png">

      </picture>   
     
       **For Central site Machine:** 

      Local IP address: 192.168.0.23

      Port listening for MIDN Central Controller: 5080 (open to local only)

      Port listening for MIDN Computing: 6600 - 6700
      
      Public IP: 129.103.12.18 

      Port listening for API: 5443 (firewall / router will forward 5443 to port 5443 of 192.168.0.23)
      
      Central site API URL: https://129.103.12.18:5443   
      
      (the remote site(s) requires this URL to acknowledge a task)

      Port listening for MIDN Computing: 6600 - 6700   (depends on how many remote sites participated. In this sample, we open 6600 only as there is only one remote site)


3. Pull the latest docker images:

    The docker images have been commited to dockerhub
    
    run the below commands to get the latest program update:
    ```
    # On the Central site Machine:
    docker pull luyaochen/midn_central:latest
    ```   
    On Linux machine, you may need to add "sudo" in front of the command. 
        
4. Create and run a Docker container on central site machine

     ```
     # create and start a Docker container to run the central site applications
     docker run  -it -d -p 5443:443 -p 5080:80  -p 6600-6700:6600-6700 --name=midn_central luyaochen/midn_central
     
     ```    
    
    The central site MIDN Controller can be accessed by:
    
    http://192.168.0.23:5080
    

     <picture>
     <img alt="Screen capture of central machine inital login in." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_Ini.JPG" width="60%" height="60%">
 
     </picture>
     
     
5. Add a task on central site machine
   
   By clicking "Refresh" under the "Task list", we can find and list the detail of tasks registired 
   
    <picture>
     <img alt="Screen capture of task list." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_task_admin_1.JPG"  width="60%" height="60%">
     </picture>    
    
   
   To add a new task, enter all the computation parameters.
     <picture>
     <img alt="Screen capture of add a task." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_task_admin_2.JPG"  width="60%" height="60%">
     </picture>       
      
   A task ID will be generated. The central site need to send (e.g. by email) this ID (with the public IP address and API port of central site machine ) to all remote sites for their acknowledgement.

 
6. Before starting the central site computation, the central site needs to wait for all remote sites to acknowledge the task and start their remote job.
   
  
7. Run the job on central site machine
   
      Once all remote sites acknowledge the task and start their job, central site can run the job by uploading its own file.
      After job finished, the central site can download the zipped result sets.

      <picture>
      <img alt="Screen capture of central job." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_job.JPG"  width="60%" height="60%">
      </picture>

   
