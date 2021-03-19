import os
import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#afficher tous les projets du k8s
def get_kubernts():
    url = 'http://127.0.0.1:8001/api/v1/namespaces/'
    r = requests.get(url)
    droplets = r.json()
    droplet_list = []
    for i in range(len(droplets['items'])):        
        droplet_list.append(droplets['items'][i])
        #print("ok")
        #print(droplets['items'][i])
    return droplet_list


#afficher tous les projets du git et redmine

def get_droplets():
    
    headers = {'Content-type': 'application/json',
    'PRIVATE-TOKEN': 't4eHMHShhBv6FLEXksqV',
    }
  
    url='http://172.16.0.111/api/v4/projects/'
    r = requests.get(url, headers=headers)
    droplets = r.json()
    #print(droplets[1])
    
    droplet_list = []
    
#mettre les données du project git en tab
    for i in range(len(droplets)) : 
        droplet_list.append(droplets[i]) 

    return droplet_list 
def get_redmine():
    
    headers = {'Content-type': 'application/json',
    'Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}

    url_redmine='http://172.16.0.112:3000/projects.json/'
    res = requests.get(url_redmine, headers = headers)
    droplets = res.json()
    #print(droplets[1])
    droplet_list = []
    for i in droplets['projects']:
        droplet_list.append(i)
    return droplet_list 

def get_delete( ):

    headers = {'Content-type': 'application/json', 'PRIVATE-TOKEN': 't4eHMHShhBv6FLEXksqV'}
    data={"name":"", "description":""}
    data=JsonResponse(data)
    response = requests.delete("http://172.16.0.111/api/v4/projects/:id", headers=headers,data=data)
    return Response(status=status.HTTP_202_ACCEPTED)


def get_users():

    url_redmine = "http://172.16.0.112:3000/users.json"
    url_git = "http://172.16.0.111/api/v4/users/"
       
    headers = {
        'Content-type': 'application/json',
        'PRIVATE-TOKEN': '3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Bearer 3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
    

    response = requests.get(url_redmine, headers=headers)
    #response = requests.get(url_git, headers=headers)
    
    droplets = response.json()
    #print(droplets)
    droplet_list = []

    for i in droplets['users']:
        droplet_list.append(i)
       
    return droplet_list

def  get_usersGit():

    
    url_git = "http://172.16.0.111/api/v4/users/"
       
    headers = {
        'Content-type': 'application/json',
        'PRIVATE-TOKEN': '3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Bearer 3YhXE1DsLE-xXs15ECg7',
        }
    

    
    response = requests.get(url_git, headers=headers)
    
    droplets = response.json()
    #print(droplets)
    droplet_list = []

    for i in range(len(droplets)):
        droplet_list.append(droplets[i])
    return droplet_list