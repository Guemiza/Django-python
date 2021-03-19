from django.http import HttpResponse
from django.shortcuts import render, redirect 
from .services import get_kubernts
from .services import get_droplets
from .services import get_redmine
from .services import get_users
from .services import get_usersGit
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import requests
import json
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    CreateView,
   
)

from .forms import OrderForm
from django.views.generic import TemplateView
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
#from .forms import OrderForm
from .filters import OrderFilter 
#from django.contrib.auth.backends.ModelBackend
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView
from .models import Post
from .models import Kubernets
from .models import Permissionproject
from .models import Quota
from django.forms import inlineformset_factory
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework import routers, serializers
from rest_framework.decorators import api_view
from .decorators import allowed_users, admin_only
from django.shortcuts import render, get_object_or_404
from django.forms import formset_factory,inlineformset_factory
from django.contrib.auth.models import User
from .forms import MemberFormSet,UserFormSet
from django.db import transaction
#affichage dans la page home les infos du redmine

def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/dashbord.html', context)

def about (request):
    context = {

        'kubers' : Kubernets.objects.all()
    }
    return render (request, 'blog/about.html', context)
#search
def search (request):
    posts = Post.objects.all()
    myFilter = OrderFilter(request.GET, queryset=posts)
    posts = myFilter.qs
    context = {
       'posts':posts, 'myFilter':myFilter
    }
    return render (request, 'blog/home.html', context)
# pour la classe k8s 
class GetKubernets(TemplateView):
    model = Kubernets
    authentication_classes = (TokenAuthentication,)
    permissions_classes = (IsAuthenticated,)
    template_name ='blog/about.html' # <app>/<model>_<viewtype>.html
    ordering =['-date_posted']
    
    def get_context_data(self, *args, **kwargs):
        context = {
            'kubers': Kubernets.objects.all(),
        }
        return context
class IDKuberListView(TemplateView):
    model = Kubernets
    template_name ='blog/about.html' # <app>/<model>_<viewtype>.html
    context_object_name ='kubers'

    def get_kubernts(self, *args, **kwargs):
        context = {
            'kubers': get_kubernts(),
        }
        return context
#détail du k8s
class KubernetsDetailView(DetailView):
    model = Kubernets
    template_name = 'blog/kuber_detail.html'


#création d'une formulaire k8s
class KubernetsCreateView(LoginRequiredMixin, CreateView):
   model = Kubernets
   fields = ['Name']
   success_url = '/namespace/'

   def form_valid(self, form):
        headers = {'Content-Type': 'application/json'}
        fields=form.cleaned_data['Name']
        data={"kind": "Namespace","metadata": {"name": fields}}
        data=JsonResponse(data) 
        response = requests.post('http://127.0.0.1:8001/api/v1/namespaces', headers=headers, data = data)
        print(response)
        #kubernets_id= response.json()['id']
        #print("this is for redmine ",response.json()['kind']['Namespace']['metadata']['name'])
        form.instance.create_by= self.request.user
        #form.instance.kubernets_id = kubernets_id
        return super().form_valid(form)
class QuotaDetailView(ListView):
    model=  Quota
    template_name = 'blog/detail_quota.html'
    
class QuotaCreateView(LoginRequiredMixin, CreateView):
    model = Quota
    success_url =  '/Quota_management'
    template_name='blog/ajout_quota.html'
    fields = ['namespace','choice_quota','quota','CPU','Limit_cpu','Memory','Limit_memory']
  
    def get_context_data(self, **kwargs):
        data = super(QuotaCreateView,self).get_context_data(**kwargs)
        if self.request.POST:
            data['members'] = MemberFormSet(self.request.POST)
           
        else:
            data['members'] = MemberFormSet()
           
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        members = context['members']
        headers = {'Content-Type': 'application/json'}
        fields=form.cleaned_data['quota']
        Name=form.cleaned_data['namespace']
      
        #project_leader=User.objects.filter(project_leader=self.get_object())
        #project_leader.select_related(project_leader)
        
        CPU=form.cleaned_data['CPU']
        Memory=form.cleaned_data['Memory']
        Limit_cpu=form.cleaned_data['Limit_cpu']
        Limit_memory=form.cleaned_data['Limit_memory']
        data= {"apiVersion": "v1","kind": "ResourceQuota","metadata":{"name": fields },"spec":{ "hard":{ "requests.cpu": CPU,"requests.memory": Memory,"limits.cpu": Limit_cpu,"limits.memory": Limit_memory} }} 
        data=JsonResponse(data) 
        response = requests.post('http://127.0.0.1:8001/api/v1/namespaces/devteam/resourcequotas', headers=headers, data = data)
        #print(response)
        with transaction.atomic():
            self.object = form.save()
            if members.is_valid():
                members.instance = self.object
                members.save()
        return super(QuotaCreateView, self).form_valid(form)

def deleteQuota(request, pk):
	quota =  Quota.objects.get(id=pk)
	if request.method == "POST":
		quota.delete()
		return redirect('/Quota_management')

	context = {'item':quota}
	return render(request, 'blog/delete_quota.html', context)
  #update k8s
class KubernetsUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model =  Kubernets 
    fields = ['Name']
    success_url = '/namespace/'
    template_name='blog/update_management.html'
    def form_valid(self, form):
        headers = {'Content-Type':'application/json-patch+json'}
        print(headers)
        fields=form.cleaned_data['Name']
        print(self.get_object())
        project = Kubernets.objects.filter(Name =self.get_object())
        Name=project[0].Name
        data={"kind": "Namespace","metadata": {"name": fields}}
        data=JsonResponse(data) 
        print(data)
        response = requests.patch('http://127.0.0.1:8001/api/v1/namespaces/'+Name+'',headers=headers)
        #print(response)
        #response.json()
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        kuber = self.get_object()
        if self.request.user == kuber.create_by:
            return True
        return False

 #supprimer namesapce en k8s  
class KubernetsDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Kubernets
    success_url = '/namespace/'
    template_name='blog/kubernets_confirm_delete.html'

    def test_func(self):
        headers = {'Content-type':'application/json'}
        print("jomm")
        print(self.get_object())
        project = Kubernets.objects.filter(Name =self.get_object())
        Name=project[0].Name
        print("jomm")
        response = requests.delete('http://127.0.0.1:8001/api/v1/namespaces/'+Name+'')
        print(response)
        kuber = self.get_object()
        if self.request.user == kuber.create_by:
            return True
        return False
 
        
#détail git & redmine

class GetDroplets(TemplateView):
    template_name = 'blog/home.html'
    model = Post
    def get_context_data(self, *args, **kwargs):
        context = {
            #'droplets' : get_droplets(),
            #'redmines' : get_redmine(),
            'posts':  Post.objects.all(),
        }
      
        #for i in range(len(context)):
        #    print(context[i])
        return context

# detail to project git & redmine
class PostDetailView(DetailView):
    model= Post
    template_name = 'blog/post_detail.html'



#la création d'api git
class PostCreateView(LoginRequiredMixin, CreateView,forms.ModelForm):
    model = Post
    fields = ['Project_name','Identifiat','project_description','visibility_Level','status']
    success_url = '/project/'
    def form_valid(self, form):
        headers = {'Content-type': 'application/json', 'PRIVATE-TOKEN': 't4eHMHShhBv6FLEXksqV','Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
        fields=form.cleaned_data['Project_name']
        #gitlab_id=form.cleaned_data['gitlab_id']
        fiel=form.cleaned_data['project_description']
        #gitlab_id=form.cleaned_data['gitlab_id']
        iden=form.cleaned_data['Identifiat']
        LEVEL =form.cleaned_data['visibility_Level'][0].lower()
        #name=form.cleaned_data['author']
        #date=form.cleaned_data['date_posted']
        url="http://172.16.0.112:3000/projects.json"
        data={"name": fields, "description":fiel,"visibility":LEVEL}
        datar= '{"project" :{"name" :"'+fields+'","identifier" : "'+iden+'" ,"description":"'+fiel+'","is_public":"'+LEVEL+'"}}'
        data=JsonResponse(data)
        res= requests.post('http://172.16.0.111/api/v4/projects/',headers=headers,data=data)
        res.json()
      

        response = requests.post(url, headers=headers, data=datar)
        response.json()
        redmine_id = response.json()['project']['id']
        print("this is for redmine ",response.json()['project']['id'])
    
        gitlab_id = res.json()['id']
        print("this is for gitlab  ",res.json()["id"])
            #else:
    #return Response(status=status.HTTP_400_BAD_REQUEST)   
        form.instance.author = self.request.user
        form.instance.gitlab_id = gitlab_id
        form.instance.redmine_id = redmine_id
        return super().form_valid(form)
#class permission User

class ProjectManagemntCreateView(LoginRequiredMixin,CreateView ):
    model =  Permissionproject
    success_url = '/detail_management/'
    fields = ['project_id','user','Choose_a_role_permission','expires_at']

    def get_context_data(self, **kwargs):
        data = super(ProjectManagemntCreateView ,self).get_context_data(**kwargs)
        data_user = super(ProjectManagemntCreateView, self).get_context_data(**kwargs)
      
        if self.request.POST:
            data['members'] = MemberFormSet(self.request.POST)
            data_user['users'] = UserFormSet(self.request.POST)
        else:
            data['members'] = MemberFormSet()
            data_user['users'] = UserFormSet()
        return data
	
    def form_valid(self, form):
        context = self.get_context_data()
        members = context['members']
        headers = {'Content-type': 'application/json', 'PRIVATE-TOKEN': 't4eHMHShhBv6FLEXksqV','Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
        role=form.cleaned_data['Choose_a_role_permission']
        user=form.cleaned_data['user']
        print("my user id" , user)
        expires=form.cleaned_data['expires_at']
        form.is_valid()
        project_id=form.cleaned_data['project_id']
        print('projectID NEW' , project_id)
        data={"user_id": user,"access_level":role,"expires_at":expires}
        print(data)
        #datar= '{"project" :{"name" :"'+fields+'","identifier" : "'+iden+'" ,"description":"'+fiel+'"}}'
        #data=JsonResponse({'data': data})
        # add member from gitlab
        #curl --request POST --header "PRIVATE-TOKEN: t4eHMHShhBv6FLEXksqV" --data "user_id=4&access_level=30" "http://172.16.0.111/api/v4/projects/240/members"
        response =requests.post('http://172.16.0.111/api/v4/projects/+project_id+/members', headers=headers, data=data)
        print('myacces print',response)
        #response = requests.post('http://127.0.0.1:8001/api/v1/namespaces/'+Name+'/resourcequotas', headers=headers, data = data)

        # add a memeber for redmine
        #resp= requests.post(url, headers=headers, data=datar)
        #print(resp)
        with transaction.atomic():
            self.object = form.save()
            if members.is_valid():
                members.instance = self.object
                members.save()
        return super(ProjectManagemntCreateView, self).form_valid(form)



#details de Permission project
class UserDetailView(ListView):
    model=  Permissionproject
    template_name = 'blog/invite_detail.html'
    
  #update permission management:
class ManagementUpdateView(UpdateView):
    model =  Permissionproject
    success_url = '/detail_management'
    fields = ['project_id','user','Choose_a_role_permission','expires_at']
    template_name='blog/update_management.html'
    def get_context_data(self, **kwargs):
        data = super(ManagementUpdateView ,self).get_context_data(**kwargs)
        data_user = super(ManagementUpdateView, self).get_context_data(**kwargs)
      
        if self.request.POST:
            data['members'] = MemberFormSet(self.request.POST)
            data_user['users'] = UserFormSet(self.request.POST)
        else:
            data['members'] = MemberFormSet()
            data_user['users'] = UserFormSet()
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        members = context['members']
        headers = {'Content-type': 'application/json', 'PRIVATE-TOKEN': 't4eHMHShhBv6FLEXksqV','Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
        role=form.cleaned_data['Choose_a_role_permission']
        user=form.cleaned_data['user']
        expires=form.cleaned_data['expires_at']
        projetc_id=form.cleaned_data['project_id']
        data={"user_id": user,"access_level":role}
        print(data)
        #data= '{"project" :{"name" :"'+fields+'","identifier" : "'+iden+'" ,"description":"'+fiel+'","is_public":"'+LEVEL+'"}}'
        #print('projec2 : {0}'.format(fields))
        #url="http://172.16.0.112:3000/projects/"+redmine_id+".json"
        #data=JsonResponse(data)
        #response = requests.put('http://172.16.0.111/api/v4/projects/'+gitlab_id+'?name='+fields+'',headers=headers)
        #responseredmine = requests.put(url, headers=headers , data=data)
        #response.json()
        #responseredmine.json()
        #print(response)
        #return Response("errors" ,status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            self.object = form.save()
            if members.is_valid():
                members.instance = self.object
                members.save()
        return super(ManagementUpdateView, self).form_valid(form)

#delete management

def deleteManagement(request, pk):
	management = Permissionproject.objects.get(id=pk)
	if request.method == "POST":
		management.delete()
		return redirect('/detail_management')

	context = {'item':management}
	return render(request, 'blog/delete_management.html', context)

       # update project in gitlab and redmine
class PostUpdateView(LoginRequiredMixin,  UpdateView):
    model = Post
    fields = ['gitlab_id','redmine_id','Project_name','Identifiat','project_description','visibility_Level','status']
    success_url = '/project/'
    template_name='blog/project_update.html'
    def form_valid(self, form):
        
        #print("post",Post.gitlab_id)      
        headers = {'Content-type': 'application/json', 'PRIVATE-TOKEN': 't4eHMHShhBv6FLEXksqV','Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
        fields=form.cleaned_data['Project_name']
        gitlab_id=form.cleaned_data['gitlab_id']
        fiel=form.cleaned_data['project_description']
        iden=form.cleaned_data['Identifiat']
        LEVEL =form.cleaned_data['visibility_Level'][0].lower()
        redmine_id=form.cleaned_data['redmine_id']
        data_git={"name": fields, "description":fiel,"visibility":LEVEL}
        data= '{"project" :{"name" :"'+fields+'","identifier" : "'+iden+'" ,"description":"'+fiel+'","is_public":"'+LEVEL+'"}}'
        #print('projec2 : {0}'.format(fields))
        url="http://172.16.0.112:3000/projects/"+redmine_id+".json"
        #data=JsonResponse(data)
        response = requests.put('http://172.16.0.111/api/v4/projects/'+gitlab_id+'?name='+fields+'',headers=headers)
        responseredmine = requests.put(url, headers=headers , data=data)
        #response.json()
        #responseredmine.json()
        print(response)
        form.instance.author = self.request.user
        return super().form_valid(form)
        #return Response("errors" ,status=status.HTTP_400_BAD_REQUEST)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
     


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
   
    model = Post
    success_url = '/project/'
 
    def test_func(self):
      
        print(self.get_object())
        project = Post.objects.filter(Project_name=self.get_object())
        gitlab_id = project[0].gitlab_id
        redmine_id= project[0].redmine_id

        headers = {'Content-type':'application/json',
                    'PRIVATE-TOKEN': 't4eHMHShhBv6FLEXksqV',
                    'Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
        print("jomm")
        url="http://172.16.0.112:3000/projects/"+redmine_id+".json"
        #post = self.get_context_data
        #if self.request.user == post.author:
        response = requests.delete('http://172.16.0.111/api/v4/projects/'+gitlab_id+'',headers=headers)
        responseredmine = requests.delete(url, headers=headers)
        print("supprimer de redmine",responseredmine)
        print("deleteof gitlab",response)
        print("hello word")
      
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



       

    