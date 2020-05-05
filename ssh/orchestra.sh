#!/bin/bash

sudo docker network create testnet

clear
echo "##################################"
echo "          CONFIGURING SERVER"
echo "##################################"
sleep 1.5
sudo docker build -f Dockerfile.server -t server_build .
sudo docker run --net testnet -d -P --name test_server server_build

HOST_PORT=$(sudo docker port test_server 22 | awk -F ':' '{print $2}')
KEY_PATH='/home/drednaut/Programming/ncr-portal/ssh/test'

clear
echo "##################################"
echo "          CONFIGURING CLIENT"
echo "##################################"
sleep 1.5
sudo docker build -f Dockerfile.client -t client_build . \
--build-arg DPORT=$HOST_PORT
sudo docker run --net testnet -d -P --name test_client client_build 


#clear
#echo "##################################"
#echo "       CONNECTING TO SERVER"
#echo "##################################"
#sleep 1.5
#ssh -i $KEY_PATH root@$HOST_IP -p $HOST_PORT


#clear
#echo "##################################"
#echo "       CLEANING UP CONTAINERS"
#echo "##################################"
#sleep 1.5
#sudo docker stop $(sudo docker ps -aq)
#sudo docker rm $(sudo docker ps -aq)
