from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from .models import Note

admin.site.register(Note)