from django.shortcuts import render,Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import NoteSerializer
from .models import Note
class NoteList(APIView):
	def get(self,request,format=None):
		notes = Note.objects.all()
		data = NoteSerializer(notes,many=True).data
		return Response(data)

	def post(self,request,format=None):
		serializer = NoteSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(creater=self.request.user)
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def delete(self,request,pk,format=None):
		notes = self.get_object(pk)
		notes.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class NoteDetailView(APIView):
	authentication_classes = (SessionAuthentication,BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	def get_object(self,pk):
		try:
			return Note.objects.get(pk=pk)
		except Note.DoesNotExist:
			raise Http404	
	def get(self,request,pk):
		notes   = self.get_object(pk=pk)
		serializer = NoteSerializer(notes)
		return Response(serializer.data)

	def patch(self,request,pk,format=None):
		serializer = self.get_object(pk=pk)
		serializer = NoteSerializer(serializer,data=request.data)
		if serializer.is_valid():
			serializer.save(creater=self.request.user)
			return Response(serializer.data)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def delete(self,request,pk,format=None):
		note = self.get_object(pk)
		note.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class GenerateView(APIView):
	def post(self,request,*args,**kwargs):
		serializer = self.serializer_class(data=request.data,
										context={'request':request})
		serializer.is_valid(raise_exception=True)

		user = serializer.validated_data['user']
		token,created = Token.objects.get_or_create(user=user)
		return Response({
			'token':token.key,
			})