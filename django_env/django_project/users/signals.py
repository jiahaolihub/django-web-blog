from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# receiver is decorator, once signal - post_save is received, execute / pass all params then save.
# This will create profile with default image after creating new user on site.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# save the profile
@receiver(post_save, sender=User)
def save(sender, instance, **kwargs):
    instance.profile.save()