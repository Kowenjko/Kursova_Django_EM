from django.contrib import admin
from .models import  account_data
# Register your models here.
class UserData(admin.ModelAdmin):
    list_display = ['username', 'key', 'value']
    list_filter = ['username']
admin.site.register(account_data, UserData)