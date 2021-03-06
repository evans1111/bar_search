from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
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
       
# Home Page
def home(request):
    api_key='ICFTK388eCNp493fEzwT-hwJCHgGKZi-Hjs-ZNVMThBBzPDduzs8Pya_WCs7tSSAnjqUPjmwrAhMXy3kC3wZlnCnpNo31qgMSSsEjLGW6dP6w09xMlMrX19sCbQcX3Yx'
    url = 'https://api.yelp.com/v3/businesses/search?categories=bars&location={}&reviews?sort_by=rating'
    headers = {'Authorization': 'Bearer %s' % api_key}
    params = {
        'limit': 20,
        'radius': 10000,
        'offset': 50

    }
    form = SearchForm()
    if request.method == "GET":
        form = SearchForm(request.GET or None)
        if form.is_valid():
            # Append user entry (zip code) onto the endpoint url
            zc = form.cleaned_data["zip_code"]

            # Save the json dictionary to business_data
            try:
                business_data = requests.get(url.format(zc), headers=headers, params=params).json()
            except requests.exceptions.RequestException:
                #Handle incase you're unable to get the response
                redirect('about/')
                
            else:
                # Re-instantiate the form after it's submitted
                form = SearchForm()

                # Save the json response into a new dictionary
                context = {
                    'businesses': business_data['businesses']
                }
                
                print(context)
                # Return the data so that it is available for the home page template
                return render(request, 'blog/home.html', context)     
    else:
        redirect('/')
    
    return render(request, 'blog/home.html', {"form": form})      

# Blog Page
def blog(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/blog.html', context)

# Blog List
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
    form = SearchForm()
    return render(request, 'blog/about.html', {'form': form})
