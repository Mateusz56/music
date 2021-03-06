from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from album_invitation import views

urlpatterns = [
    path('album_invitation/', views.FavouriteAlbumList.as_view()),
    path('album_invitation_user/<int:userId>/', views.AlbumInvitationUser.as_view()),
    path('album_invitation_user/', views.AlbumInvitationUser.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
