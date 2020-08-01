from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Profile_student(models.Model):
	# one user is related to one profile and vice versa, and when User is deleted, the profile gets deleted
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

	# for storing name of institution,
	# Should we have a model for each institution as well instead of string ? -- Opinion one - No(it's just prototype, let's keep it simple)
	institution = models.CharField(max_length=100, default='Other')
	institute_email = models.EmailField(max_length=254)

	# each user has a list of papers, make a posts app, and import it here.
	# add many to many field.

	# ELO rating of current user
	rating = models.IntegerField(default=1600)

	# list of authors that current user follows
	authors_followed = models.ManyToManyField('Profile_student', blank=True)

	#image - photo :)
	profile_picture = models.ImageField(upload_to='profile_picture/', default='profile_picture/image.jpg')

	# list of research papers followed, import class definition (ie. model) of ResearchPaper
	# research_papers_followed = models.ManyToManyField(ResearchPaper, blank=True)

	def __str__(self):
		return self.user.username

	def __repr__(self):
		return self.__str__()

# to show this group on admin page ('localhost:3000/admin')
admin.site.register(Profile_student)

class Profile_corporate(models.Model):
	# one user is related to one profile and vice versa, and when User is deleted, the profile gets deleted
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="corporate_profile")

	# for storing name of institution,
	# Should we have a model for each institution as well instead of string ? -- Opinion one - No(it's just prototype, let's keep it simple)
	institution = models.CharField(max_length=100, default='Other')
	#institute email is preferred but not compulsory
	email = models.EmailField(max_length=254)
	role = models.CharField(max_length=100, default='empty')

	# each user has a list of papers, make a posts app, and import it here.
	# add many to many field.

	# ELO rating of current user
	rating = models.IntegerField(default=1600)

	# list of authors that current user follows
	authors_followed = models.ManyToManyField('Profile_corporate', blank=True)

	#image - photo :)
	profile_picture = models.ImageField(upload_to='profile_picture/', default='profile_picture/image.jpg')

	# list of research papers followed, import class definition (ie. model) of ResearchPaper
	# research_papers_followed = models.ManyToManyField(ResearchPaper, blank=True)

	def __str__(self):
		return self.user.username

	def __repr__(self):
		return self.__str__()

# to show this group on admin page ('localhost:3000/admin')
admin.site.register(Profile_corporate)
