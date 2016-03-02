from django.contrib import admin
from fhsa.models import UserProfile, UserFolder

class FolderAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserFolder, FolderAdmin)