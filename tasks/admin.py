from django.contrib import admin
from .models import Task

# Register your models here.

# With this, you'll be able to manage your databases in the admin mode 
admin.site.register(Task)