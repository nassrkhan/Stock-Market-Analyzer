from django.db import models
from django.contrib.auth.models import User

class Stock_Companies(models.Model):
    symbol = models.CharField(max_length=30,default=None,null=True)
    name = models.CharField(max_length=150,default=None,null=True)
    sectorName = models.CharField(max_length=300,default=None,null=True)
 
    class Meta:
        db_table='Stock_Companies'
        ordering = ['symbol']
 
    def __str__(self):
        return str(self.symbol)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    reset_password = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username