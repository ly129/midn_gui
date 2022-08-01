1. Prerequisite:
   
   Docker is the only software required to run the GUI version of MIDN network. 
   
      [Install Docker](Prerequisite_Docker.MD)
   

2. Plan the Remote site network

   * To run the remote site of a MIDN network, the site must expose one port to the public internet (the remote site may setup the firewall that only central site can access this port ):
    
   * There are 3 IP addresses are involved in the networking   
    
       *   The public IP address:  The cental site will use the remote site public IP address to communicate with remote site for computation 

       *   The remote site machine host IP address:  This is the IP address of the machine running the Docker. The user on the remote site will use this IP address to access the GUI application 
       
       *   The Docker container IP address: While running the MIDN remote site, the Docker will create a container (instance) to run the application. There is an internal IP address was assigned to this container. Unless we try the MIDN network central and remote sites on the same host (this scenario will be explained in a separate document), this IP address is transparent to the users.

    * Here is a sample to be used for a 1 central site + 1 remote site experiment. The IP address (not real, for the purpose of explanation only) in this diagram will be used in the below configuration. 
   
      <picture>
      <img alt="Sample network diagram" src="https://github.com/Luyaochen1/midn_gui/blob/main/MIDN%20Netwok%20Diagram.png">

      </picture>   
     
    **For Remote Site Machine:** 
   
      Local IP address: 192.168.1.15

      Port listening for MIDN Remote Controller: 5080 

      Port listening for MIDN Computing: 6000  

      Public IP: 202.18.15.63

      Port listening for MIDN Computing: 6000   

4. Pull the latest docker images:

    The docker images have been commited to dockerhub
    
    run the below commands to get the latest program update:
    ```
    #On Remote Machine
    docker pull luyaochen/midn_remote:latest
    ```
   On a Linux machine, you may need to add "sudo" in front of the command.

   All Docker command needs to run in a command line ( or Terminal) window. 

   For windows: https://www.dell.com/support/kbdoc/en-in/000130703/the-command-prompt-what-it-is-and-how-to-use-it-on-a-dell-system

   For Mac:  https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac

      
5. Create and run dokcer container on remote site machine
   ```  
    sudo docker run  -it -d -p 5080:80 -p 6000:6000 --name=midn_remote luyaochen/midn_remote
   ```    
   
     The remote site MIDN Controller can now be accessed by:

       http://192.168.1.15:5080   

     After entered the above URL, there is a onetime setup on remote site:

        <picture>
        <img alt="Screen capture of onetime remote site setup." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Remote_Config.JPG"  width="60%" height="60%">
        </picture>

      The below information is reuiqred:

      Remote Site name  - To idenfiry the site name

      Central Site Web Applicaiton URL: The public IP address and port of the central mahine  (in this sample -  https://129.103.12.18:5443 )

      Remote site public IP address: The program will try to idenfify the public IP address. But, if it is not accurate, manual correction is reuqired.
    
  
6. Acknowledge a task on remote site machine
   
   The remote side need the task ID to acknowledge a task and start a remote job.
   
   By entering the "task id" and clicking "Get Task Detail", the remote side get the task detail; by entering the remote site public IP address and port, the remote site acknowledges the task.
   
   Note: if the remote site refresh the screen, the remote must "Acknowledge" (again) before running a job, even they had acknowledged before.
      
    <picture>
     <img alt="Screen capture of acknowledge a task." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Remote_job.JPG"  width="60%" height="60%">
     </picture> 
   
   By uploadin a data file, the remote site can run the remote job. There is an explnation of all the buttons:
   
   * Run - start a remote site job. User must click "Acknowledge" before run the job each time.
   
   * Refresh - Get the status of current job.
   
   * Stop - Stop the job
   
   * Kill all R process -  Kill all runnning R programs. It is userful if the screen is refreshed or quite while a job is running (in this case, we lost the track of process ID and have to kill all R process). 
   
 
7. Other useful Docker commands
 
     ```
    # to stop a remote site Docker container 
    docker stop  midn_remote
    
    # to start a remote site Docker container 
    docker start  midn_remote
    
    # to remove a remote site Docker container ( in case you need to recreate it. It is always recommended to run this before you rerun step 5)
    docker rm midn_remote -f 
        
    ```
