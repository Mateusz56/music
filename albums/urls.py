from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from albums import views

urlpatterns = [
    path('album/', views.AlbumList.as_view()),
    path('album/<int:pk>/', views.AlbumDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
