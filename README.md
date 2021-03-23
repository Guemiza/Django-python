# https-github.com-Guemiza-Django-python.git-
it’s a Django-python project that allows the getion of projects in gitlab,kubernets and redmine to cross-api

the commands necessary to download and start the project in your local:

1- Downloading the project
git clone /https-github.com-Guemiza-Django-python.git-

2- you do not ask the pienne to install the django libraries just need your docker contents
and you run the order
docker build -t python:latest .
docker images : to see that the image is well builder

and to run this image in docker container 

docker run -d -8000:8000 python:latest 

docker ps :to see that the container is properly started

and in your navigator you type 127.0.0.1:8000
