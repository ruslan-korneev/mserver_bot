from django.contrib import admin

# Register your models here.
from .models import User, Url, Server


admin.site.register(User)
admin.site.register(Url)
admin.site.register(Server)