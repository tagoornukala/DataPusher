from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Account)
class Account_admin(admin.ModelAdmin):
    list_display = ['account_id','email','account_name','app_secret_token','website']

@admin.register(Destination)
class Destination_admin(admin.ModelAdmin):
    list_display = [ 'url','http_method','headers']