from django.db import models
from django.contrib import admin
from users.models import Profile_student
import datetime
import os

class paper_tag(models.Model):
    '''
        class for storing paper tags
    '''
    tag = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.tag
    def __repr__(self):
	    return self.__str__()

admin.site.register(paper_tag)

class research_paper(models.Model):
    '''
        class for storing research papers added by researchers
    '''

    # all files are stored in papers directory
    file = models.FileField(upload_to = "media/papers/")
    created_on = models.DateField(default=datetime.date.today)
    authors = models.ManyToManyField(Profile_student, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss",)
    liked_by = models.ManyToManyField(Profile_student)
    tags = models.ManyToManyField(paper_tag)
    
    def tagsname(self):
        temp = []
        for i in self.tags.all():
            temp.append(i.tag)
        return temp
admin.site.register(research_paper)
