from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    email = models.CharField()

    def __str__(self):
        return self.email
    

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


