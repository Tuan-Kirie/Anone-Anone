from django.contrib import admin
from .models import Blog
from django import forms
from ckeditor.widgets import CKEditorWidget

class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = ['author', 'text', 'published_date']


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Blog, PostAdmin)
