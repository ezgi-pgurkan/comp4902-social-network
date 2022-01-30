from django import forms
from .models import *
from django.forms import ModelForm


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'post_image')
        widgets = {
                    'text': forms.Textarea(attrs={ 'cols':35, 'class': 'form-conrol', 'placeholder': 'Write a post...',  'style': ' border-radius: 8px;  padding: 12px;  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);',}),
                    }
'''
class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)
'''