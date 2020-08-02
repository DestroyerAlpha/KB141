import requests,webbrowser
import concurrent.futures
from bs4 import BeautifulSoup
from django.db.models import Q
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
    
    papers = research_paper.objects.all().order_by('-created_on')
    postpapers = []
    postpapersbyauth = []
    postpapersbytag = []
    users = Profile_student.objects.all().order_by('-rating')
    cusers = Profile_corporate.objects.all().order_by('-rating')
    papersbyauth = []
    papersbytag = []
    userbyname = []
    userbycollege = []
    cuserbyname = []
    cuserbyinsti = []
    posts = []
    search = False
    if request.method == 'POST' :
        name = request.POST.get("search","")
        if name != "" :
            search = True
            #for users(students) filter 
            userbyname = Profile_student.objects.filter( Q(user__username__contains=name) | Q(user__first_name__contains=name) | Q(user__last_name__contains=name))
            userbycollege = Profile_student.objects.filter(institution__contains = name)

            #for users(company)
            cuserbyname = Profile_corporate.objects.filter( Q(user__username__contains=name) | Q(user__first_name__contains=name) | Q(user__last_name__contains=name))
            cuserbyinsti = Profile_corporate.objects.filter(institution__contains = name)

            #for paper filter
            papersbyauth = research_paper.objects.filter(authors__user__username__contains=name).order_by('-created_on')
            papersbytag = research_paper.objects.filter(tags__tag__contains=name).distinct().order_by('-created_on')

            posts = Post.objects.filter( Q(paper__authors__user__username__contains=name) |  Q(content__contains=name) | Q(author__user__username__contains=name) | Q(author__user__first_name__contains=name) | Q(author__user__last_name__contains=name)).order_by('-date_posted')

	
	#google scraper
	gscraper(name)
	#rsscraper
	rgscraper(name)
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
        'posts' : posts,
        'papersbyauth' : resultpapersbyauth,
        'papersbytag' : resultpapersbytag,
        'userbyname' : userbyname,
        'userbycollege' : userbycollege,
        'cusers' : cusers,
        'cuserbyname' : cuserbyname,
        'cuserbyinsti' : cuserbyinsti,
    }
    return render(request, 'home/rs_filter.html', rtn)

def gscraper(name):
    global gsearch
    google_search = requests.get("https://scholar.google.com/scholar?q=" + name)
    soup = BeautifulSoup(google_search.text,'html.parser')
    gtitle = []
    glink = []
    gtext = []
    gcites = []
    
    searchresults = soup.select('.gs_rt a')
    for result in searchresults:
        gtitle.append(''.join(result.findAll(text=True)))
        glink.append(result.get('href'))
    
    searchresults = soup.select('.gs_rs')
    for result in searchresults:
        gtext.append(''.join(result.findAll(text=True)))
    
    searchresults = soup.select('.gs_fl a:nth-of-type(3)')
    for results in searchresults:
        gcites.append(results.text)
    gsearch = zip(gtitle, glink, gtext, gcites)

def rgscraper(name):
    global rgsearch
    rg_search = requests.get("https://www.researchgate.net/search/publication?q=" + name)
    soup = BeautifulSoup(rg_search.text,'html.parser')
    print('\n\n\n\n\n\n in rg scaper')
    file1 = open('output.html','w')
    print(soup.prettify(),file=file1)
    file1.close()
    
    
    searchresults = soup.select('.nova-v-publication-item__body .nova-e-link.nova-e-link--color-inherit.nova-e-link--theme-bare')
    dateresults = soup.select('.nova-v-publication-item__body .nova-v-publication-item__meta-right li:nth-of-type(1)')
    authorsresultsp = soup.select('.nova-v-publication-item__body') #ul.nova-e-list.nova-e-list--size-m.nova-e-list--type-inline.nova-e-list--spacing-none.nova-v-publication-item__person-list')
    authorsresults = authorsresultsp.find(' .nova-e-list.nova-e-list--size-m.nova-e-list--type-inline.nova-e-list--spacing-none.nova-v-publication-item__person-list')
    rgtitle = []
    rglink = []
    rgdate = []
    rgauthors = []
    for result,date,authors in zip(searchresults,dateresults,authorsresults):
        if(''.join(result.findAll(text=True)) == ''):
            print('no')
            break
        print('yo')
        rgtitle.append(''.join(result.findAll(text=True)))
        rglink.append('https://www.researchgate.net/' + result.get('href'))
        rgdate.append(date.text)
        # try :
        #     temp = authors.find('ul.nova-e-list.nova-e-list--size-m.nova-e-list--type-inline.nova-e-list--spacing-none.nova-v-publication-item__person-list')
        # except :
        #     temp = None
        # if not temp:
        #     rgauthors.append('')
        # else:
        #     rgauthors.append(temp)
    rgsearch = zip(rgtitle, rglink, rgdate, rgauthors)
