from rest_framework import serializers
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Note
from .object import Notes
class NoteSerializer(serializers.ModelSerializer):
	creater = serializers.ReadOnlyField(source='creater.username',read_only=True)
	
	class Meta:
		model = Note
		fields = '__all__'
