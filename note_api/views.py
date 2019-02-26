from django.shortcuts import render,Http404
from rest_framework import status
import os
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from google.cloud import translate
from rest_framework import permissions
import json
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import NoteSerializer
from .models import Note
import functools

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getcwd()+"/translate.json"
class Register(APIView):

	permission_classes = (AllowAny,)

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
				with open(user.username+".json", "w") as write_file:
				    json.dump([], write_file)
				return Response({"message":"User Created","flag":True},status=status.HTTP_201_CREATED)
			except:
				return Response({"message":"Unable to create User"},status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"message":"Please provide correct details"},status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

	permission_classes = (AllowAny,)

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

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_object(self,pk):
		try:
			return Note.objects.get(pk=pk)
		except Note.DoesNotExist:
			raise Http404	

	def get(self,request,pk):
		translate_client = translate.Client()
		notes   = self.get_object(pk=pk)
		serializer = NoteSerializer(notes).data
		x=serializer['name']
		y=serializer['description']
		target='hi'
		translated_description = translate_client.translate(y,target_language='hi')
		print(translated_description)
		serializer['description']=translated_description['translatedText']
		translated_description = translate_client.translate(x,target_language='hi')
		print(translated_description)	
		serializer['name']=translated_description['translatedText']
		return Response(serializer)


class NoteList(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self,request,format=None):
		token,created = Token.objects.get_or_create(user=self.request.user)
		file=open(self.request.user.username+".json","r")
		file_data=json.load(file)
		return Response({"objects":file_data})

	def post(self,request):
		serializer = NoteSerializer(data=request.data)
		data = request.data
		if serializer.is_valid():
			data=dict()
			token,created = Token.objects.get_or_create(user=self.request.user)
			data.update(serializer.data)
			data['creater']=token.key
			file=open(self.request.user.username+".json","r")
			file_data=json.load(file)
			data['id']=len(file_data)+1
			file_data.append(data)
			file.close()
			file=open(self.request.user.username+".json","w")
			json.dump(file_data,file,indent=4)
			file.close()			
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class NoteDetailView(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_object(self,pk):
		try:
			file=open(self.request.user.username+".json","r")
			file_data=json.load(file)
			x = filter(lambda x : x['id']==int(pk),file_data) 
			file.close()
			return list(x)[0]
		except :
			return {"message":"Note Does Not Exists"}	

	def get(self,request,pk):
		notes   = self.get_object(pk=pk)
		return Response(notes)

	def patch(self,request,pk,format=None):
		serializer = self.get_object(pk=pk)
		token,created = Token.objects.get_or_create(user=request.user)
		file=open(self.request.user.username+".json","r")
		file_data=json.load(file)
		file.close()
		data_changed={"message":"No data found"}
		for i in file_data:
			if i['id']==int(pk):
				i['description']=request.data.get("description")
				i['name']=request.data.get("name")
				data_changed=i
				break
		file=open(self.request.user.username+".json","w")
		json.dump(file_data,file,indent=4)
		file.close()				
		return Response(data_changed,status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self,request,pk,format=None):
		note = self.get_object(pk)
		note.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)