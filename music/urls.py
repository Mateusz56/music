"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.authtoken import views
from user.views import UserPost, UserDetail
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('song.urls')),
    path('', include('album_comment.urls')),
    path('', include('albums.urls')),
    path('', include('song_comment.urls')),
    path('', include('song_mark.urls')),
    path('', include('album_mark.urls')),
    path('', include('favourite_song.urls')),
    path('', include('favourite_album.urls')),
    path('', include('album_invitation.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('user/', UserPost.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
]
