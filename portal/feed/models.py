from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ResearchPaper.models import research_paper
from users.models import Profile_student

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Profile_student, on_delete=models.CASCADE)
    paper = models.ForeignKey(research_paper,null=True, blank=True, on_delete=models.CASCADE)
    post_like = models.ManyToManyField(User, blank=True, related_name="post_liked")
    post_save = models.ManyToManyField(User, blank=True, related_name="post_saved")
    def get_absolute_url(self):
        return reverse('feed')


class Comment(models.Model):
    class Meta:
        db_table = "comment"
    comment_post = models.ForeignKey('Post',
        related_name='comment_post_key',
        on_delete=models.CASCADE
    )
    comment_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_author_key"
    )
    comment_text = models.TextField()
    comment_created_date = models.DateTimeField(
        default=timezone.now
    )
    comment_like = models.ManyToManyField(User, blank=True, related_name="comment_liked")
