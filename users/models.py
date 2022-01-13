from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.db.models.signals import post_save


class User(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(verbose_name='Email Address', unique=True)
    username 		= models.CharField(verbose_name='User Name',max_length=30, unique=True)
    name            = models.CharField(verbose_name='Name', max_length=30, blank=True)
    is_active		= models.BooleanField(verbose_name='is_active',default=True)
    is_staff		= models.BooleanField(verbose_name='is_staff',default=False)
    is_superuser	= models.BooleanField(verbose_name='is_superuser',default=False)
    date_joined		= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login		= models.DateTimeField(verbose_name='last login', auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        verbose_name = 'user'
        verbose_name_plural ='users'

class FollowUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   #follower
    follow_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='following') #following
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return "( follower user : "+str(self.user)+")  + (  following user : "+str(self.follow_user)+")"

class Profile(models.Model):
    user       =  models.OneToOneField(User, on_delete=models.CASCADE)
    bio        =  models.TextField(blank=True, null=True)
    timestamp  =  models.DateTimeField(auto_now_add=True)
    updated    =  models.DateTimeField(auto_now=True)
    # followers  =  models.ManyToManyField(User, related_name='following', blank=True)
    image = models.ImageField(upload_to='images/profile', blank=True, null=True,default='images/profile/default.png')
    """
    project_obj = Profile.objects.first()
    project_obj.followers.all() -> All users following this profile
    user.following.all() -> All user profiles I follow
    """

    def __str__(self):
        return str(self.user)

def user_created(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_created, sender=User)