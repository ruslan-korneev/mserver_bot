from django.db import models

# Create your models here.
class User(models.Model):
	""" docstring for User """
	
	username = models.CharField(max_length=32)
	chat_id = models.IntegerField(blank=True)


class Url(models.Model):
	""" docs for Url """

	url = models.TextField(blank=True)
	alarm_status = models.BooleanField(blank=True)

class Server(models.Model):
	""" docs for Server """

	host = models.CharField(max_length=15)
	username = models.CharField(max_length=32)
	path_to_key = models.TextField(blank=True)
	alarm_status = models.BooleanField(blank=True)