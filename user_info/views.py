from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from user_info.models import UserInfo
import json
from rest_framework.authentication import TokenAuthentication


class UserInfoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            user_info = UserInfo.objects.get(user=request.user)
            return Response(model_to_dict(user_info), status=status.HTTP_200_OK)
        except UserInfo.DoesNotExist:
            return Response(data={}, status=status.HTTP_200_OK)

    def put(self, request):
        body = json.loads(request.body)
        try:
            user_info = UserInfo.objects.get(user=request.user)
        except UserInfo.DoesNotExist:
            user_info = None

        if not user_info:
            user_info = UserInfo(user=request.user, skin_mode=body['skin_mode'])
            user_info.save()
            return Response(model_to_dict(user_info), status=status.HTTP_201_CREATED)
        else:
            user_info.skin_mode = body['skin_mode']
            user_info.save()
            return Response(model_to_dict(user_info), status=status.HTTP_200_OK)
