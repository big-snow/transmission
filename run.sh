#! /bin/bash

IMG_NAME="image name"
CONT_NAME="container name"
PORT="port number"
HOST_VOL="host volume path"
DOCK_VOL="docker volume path"


if [ ! "$(docker ps -q -f name=$CONT_NAME)" ]; then
	if [ "$(docker ps -aq -f status=exited -f name=$CONT_NAME)" ]; then
		docker rm $CONT_NAME
	fi
	docker run -d -t --name $CONT_NAME -p $PORT:$PORT -v $HOST_VOL:$DOCK_VOL $IMG_NAME
fi
