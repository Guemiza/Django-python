from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField
import datetime
class Post(models.Model):
   
    id = models.AutoField(primary_key=True)
    Project_name = models.CharField(max_length=100)
    gitlab_id = models.CharField(max_length=100)
    redmine_id = models.CharField(max_length=100)
    Identifiat  = models.CharField(max_length=100)
    #user_id = models.ForeignKey(User, on_delete= models.CASCADE)
    gitlab_member = models.CharField(max_length=100)
    project_description = models.TextField()
    Project_URL = models.CharField(max_length=100)
    name_customer = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=123)
    LEVEL = (
        ('Public',  'Public'),
        ('Private', 'Private'),
        ('Internel', 'Internel'),
     
    )
    visibility_Level = MultiSelectField(choices=LEVEL)
    STATUS = (
                ('Pending', 'Pending'),
                ('Out for delivery', 'Out for delivery'),
                ('Delivered', 'Delivered'),
                )  

    status = models.CharField(max_length=200, null=True, choices=STATUS)
 

    def __str__(self):
        return self.Project_name



    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    

class Permissionproject(models.Model):
    USER = (
                ('50', 'Manager'),
                ('20', 'Reporter'),
                ('30', 'Developer'),
                ('0', 'No access'),
			) 
    user =models.ForeignKey(User, on_delete=models.PROTECT,verbose_name=u"User member")
    project_id =models.ForeignKey(Post, on_delete=models.PROTECT,verbose_name=u"Projects")
    Choose_a_role_permission = models.CharField(max_length=200, null=True, choices=USER)
    expires_at = models.DateTimeField(default=datetime.date.today)

    STATUS = (
                ('Pending', 'Pending'),
                ('Out for delivery', 'Out for delivery'),
                ('Delivered', 'Delivered'),
                )  

    status = models.CharField(max_length=200, null=True, choices=STATUS)

class Kubernets(models.Model):
    create_by = models.ForeignKey(User, null=True, related_name="author",on_delete=models.SET_NULL)
    project_description = models.TextField()
    Name = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now,null=True, blank=True)
    STATUS = (
                ('Pending', 'Pending'),
                ('Active', 'Active'),
                ('Deactivate', 'Deactivate'),
                )  

    status = models.CharField(max_length=200, null=True, choices=STATUS)
    def __str__(self):
     return self.Name

class Quota(models.Model):
    quota = models.CharField(max_length=100,blank=True)
    CPU = models.CharField(max_length=100,blank=True)
    Memory = models.CharField(max_length=100,blank=True)
    Limit_cpu = models.CharField(max_length=100,blank=True)
    Limit_memory = models.CharField(max_length=100,blank=True)
    QUOTA = (
                ('Business', 'Business'),
                ('Mobile', 'Mobile'),
                ('Ess', 'Ess'),
                
                )  

    choice_quota = models.CharField(max_length=200, choices=QUOTA,blank=True)
    namespace = models.ForeignKey(Kubernets, on_delete=models.PROTECT ,verbose_name=u"Namespaces", blank=True)



       
       

class Order(models.Model):

    STATUS = (
                ('Pending', 'Pending'),
                ('Out for delivery', 'Out for delivery'),
                ('Delivered', 'Delivered'),
                )

USER = (
                ('Owner', 'Owner'),
                ('Guest', 'Guest'),
                ('Reporter', 'Reporter'),
                ('Developer', 'Developer'),
                ('Maintainer', 'Maintainer'),
                ('NO access', 'No access'),
			) 
post = models.ForeignKey(Post, null=True, on_delete= models.SET_NULL)
kubernets = models.ForeignKey(Kubernets, null=True, on_delete= models.SET_NULL)
date_created = models.DateTimeField(auto_now_add=True, null=True)
#status = models.CharField(max_length=200, null=True, choices=STATUS)
user = models.CharField(max_length=200, null=True, choices=USER)
note = models.CharField(max_length=1000, null=True)

def __str__(self):
		return self.Post.title

def get_absolute_url(self):
        return reverse('kuber-create', kwargs={'pk': self.pk})


