from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from song_comment import views

urlpatterns = [
    path('song_comment/', views.SongCommentList.as_view()),
    path('song_comment/<int:pk>/', views.SongCommentDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
