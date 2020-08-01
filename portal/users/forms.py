from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile_student, Profile_corporate

class RegistrationForm(UserCreationForm):
    '''
        basic registration form for both researchers and companies.
    '''
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user

class student_form(ModelForm):
    '''
        form to collect more information about user if researcher
    '''
    class Meta:
        model = Profile_student
        fields = [
            'institution',
            'institute_email',
            'profile_picture',
        ]

class corporate_form(ModelForm):
    '''
        form to collect more information about user if company people
    '''
    class Meta:
        model = Profile_corporate
        fields = [
            'institution',
            'email',
            'role',
            'profile_picture',
        ]

