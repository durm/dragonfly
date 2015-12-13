from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    password_recovery_code = models.CharField(max_length=100, null=True)
    
    @staticmethod
    def get_account(user):
        return Account.objects.get_or_create(user=user)[0]
