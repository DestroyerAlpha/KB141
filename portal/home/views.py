from django.shortcuts import render,HttpResponse
from django.views import generic
from users.models import Profile_student,Profile_corporate
import datetime
from ResearchPaper.models import research_paper, paper_tag
from feed.models import Post

def home(request):
    try:
        username = request.user.username
        # search for user in user model. this is being passed to template
        requested_user = User.objects.get(username=username)
        # search for user whose profile is begin searched
        searched_user = User.objects.filter(username = username)
        try:
            # search student profile models by user which could be passed to profile.html to display information
            profile = Profile_student.objects.get(user__in = searched_user)
        except:
            # search corporate profile models by user which could be passed to profile.html to display information
            profile = Profile_corporate.objects.get(user__in = searched_user)
        profile.authors_followed.add(profile)
        return render(request, 'home/home.html')
    except:
        return render(request, 'home/home.html')

def rs_filter(request):
    papers = research_paper.objects.all()
    postpapers = []
    postpapersbyauth = []
    postpapersbytag = []
    users = Profile_student.objects.all()
    cusers = Profile_corporate.objects.all()
    papersbyauth = []
    papersbytag = []
    userbyname = []
    userbycollege = []
    cuserbyname = []
    cuserbyinsti = []
    search = False
    if request.method == 'POST' :
        name = request.POST.get("search","")
        if name != "" :
            search = True
            #for users(students) filter 
            userbyname1 = Profile_student.objects.filter(user__username__contains=name)
            userbyname2 = Profile_student.objects.filter(user__first_name__contains=name)
            userbyname3 = Profile_student.objects.filter(user__last_name__contains=name)
            userbyname = (userbyname1 | userbyname2 | userbyname3).distinct()
            userbycollege = Profile_student.objects.filter(institution__contains = name)

            #for users(company)
            cuserbyname1 = Profile_corporate.objects.filter(user__username__contains=name)
            cuserbyname2 = Profile_corporate.objects.filter(user__first_name__contains=name)
            cuserbyname3 = Profile_corporate.objects.filter(user__last_name__contains=name)
            cuserbyname = (cuserbyname1 | cuserbyname2 | cuserbyname3).distinct()
            cuserbyinsti = Profile_corporate.objects.filter(institution__contains = name)

            #for paper filter
            papersbyauth = research_paper.objects.filter(authors__user__username__contains=name)
            papersbytag = research_paper.objects.filter(tags__tag__contains=name).distinct()


    for p in papers:
        post = Post.objects.filter(paper__id = p.id)
        for po in post:
            postpapers.append(po)
    
    for p in papersbyauth:
        post = Post.objects.filter(paper__id = p.id)
        for po in post:
            postpapersbyauth.append(po)
    
    for p in papersbytag:
        post = Post.objects.filter(paper__id = p.id)
        for po in post:
            postpapersbytag.append(po)

    resultpapers = zip(postpapers,papers)
    resultpapersbyauth = zip(postpapersbyauth,papersbyauth)
    resultpapersbytag = zip(postpapersbytag,papersbytag)
    rtn = {
        'name' : name,
        'search' : search,
        'papers' : resultpapers,
        'users' : users,
        'papersbyauth' : resultpapersbyauth,
        'papersbytag' : resultpapersbytag,
        'userbyname' : userbyname,
        'userbycollege' : userbycollege,
        'cusers' : cusers,
        'cuserbyname' : cuserbyname,
        'cuserbyinsti' : cuserbyinsti,
    }
    return render(request, 'home/rs_filter.html', rtn)