FROM python:3.7-buster
RUN apt-get update && \
    apt-get install openvpn -y

RUN mkdir -p myapp
WORKDIR myapp
COPY . .
RUN chmod +x ovpnconnect.sh ; bash ovpnconnect.sh

#ENV PATH="/scripts:${PATH}"
#COPY ./requirements.txt /requirements.txt
#RUN apt-get update  
#&& apt-get install no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip3 install -r requirements.txt
#RUN apt-get del .tmp

#RUN mkdir /app
#COPY ./dprojx /app
#WORKDIR /app
#COPY ./dprojx/blog/static/js /scripts

#RUN chmod +x /scripts/*

#RUN mkdir -p /vol/web/media
#RUN mkdir -p /vol/web/static
#RUN adduser  user
#RUN chown -R user:user /vol
#RUN chmod -R 755 /vol/web
#USER user
#RUN python3 manage.py runserver --noreload
#ENTRYPOINT ["entrypoint.sh"]
EXPOSE 8000
CMD ["python3","manage.py","runserver","0.0.0.0:8000","--noreload"]
