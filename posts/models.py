from django.db import models
from django.db.models import SET_NULL
from User.models import User

class Post(models.Model):
    title = models.CharField( max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    miniature = models.ImageField(upload_to='posts/images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    published = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    
