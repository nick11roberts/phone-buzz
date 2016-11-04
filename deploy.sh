#!/bin/bash

source ~/phone-buzz/docker.env
dvm use
docker rm -fv phone-buzz
docker build -t phone-buzz:latest .
docker run --name phone-buzz --detach -p 80:5000 phone-buzz
