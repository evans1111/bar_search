from django.shortcuts import render

# From our models within the current package/directory, import the Post class
from .models import Post
# from django.http import HttpResponse

# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
