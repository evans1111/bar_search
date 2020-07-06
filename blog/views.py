from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# From our models within the current package/directory, import the Post class
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

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
