from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from song import views

urlpatterns = [
    path('song/', views.SongList.as_view()),
    path('song/<int:pk>/', views.SongDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
