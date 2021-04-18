from django.contrib import admin

# Register your models here.
from .models import BotChatUser, BotUrl, BotServer


# admin.site.register(User)
admin.site.register(BotChatUser)
admin.site.register(BotUrl)
admin.site.register(BotServer)