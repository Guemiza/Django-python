FROM python:3.7-buster
RUN apt-get update 

RUN mkdir -p myapp
WORKDIR myapp
COPY . .
<<<<<<< HEAD
#RUN chmod +x ovpnconnect.sh ; bash ovpnconnect.sh

#ENV PATH="/scripts:${PATH}"
#COPY ./requirements.txt /requirements.txt
#RUN apt-get update  
#&& apt-get install no-cache --virtual .tmp gcc libc-dev linux-headers
=======
>>>>>>> de472e2b214b50697ad3c5b271edfadc3b764582
RUN pip3 install -r requirements.txt
RUN echo "hello world"  /myvolume1/message
VOLUME /myvolume1
EXPOSE 8000
CMD ["python3","manage.py","runserver","0.0.0.0:8000","--noreload"]
