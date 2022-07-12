1. the docker images have been commited to dockerhub
    
   
2. run server

    sudo docker run  -it -d -p ssss:80 --name=midn_server luyaochen/midn_server
      where ssss is the server GUI port exposed to external network

3. run remote 
  
    sudo docker run  -it -d -p remote_port_1:80 --name=midn_remote_1 luyaochen/midn_remote
      where remote_port_1 is the remote server 1 GUI port exposed to external network
    
    sudo docker run  -it -d -p remote_port_2:80 --name=midn_remote_1 luyaochen/midn_remote 
      where remote_port_2 is the remote server 2 GUI port exposed to external network
