
* Prerequest:
   
   Please refer to  https://docs.docker.com/get-docker/ to install docker service on your testing machine.


* Pull the latest docker images:

    The docker images have been commited to dockerhub
    
    run the below commands to get the latest program update:
    ```
    #On Central Machine:
    sudo docker pull luyaochen/midn_central:latest
    
    #On Remote Machine
    sudo docker pull luyaochen/midn_remote:latest
    ```

* Plan the networking

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
   
   
* run central site 
     ```
     # create and start a docker container to run the central site applications
     sudo docker run  -it -d -p 443:443 -p 6600-6700:6600-6700 --name=midn_central luyaochen/midn_central
     ```    
    
    The central site MIDN Controller can be accessed by:
    
    https://192.168.0.23/midn_central/
    
    (The SSL certification is local signed for testing, please ignore the error when enter this URL )

     <picture>
     <img alt="Screen capre of central machine inital login in." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Central_Ini.JPG">
 
     </picture>
     
* Run remote server
   ```  
    sudo docker run  -it -d -p 80:80 -p 6000:6000 --name=midn_remote_1 luyaochen/midn_remote
   ```    
   
  The remote site MIDN Controller can be accessed by:
    
    http://192.168.1.15   
    
  There is a onetime setup on remote site:
     <picture>
     <img alt="Screen capre of onetime remote site setup." src="https://github.com/Luyaochen1/midn_gui/blob/main/screen_capture/Remote_Config.JPG">
 
     </picture>
  
   The below information is reuiqred:
   Remote Site name  - To idenfiry the site name
   Central Site Web Applicaiton URL: The public IP address and port of the central mahine
   Remote site public IP address: The program will try to idenfify the public IP address. But, if it is not accurate, manual update is reuqired.
    
 * Add a task on central site machine
    
    
      
 * 
 
 
 
 * Acknowledge a task on remote site machine
 
 
   
    ``` 
    http://remote_ip:remote_port
     ```    
      where temote_ip is the host running the docker ( not the IP of remote container)
    
    change and save the defaul setup on remote server
    
    - update the site name
    
    - update the central server app url:
    
      eg, if you get "Central Host IP address: 172.17.0.26" on central server, setup http://172.17.0.26  on all remote sites
      

