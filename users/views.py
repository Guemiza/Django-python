from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
import requests
import json
from django import forms
from .models import Profile
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.generic.list import ListView
import requests
import http.client
import mimetypes
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from .service import get_users
from .service import get_usersGit
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    DeleteView,
    UpdateView,)
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_list_or_404


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)


def register(request):  
    form = UserRegisterForm(request.POST)
    #profile= create_profile(request.POST,instance = Profile)
    if request.method == 'POST':
        #User_form = UserUpdateForm(request.POST, instance=request.user)
        #profile = Profile.objects.get(user = request.user)
        #Profile_form = ProfileUpdateForm(request.POST, instance = profile)
        if form.is_valid() : #and Profile_form. is_valid():
            form.save()

            #User_form.save()
            #profile.save()
            headers = {
        'Content-type': 'application/json',
        'PRIVATE-TOKEN': '3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Bearer 3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
            url='http://172.16.0.112:3000/users.json'
            
            name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username = form.cleaned_data['username']
            password1 =form.cleaned_data['password1']

            
            data={"name":name,"username":username,"email":email,"password":password1} 
            datar= '{"user": {"login":"'+name+'","firstname":"'+name+'","lastname":"'+last_name+'","mail":"'+email+'","password":"'+password1+'"}}'
            data=JsonResponse(data)
            #add user in gitlab
            response = requests.post('http://172.16.0.111/api/v4/users/', headers=headers, data=data) 
            user_git_id = response.json()['id']
            print(response)
             # save id user in gitalb
            print("this is id for gitlab  ",response.json()['id'])

            # add user in redmine
            res = requests.post(url, headers=headers, data=datar)  
            print(res)
            user_redmine= res.json()['user']['id']
            print("this is id for redmine ",res.json()['user']['id'])  
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('list')
            form.instance.user_git_id = user_git_id 
            print(user_git_id) 
            form.instance.user_redmine = user_redmine
            print(user_redmine)
            return super().form_valid(form)
          
    else:
        form = UserRegisterForm()
        #User_form = UserUpdateForm(instance=request.user)
        #profile = Profile.objects.get(user = request.user)
        #Profile_form = ProfileUpdateForm(request.POST, instance = profile)
    return render(request, 'users/register.html', {'form': form})

class GetUser(TemplateView):
    template_name = 'users/list.html'
    Model = User
    def get_context_data(self, *args, **kwargs):
        context = {
            'object_list' : get_users(),
            'git_user'    :  get_usersGit(),
            'git_user' : User.objects.all(),
        }
        
        return context

# detail user to git & redmine
class UserDetailView(DetailView):
    model= User
    template_name = 'users/user_details.html'

def delete_user(request,pk):

	if request.method == "POST":
            headers = {
        'Content-type': 'application/json',
        'PRIVATE-TOKEN': '3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Bearer 3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
            print(headers)
           
            #print(self.get_object())
            #tabuser=User.objects.filter(userame=self.get_object())
            #user_git_id= tabuser[0].user_git_id
            #user_git_id=User.objects.filter(user_git_id)
            user= User.objects.get(id=pk)
            user_git_id= get_list_or_404(User, published=True)

            delete_gitlab= requests.delete('http://172.16.0.111/api/v4/users/'+user_git_id+'',headers=headers)
            print(delete_gitlab)
            delete_redmine = requests.delete('http://172.16.0.112:3000/users/user_id.json', headers=headers)
            print(delete_gitlab)
            #response.json()
            user.delete()
            print("heeloooo")
            return redirect('/list')


   
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES ,instance=request.user.profile)
      
        if u_form.is_valid() and p_form.is_valid():
            user_from =u_form.save()
            profile_form= p_form.save(False)
            user_from=profile_form
            profile_form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('list')


    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)                             #instance=request.user.profile)
    args = {}
       
    args['u_form'] = u_form
    args['p_form'] = p_form
    return render(request, 'users/profile.html',args)


class UserUpdate(LoginRequiredMixin, UpdateView):
    model=User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    success_url='/list'
    
    def form_valid(self, form):
      
        headers = {
        'Content-type': 'application/json',
        'PRIVATE-TOKEN': '3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Bearer 3YhXE1DsLE-xXs15ECg7',
        'Authorization': 'Basic YWRtaW46YXplcnR5cmVkbWluZQ=='}
        user = form.save(commit=True)
        name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        email=form.cleaned_data['email']
        username = form.cleaned_data['username']
        #user_git_id=form.cleaned_data['user_git_id']
        #user_redmine=form.cleaned_data['user_redmine']
        data_git={"name":name,"username":username,"email":email} 

        #print("user",User.user_git_id) 
        print(self.get_object())
        project = User.objects.filter(username=self.get_object())
        user_git_id= project[0].first_name
        user_redmine= project[0].first_name
       
        data= '{"user": {"login":"'+name+'","firstname":"'+name+'","lastname":"'+last_name+'","mail":"'+email+'"}}'
        
        url="http://172.16.0.112:3000/users/"+email+".json"
        #data=JsonResponse(data)

        #update user in gitlab with api
        response = requests.put('http://172.16.0.111/api/v4/users/'+email+'', headers=headers,data=data_git)
        print(response)
        #response.json()


        #update user in redmine with api
        res = requests.put(url, headers=headers, data=data)
        print(res)
        #user.set_password(password)
        user.save()
        return HttpResponseRedirect(self.get_success_url())

def email(request):
    subject = "You're receiving this email because you requested a password reset for your user account at localhost."
    message ="Please go to the following page and choose a new password:"
    email_form= settings.EMAIL_HOST_USER
    recipent_list=['gmiza.amel@gmail.com']
    send_mail(subject,message,email_form,recipent_list)
    return HttpResponse("email sent")


