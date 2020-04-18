from django.contrib import admin
from .models import Profile, BookReadingStatus, ReadHistory


# Register your models here.
# admin.site.register(Profile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'birth_date', 'profile_img']


admin.site.register(BookReadingStatus)

admin.site.register(ReadHistory)
