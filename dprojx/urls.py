"""dprojx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static 
from users import views as user_views
from users import views as delete_user 



urlpatterns = [
    path('admin/', admin.site.urls),
    # afficher le tab d'user
    path('list/', user_views.GetUser.as_view(template_name='users/list.html'), name='list'),
   
   #page to register user in git and redmine 
    path('', user_views.register, name='register'),

    #update_user
    path('users/<int:pk>/update/', user_views.UserUpdate.as_view(), name='user-update'),

    #page details
    path('user_detail/<int:pk>/', user_views.UserDetailView.as_view(template_name = 'users/user_details.html'), name='user-detail'),


    #delete user
    path('user/<int:pk>/delete/', user_views.delete_user, name='delete'),

    # user profile
    path('profile/', user_views.profile, name='profile'),

    #page login
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

   #page logout
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # test email 
    path('send-mail/', user_views.email, name='send-mail'),

    
    path('', include('blog.urls')),
    #path('login/',login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    #path('', include('blog.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
