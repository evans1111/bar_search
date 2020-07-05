from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Add: on_delete=models.CASCADE as a second argument for handline deleting accounts but not the user
    image = models.ImageField(default='default.jpg', upload_to='account_pics')

    def __str__(self):
        return f'{self.user.username} Account'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Inherit the image from the parent class. 
        # Save the image as an instance of itself
        img = Image.open(self.image.path)
        # Re-size the image if it's too large
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)