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
