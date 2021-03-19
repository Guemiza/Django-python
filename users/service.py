import os
import requests

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