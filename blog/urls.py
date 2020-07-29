from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, # Class based views | Allows PostListView.as_view()
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    # HomePageView
)
from . import views

# After adding the routes, create a template
urlpatterns = [
    # path('', views.home, name="blog-home"),
    path('', views.home, name="blog-home"),
    path('blog/', PostListView.as_view(), name="blog-blog"),
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"), #pk (primary key) for the blog number
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"), 
    path('about/', views.about, name="blog-about"),
]
