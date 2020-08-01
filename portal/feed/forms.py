from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Comment

class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = ['comment_text']