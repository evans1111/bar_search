from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
import requests
import json
from users.forms import SearchForm
from django.views.generic.base import TemplateView

# From our models within the current package/directory, import the Post class
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post

class HomePageView(TemplateView):
    template_name = 'blog/home.html'

    def get(self, request):
        api_key='ICFTK388eCNp493fEzwT-hwJCHgGKZi-Hjs-ZNVMThBBzPDduzs8Pya_WCs7tSSAnjqUPjmwrAhMXy3kC3wZlnCnpNo31qgMSSsEjLGW6dP6w09xMlMrX19sCbQcX3Yx'
        url = 'https://api.yelp.com/v3/businesses/search?categories=bars&location={}&reviews?sort_by=rating'
        zip_code = '33703'
        headers = {'Authorization': 'Bearer %s' % api_key}
        r = requests.get(url.format(zip_code), headers=headers).json()

        #converts the json response into a usable dictionary
        bar_name = {
            'name': r['businesses'][0]['name']
        }

        context = {'bar_name' : bar_name}
        return render(request, self.template_name, context)

        

   

def blog(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/blog.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        # Get user associated with the username that we get from the url
        # If the user doesn't exist, return 404 DNE error (using get_object_or_404 from imports)
        user = get_object_or_404(User, username=self.kwargs.get('username')) # Capture the user into user variable if they exist
        return Post.objects.filter(author=user).order_by('-date_posted') # Order by date posted reverse

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/' # Sets the url destination for after a post is created

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author before PostCreateView gets run
        return super().form_valid(form) # Runs form valid method on parent class

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    success_url = '/' # Sets the url destination for after a post is updated

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author before PostCreateView gets run
        return super().form_valid(form) # Runs form valid method on parent class
    
    def test_func(self): # Prevent users from updating other user posts
        post = self.get_object()
        if self.request.user == post.author: # Check if the current user is the author of the post
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # Sets the url destination for after a post is deleted

    def test_func(self): # Prevent users from updating other user posts
        post = self.get_object()
        if self.request.user == post.author: # Check if the current user is the author of the post
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
