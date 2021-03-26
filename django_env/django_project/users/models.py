from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # overwrite save() from parent class, accept all arguments that parent class expected.
    def save(self, *args, **kawrgs):
        super().save(*args, **kawrgs) # run save() method from parent class

        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300) # tuple
            img.thumbnail(output_size)
            img.save(self.image.path)