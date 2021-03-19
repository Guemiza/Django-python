from django.urls import path, include
from .views import (
   
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView, 
    KubernetsCreateView,
    KubernetsDetailView,
    KubernetsDeleteView
)
from .views import KubernetsUpdateView
from .views import GetDroplets
from .views import GetKubernets
from .views import ProjectManagemntCreateView
from .views import  QuotaCreateView
from .views import ManagementUpdateView
from .views import UserDetailView
from .views import QuotaDetailView
from . import views
urlpatterns = [
    #la page index
    path('dashbord/',views.index, name="blog-index"),



    # url de table de redmine & gitlab
    path('project/', GetDroplets.as_view(template_name='blog/home.html'), name='blog-home'),

    # url du page details project git & redmine
    path('project_detail/<int:pk>/', PostDetailView.as_view(template_name = 'blog/post_detail.html'), name='post-detail'),
   
    #url for create a project in gitlab and redmine
    path('project/new/', PostCreateView.as_view(), name='post-create'),
   
    # url to update project
    path('project/<str:pk>/update/', PostUpdateView.as_view(template_name='blog/project_update.html'), name='post-update'),
    
    # url to delete project
    path('project/<int:pk>/delete/', PostDeleteView.as_view(template_name='blog/post_confirm_delete.html'), name='post-delete'),
    
    
    
    #url for invite member in git and redmine
    path('project_members/',ProjectManagemntCreateView.as_view(template_name='blog/invite_user.html'), name='blog-invite_user'),
  
  #details for invite member
    path('detail_management/', UserDetailView.as_view(template_name = 'blog/invite_detail.html'), name='detail'),

    # update project members
    path('detail_management/<str:pk>/update/', ManagementUpdateView.as_view(), name='permission-update'),
      # url to delete project members
    path('detail_managemen/<int:pk>/delete/',views.deleteManagement, name='permission-delete'),
    
    
    # url update a namespace in kubernets 
    path('kuber/<int:pk>/update/', KubernetsUpdateView.as_view(template_name='blog/update_management.html'), name='kuber-update'),
    #url delete a project in kuber 
    path('kuber/<int:pk>/delete/', KubernetsDeleteView.as_view(template_name='blog/kubernets_confirm_delete.html'), name='kuber-delete'),
    # url for details kuber
    path('kuber/<int:pk>', KubernetsDetailView.as_view(), name='kuber-detail'),
    # url add a namespace
    path('kuber/new/',  KubernetsCreateView.as_view(), name='kuber-create'),
    # url for table details du k8s
    path('namespace/', GetKubernets.as_view(), name='blog-about'),
    # url to add a quota 
    path('namespace/add_quota/', QuotaCreateView.as_view(template_name="blog/ajout_quota.html"), name='blog-ajout_quota'),
    # details quota 
    path('Quota_management/', QuotaDetailView.as_view(), name='detail-quota'),
    path('Quota_management/<int:pk>/delete/',views.deleteQuota, name='quota-delete'),

   

]

