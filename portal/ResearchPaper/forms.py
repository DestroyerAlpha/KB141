from django.forms import ModelForm
from .models import research_paper, paper_tag
from django.contrib.auth.forms import UserCreationForm

class research_paper_form(ModelForm):
    class Meta:
        model = research_paper
        fields = [
            'file',
            'title',
            'authors',
            'tags',
            'Private',
        ]
