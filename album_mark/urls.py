from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from album_mark import views

urlpatterns = [
    path('album_mark/', views.AlbumMarkView.as_view()),
    path('album_mark_author/', views.AlbumMarkDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
