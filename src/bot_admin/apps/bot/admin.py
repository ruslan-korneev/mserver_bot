from django.contrib import admin

# Register your models here.
from .models import BotChatUser, BotServer, BotUrl, Project


@admin.register(BotChatUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("__str__", "username", "status", "subscribe")
    list_filter = ("subscribe", "status")


@admin.register(BotServer)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("__str__", "alarm_status", "get_projects")
    list_filter = ("alarm_status", "project")


@admin.register(BotUrl)
class UrlAdmin(admin.ModelAdmin):
    list_display = ("url", "alarm_status", "get_projects")
    list_filter = ("alarm_status", "project")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
