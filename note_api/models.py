from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.conf import settings
class Note(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	created_at = models.DateTimeField(default=timezone.now)
	creater = models.ForeignKey('auth.user',on_delete=models.CASCADE)
	def __str__(self):
		return self.name

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance)
