from django.shortcuts import render,Http404
from rest_framework import status
import os
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from google.cloud import translate
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import NoteSerializer
from .models import Note

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getcwd()+"/translate.json"
class Register(APIView):
	def post(self,request):
		password1 = request.data.get('password1')
		password2 = request.data.get('password2')
		username  = request.data.get('username')

		if password1 and password2 and username and password1==password2:
			try:
				user_exists = User.objects.filter(username=username).exists()
				if user_exists:
					return Response({"message":"This user already exists","flag":False},status=status.HTTP_400_BAD_REQUEST)
				user = User.objects.create_user(username=username,password=password1)
				user.is_active=True
				return Response({"message":"User Created","flag":True},status=status.HTTP_201_CREATED)
			except:
				return Response({"message":"Unable to create User"},status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"message":"Please provide correct details"},status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
	def post(self,request):
		username = request.data.get('username')
		password = request.data.get('password')
		try:
			user_obj = authenticate(username=username,password=password)
			if user_obj:
				token,created = Token.objects.get_or_create(user=user_obj)
				return Response({"api_key":token.key},status=status.HTTP_200_OK)
			else:
				return Response({"message":"Wrong password"},status=HTTP_400_BAD_REQUEST)
		except:
			return Response({"message":"Something Went Wrong"},status=status.HTTP_400_BAD_REQUEST)

class Translation(APIView):
	def get_object(self,pk):
		try:
			return Note.objects.get(pk=pk)
		except Note.DoesNotExist:
			raise Http404	
	def get(self,request,pk):
		translate_client = translate.Client()
		notes   = self.get_object(pk=pk)
		serializer = NoteSerializer(notes).data
		x=serializer[0]['description']
		y=serializer[0]['name']
		target='hi'
		serializer[0]['description'] = translate_client.translate(x,target_language=target)
		serializer[0]['name'] = translate_client.translate(y,target_language=target)
		return Response(serializer)


class NoteList(APIView):
	#authentication_classes = (TokenAuthentication,)
	#permission_classes = (IsAuthenticated,)
	def get(self,request,format=None):
		token,created = Token.objects.get_or_create(user=self.request.user)
		notes = Note.objects.filter(creater=token.key)
		data = NoteSerializer(notes,many=True).data
		return Response({"objects":data})

	def post(self,request):
		serializer = NoteSerializer(data=request.data)
		if serializer.is_valid():
			token,created = Token.objects.get_or_create(user=self.request.user)
			serializer.save(creater=token.key)
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class NoteDetailView(APIView):
	#authentication_classes = (TokenAuthentication,)
	#permission_classes = (IsAuthenticated,)
	def get_object(self,pk):
		try:
			return Note.objects.get(pk=pk)
		except Note.DoesNotExist:
			raise Http404	
	def get(self,request,pk):
		notes   = self.get_object(pk=pk)
		serializer = NoteSerializer(notes).data
		return Response(serializer)

	def patch(self,request,pk,format=None):
		serializer = self.get_object(pk=pk)
		serializer = NoteSerializer(serializer,data=request.data).data
		token,created = Token.objects.get_or_create(user=self.request.user)
		if serializer.is_valid():
			serializer.save(creater=self.request.user)
			return Response(serializer.data)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def delete(self,request,pk,format=None):
		note = self.get_object(pk)
		note.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)