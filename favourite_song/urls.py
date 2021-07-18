from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from favourite_song import views

urlpatterns = [
    path('favourite_song/<int:pk>', views.FavouriteSongDetail.as_view()),
    path('favourite_song/', views.FavouriteSongList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
