from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from favourite_album import views

urlpatterns = [
    path('favourite_album/<int:pk>', views.FavouriteAlbumDetail.as_view()),
    path('favourite_album/', views.FavouriteAlbumList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
