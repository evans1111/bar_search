from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Tutorial Ep. 9 - Senders & Receivers
from django.dispatch import receiver
from .models import Account

# @ symbol is called a Decorator. It takes 2 args: Sender & Receiver
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

# Save profile function
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.account.save()
