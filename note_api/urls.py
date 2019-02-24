from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as rest_framework_views
from note_api import views
urlpatterns =[
	url(r'^note/(?P<pk>[0-9]+)/translation/',views.Translation.as_view(),name='translation'),
	url(r'^note/(?P<pk>[0-9]+)',views.NoteDetailView.as_view(),name='note-detail'),
	url(r'^note/',views.NoteList.as_view(),name='notes-list'),
	url(r'^generate/',views.Login.as_view(),name='login'),
	url(r'^signup/',views.Register.as_view(),name='signup'),
	#url(r'^generate/',views.GenerateView.as_view(),name='generate_key'),
]
