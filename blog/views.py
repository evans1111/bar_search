from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
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
    return render(request, 'blog/home.html')

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
