from django import forms
from .models import *
from django.forms import ModelForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'post_image', 'author')
        widgets = {
                    'text': forms.Textarea(attrs={'class': 'form-conrol', 'placeholder': 'Write a post...'}),
                    'author': forms.TextInput(attrs={'class': 'form-conrol', 'value':'', 'id': 'elder', 'type':'hidden'}),
                    }

'''
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post', 'author', 'body')
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-conrol', 'value':'', 'id': 'elder1', 'type':'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-conrol', 'placeholder': 'Write your comment here...'}),
            
                    }
'''