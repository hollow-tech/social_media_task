from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=200)
	text = models.TextField(null=True, blank=True)
	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.title
	
