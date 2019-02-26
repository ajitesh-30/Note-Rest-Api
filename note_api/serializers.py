from rest_framework import serializers
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
class NoteSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	name = serializers.CharField(default=None,max_length=256)
	description = serializers.CharField(max_length=500)
	creater = serializers.ReadOnlyField(source='creater.username',read_only=True)

	def create(self,validated_data):
		return Notes(id=1,**validated_data)
