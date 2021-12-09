from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save  # will run everytime a user is saved in database
from django.dispatch import receiver
import os, random, pdb
from taggit.managers import TaggableManager


# Create your models here.

class Post(models.Model):
    '''
    will need 3 fields here, body (text), created on date, and user that created post.
    '''
    body = models.TextField()
    # to upload images
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    # Always defaults current time, user cannot change time
    created_on = models.DateTimeField(default=timezone.now)
    # Finds user that is loged in and substitutes that into field
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # to hold likes:
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    comments = models.ManyToManyField(User, blank=True, related_name='comments')
    #slug = models.SlugField(unique=True, max_length=100) # from a tutorial and not necessary for my project
    tags = TaggableManager()


class Comment(models.Model):
    '''Make a comment model so that users can comment on posts!'''
    # will need time stamp, post, and author (USER), similar to POST model :)
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # another field for posts, needs foreign new to origin post, and then on_delete... so that
    # if the post is deleted, the comments are also all deleted
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Reply(models.Model):
    reply = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


def random_image():
    '''to get random image for default profile'''

    default_img = random.choice(os.listdir("media/uploads/profile_pictures"))
    image_path = 'uploads/profile_pictures/' + default_img

    return image_path


class UserProfile(models.Model):
    ''' a class for user profiles '''
    # give user field to link to users w/ foreign key
    # one profile per user (one to one)
    # can access using 'profile'
    # way to delete user profile
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile',
                                on_delete=models.CASCADE)
    ### attributes of user:
    ### allowed to be empty so no errors
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    # default image of bull-dog
    picture = models.ImageField(upload_to='uploads/profile_pictures', default=random_image, blank=True)
    # add area to store followers and add to field
    followers = models.ManyToManyField(User, blank=True, related_name='followers')


## user sender/receiver to make new profiles when a person registers"


# both need receiver decorator:
@receiver(post_save, sender=User)  # once user saved in database, then we want to run:
def create_user_profile(sender, instance, created, **kwargs):
    ''' creates user profile '''
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    ''' saves profile '''
    instance.profile.save()
