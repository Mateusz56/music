from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from album_comment import views

urlpatterns = [
    path('album_comment/', views.AlbumCommentList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
