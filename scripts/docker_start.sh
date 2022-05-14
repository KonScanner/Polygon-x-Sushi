#!/bin/bash
NAME='polygon-x-sushi'
docker build --pull --rm -f "Dockerfile" -t $NAME:latest $PWD 
docker run --rm -d  -p 8501:8501/tcp --name $NAME $NAME:latest