#!/bin/bash

clear
echo "##################################"
echo "       CLEANING UP CONTAINERS"
echo "##################################"
sleep 1.5
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
