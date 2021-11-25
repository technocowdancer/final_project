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

