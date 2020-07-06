from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # Used instead of Redirect. Redirect will redirect to a specific route | Reverse will return the full url to that route as a string
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    # Returns the post instance's details page 
    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})
        
