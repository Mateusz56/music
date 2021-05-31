from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from song_mark import views

urlpatterns = [
    path('song_mark/', views.SongMarkView.as_view()),
    path('song_mark_author/', views.SongMarkDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
