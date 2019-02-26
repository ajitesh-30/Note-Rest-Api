from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.conf import settings

class Note(models.Model):
	name = models.CharField(default=None,max_length=100,null=True)
	description = models.CharField(max_length=500)
	created_at = models.DateTimeField(default=timezone.now)
	creater = models.CharField(default=None,max_length=100,null=True)
	def __str__(self):
		return self.name

