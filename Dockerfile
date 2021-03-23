FROM python:3.7-buster
RUN apt-get update 

RUN mkdir -p myapp
WORKDIR myapp
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python3","manage.py","runserver","0.0.0.0:8000","--noreload"]
