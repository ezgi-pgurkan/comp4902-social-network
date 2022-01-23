from django import forms
from .models import *
from django.forms import ModelForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'post_image', 'author')
        widgets = {
                    'text': forms.Textarea(attrs={'class': 'form-conrol'}),
                    'author': forms.TextInput(attrs={'class': 'form-conrol'}),
                    }
