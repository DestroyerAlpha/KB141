from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .forms import student_form, corporate_form, RegistrationForm, student_follow
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import Profile_student, Profile_corporate
from django.contrib.auth.models import User

def student_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            messages.success(request, "Thanks for registering.")
            # being directed to details page to collect more details
            return redirect(reverse('student_detail'))
    else:
        form = RegistrationForm()
    return render(request, 'users/student_register.html', {'form':form})

def corporate_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            messages.success(request, "Thanks for registering.")
            # being directed to details page to collect more details
            return redirect(reverse('corporate_detail'))
    else:
        form = RegistrationForm()
    return render(request, 'users/corporate_register.html', {'form':form})

def user_profile(request, username):
    # pass the details of currently loggedIn user
    try:
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

        try:
            if request.method == 'POST':
                form = student_follow(request.POST)
                if form.is_valid():
                    logged_in = request.user
                    logged_in_user = Profile_student.objects.get(user = logged_in)
                    print(logged_in_user.user.username)
                    print(profile.user.username)
                    logged_in_user.authors_followed.add(profile)
                    form.save()
                else:
                    print("Form is not valid-Error in follow")
            else:
                form = student_follow()
        except:
            #this block is to handle when django loads this page first time - POST will fail and will throw error - so except :)
            print("it's okkk. User came in first time.")

        context = {'form': form, 'current_user': requested_user, 'user_profile': profile, 'searched': requested_user}
        return render(request, 'users/profile.html', context)
    except ObjectDoesNotExist:
        requested_user = None
        return HttpResponse("<h3> 404 User not found<h3> <p> This is returned from HttpResponse, make a template in home app, and render that page and return that before final presentation. </p>")

def student_detail(request):
    if request.method == 'POST':
        form = student_form(request.POST, request.FILES)
        if form.is_valid():
            # commit false because we will add user. see two lines below
            object = form.save(commit=False)
            #automatically filling current user in the form and saving in the next line
            object.user = request.user
            object.save()
            messages.success(request, "Thanks. Your information is saved successfully. You can edit it and save again OR Click Finish to move ahead.")
            return redirect('website-home')
        else:
            print(form.errors)
            messages.error(request, "couldn't save your response")
    else :
        form = student_form()
    return render(request, 'users/student_detail.html', {'form':form})

def corporate_detail(request):
    if request.method == 'POST':
        form = corporate_form(request.POST, request.FILES)
        if form.is_valid():
            # commit false because we will add user. see two lines below
            object = form.save(commit=False)
            #automatically filling current user in the form and saving in the next line
            object.user = request.user
            object.save()
            messages.success(request, "Thanks. Your information is saved successfully. You can edit it and save again OR Click Finish to move ahead.")
            return redirect('website-home')
        else:
            print(form.errors)
            messages.error(request, "couldn't save your response")
    else :
        form = corporate_form()
    return render(request, 'users/corporate_detail.html', {'form':form})
