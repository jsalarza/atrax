from django.contrib import admin
from .models import LiteratureType, Literature

admin.site.register(LiteratureType)
admin.site.register(Literature)