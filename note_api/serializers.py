from rest_framework import serializers
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Note
from .object import Notes
class NoteSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	name = serializers.CharField(default=None,max_length=256)
	description = serializers.CharField(max_length=500)
	creater = serializers.ReadOnlyField(source='creater.username',read_only=True)

	def create(self,validated_data):
		return Notes(id=1,**validated_data)

	# def update(self,instance,validated_data):
	# 	print(validated_data)
	# 	for field,value in validated_data.items():
	# 		setattr(instance,field,value)
	# 	print(instance)
	# 	return instance
