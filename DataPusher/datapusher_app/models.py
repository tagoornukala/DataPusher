from django.db import models
from django.utils.crypto import get_random_string
# Create your models here.
class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100)
    account_name = models.CharField(max_length=100)
    app_secret_token = models.CharField(max_length=100,unique=True,blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.account_name
    
    def save(self,*args,**kwargs):
        if not self.app_secret_token:
            self.app_secret_token = get_random_string(32)
        super().save(*args,**kwargs)
        

class Destination(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=100)
    headers = models.JSONField()

    def __str__(self):
        return self.url
    