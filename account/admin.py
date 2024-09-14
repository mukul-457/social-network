from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth','image']
    raw_id_fields = ['user']
