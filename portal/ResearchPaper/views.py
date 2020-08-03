from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import research_paper_form
from django.contrib import messages
# only student profile because only researchers can publish, companies cannot
from users.models import Profile_student
from django.contrib.auth.models import User

@login_required
def research_paper(request):
    form = research_paper_form(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            research_paper = form.save(commit=False)
            research_paper.save()
            # for manytomany author field
            form.save_m2m()
            messages.success(request, "Thanks. Your information is saved successfully. You can edit it and save again OR Click Finish to move ahead.")
            return redirect('paper-post-create', research_paper.id)
        else:
            print(form.errors)
            messages.error(request, "couldn't save your response")
    else :    
        query_result_student_profile = Profile_student.objects.all().filter(user = request.user)
        # length of query result will be 0 if user is not student(i.e she/he is not researcher)....And form to add paper will not be passed :)
        if(len(query_result_student_profile) == 0):
            form = "sorry, you can't publish a paper. You are company person. :("
            # to indicate that she/he is company person...not researcher
            researcher = 0
        else :
            form = research_paper_form()
            # to indicate that she/he is not company person...but is researcher
            researcher = 1
    return render(request, 'ResearchPaper/add_paper.html', {'form':form, 'is_allowed' : researcher})
