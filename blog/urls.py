from django.urls import path
from .views import PostListView, PostDetailView # Class based views | Allows PostListView.as_view()
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name="blog-home"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"), #pk (primary key) for the blog number
    path('about/', views.about, name="blog-about"),
]
