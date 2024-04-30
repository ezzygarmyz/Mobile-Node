#!/bin/bash

DOCKER_FILE="docker/build-apk"
IMAGE_NAME="build:android"
CONTAINER_NAME="build_android3"
APK_PATH="root/mobileznode/build/btczmobilenode/android/gradle/app/build/outputs/apk/debug/"
APK_FILENAME="app-debug.apk"
NEW_APK_FILENAME="MobileNode.apk"
HOST_PATH="$HOME"

sudo docker build -t $IMAGE_NAME -f $DOCKER_FILE .
sudo docker run -d --name $CONTAINER_NAME $IMAGE_NAME

sudo docker cp $CONTAINER_NAME:$APK_PATH$APK_FILENAME $HOST_PATH

sudo mv $HOST_PATH/$APK_FILENAME $HOST_PATH/$NEW_APK_FILENAME

sudo docker stop $CONTAINER_NAME
sudo docker rm $CONTAINER_NAME

echo "APK file has been extracted and renamed to MobileNode.apk"
echo "Destination: $HOST_PATH/$NEW_APK_FILENAME"