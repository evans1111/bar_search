from django.contrib import admin

# Load in the Post model
from .models import Post

# Register the post within the admin page
admin.site.register(Post)
