from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user_info import views

urlpatterns = [
    path('user_skin_mode/', views.UserInfoView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
