from django.shortcuts import render, redirect
from .forms import research_paper_form
from django.contrib import messages
# only student profile because only researchers can publish, companies cannot
from users.models import Profile_student
from django.contrib.auth.models import User

def research_paper(request):
    form = research_paper_form(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
        
            print(form.errors)
            messages.error(request, "couldn't save your response")
    else :
        q
    return render(request, 'ResearchPaper/add_paper.html', {'form':form, 'is_allowed' : researcher})
