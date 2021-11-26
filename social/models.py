from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

# Create your models here.

class Post(models.Model):
	'''
	will need 3 fields here, body (text), created on date, and user that created post.
	'''
	body = models.TextField()
	# Always defaults current time, user cannot change time
	created_on = models.DateTimeField(default=timezone.now)
	# Finds user that is loged in and substitutes that into field
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
	'''Make a comment model so that users can comment on posts!'''

	# will need time stamp, post, and author (USER), similar to POST model :) 

	comment = models.TextField()
	created_on = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	# another field for posts, needs foreign new to origin post, and then on_delete... so that
	# if the post is deleted, the comments are also all deleted
	post = models.ForeignKey('Post', on_delete=models.CASCADE)

