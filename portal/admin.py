from django.contrib import admin
from .models import LiteratureType, Literature, School, Division, District, Profile

admin.site.register(LiteratureType)
admin.site.register(Literature)
admin.site.register(Division)
admin.site.register(District)
admin.site.register(Profile)