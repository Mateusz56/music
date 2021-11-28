from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user import ObtainAuthTokenView, views

urlpatterns = [
    path('api-token-auth/', ObtainAuthTokenView.ObtainAuthToken.as_view()),
    path('user_info/', views.UserInfo.as_view()),
    path('user_detail/', views.UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
