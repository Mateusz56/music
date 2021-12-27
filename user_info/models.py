from django.db import models
from django.contrib.auth import get_user_model


class UserInfo(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    skin_mode = models.CharField(max_length=20)
