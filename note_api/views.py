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
import functools


#For translation
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.getcwd()+"/translate.json"
translate_client = translate.Client()

#Creating New User
class Register(APIView):

	permission_classes = (AllowAny,)

	def post(self,request):

		username  = request.data.get('username')
		password1 = request.data.get('password1')
		password2 = request.data.get('password2')
		
		if password1 and password2 and username and password1==password2:
			try:
				user_exists = User.objects.filter(username=username).exists()
				if user_exists:
					return Response({"message":"This user already exists","flag":False},status=status.HTTP_400_BAD_REQUEST)
				user = User.objects.create_user(username=username,password=password1)
				user.is_active=True
				#Creates a json file for each new user having all its notes
				with open(os.getcwd()+"/static/"+user.username+".json", "w") as write_file:
				    json.dump([], write_file)

				#Creates a json file for storing translation of each note created above
				with open(os.getcwd()+"/static/"+user.username+"_translation.json", "w") as write_file:
				    json.dump([], write_file)

				return Response({"message":"User Created","flag":True},status=status.HTTP_201_CREATED)
			except:
				return Response({"message":"Unable to create User"},status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"message":"Please provide correct details"},status=status.HTTP_400_BAD_REQUEST)

#Logs in the user and creates the token(URL : /api/generate/)
class Login(APIView):

	permission_classes = (AllowAny,)

	def post(self,request):
		username = request.data.get('username')
		password = request.data.get('password')
		try:
			user_obj = authenticate(username=username,password=password)
			if user_obj:
				#Token creation for each logged in user
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

			file=open(os.getcwd()+"/static/"+self.request.user.username+"_translation.json","r")
			file_data=json.load(file)
			#Get the requested note from all notes by user
			x = filter(lambda x : x['id']==int(pk),file_data) 
			file.close()
			return list(x)[0]
		except :
			return {"message":"Note Does Not Exists"}	

	def get(self,request,pk):

		notes   = self.get_object(pk=pk)
		return Response(notes)

class NoteList(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self,request,format=None):
		#Get the token for the requested user
		token,created = Token.objects.get_or_create(user=self.request.user)
		#Collect the json file storing the note for the user
		file=open(os.getcwd()+"/static/"+self.request.user.username+".json","r")
		file_data=json.load(file)
		return Response({"objects":file_data})

	def post(self,request):
		serializer = NoteSerializer(data=request.data)
		data = request.data
		if serializer.is_valid():
			data=dict()
			translated_data=dict()

			token,created = Token.objects.get_or_create(user=self.request.user)
			data.update(serializer.data)
			translated_data.update(serializer.data)

			data['creater']=token.key
			translated_data['creater']=token.key

			#For translation of note
			x=translated_data['name']
			y=translated_data['description']

			translated_description = translate_client.translate(y,target_language='hi')
			translated_data['description']=translated_description['translatedText']

			translated_description = translate_client.translate(x,target_language='hi')
			translated_data['name']=translated_description['translatedText']

			file=open(os.getcwd()+"/static/"+self.request.user.username+".json","r")
			file_data=json.load(file)
			trans_id=0

			#Storing id for each note
			if len(file_data)==0:
				data['id']=1
				trans_id=1
			else:
				data['id']=int(file_data[-1]['id'])+1
				trans_id=int(file_data[-1]['id'])+1

			file_data.append(data)
			file.close()
			#Translation_Data
			file_translation=open(os.getcwd()+"/static/"+self.request.user.username+"_translation.json","r")
			file_data_translation=json.load(file_translation)
			translated_data['id']=trans_id
			file_data_translation.append(translated_data)
			file_translation.close()

			file=open(os.getcwd()+"/static/"+self.request.user.username+".json","w")
			json.dump(file_data,file,indent=4)
			file.close()			

			#Translation_Data
			file=open(os.getcwd()+"/static/"+self.request.user.username+"_translation.json","w")
			json.dump(file_data_translation,file,indent=4)
			file.close()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class NoteDetailView(APIView):

	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get_object(self,pk):
		try:
			file=open(os.getcwd()+"/static/"+self.request.user.username+".json","r")
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
		token,created = Token.objects.get_or_create(user=request.user)
		
		file=open(os.getcwd()+"/static/"+self.request.user.username+".json","r")
		file_data=json.load(file)
		file.close()

		data_changed={"message":"No data found"}
		#Change the file for each
		for i in file_data:
			if i['id']==int(pk):
				i['description']=request.data.get("description")
				i['name']=request.data.get("name")
				data_changed=i
				break
		
		file=open(os.getcwd()+"/static/"+self.request.user.username+".json","w")
		json.dump(file_data,file,indent=4)
		file.close()


		#Translation Pattern
		file_translation=open(os.getcwd()+"/static/"+self.request.user.username+"_translation.json","r")
		file_data_translation=json.load(file)
		file.close()
		y=request.data.get("description")
		x=request.data.get("name")

		for i in file_data_translation:
			if i['id']==int(pk):
				translated_description = translate_client.translate(y,target_language='hi')
				i['description']=translated_description['translatedText']
				translated_description = translate_client.translate(x,target_language='hi')
				i['name']=translated_description['translatedText']
		
		file=open(os.getcwd()+"/static/"+self.request.user.username+"_translation.json","w")
		json.dump(file_data_translation,file,indent=4)
		file.close()

		return Response(data_changed,status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self,request,pk,format=None):
		file=open(os.getcwd()+"/static/"+self.request.user.username+".json","r")
		file_data=json.load(file)
		file.close()
		x = list(filter(lambda x : x['id']!=int(pk),file_data))
		file=open(os.getcwd()+"/static/"+self.request.user.username+".json","r")
		json.dump(x,file,indent=4)
		file.close()

		file=open(os.getcwd()+"/static/"+self.request.user.username+"_translation.json","r")
		file_data=json.load(file)
		file.close()
		#Write all files to the already existing file and rejected the file deleted
		x = list(filter(lambda x : x['id']!=int(pk),file_data))
		file=open(os.getcwd()+"/static/"+self.request.user.username+"_translation.json","r")
		json.dump(x,file,indent=4)
		file.close()						
		return Response(status=status.HTTP_204_NO_CONTENT)