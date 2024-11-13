from django.db import models
from django.contrib.auth.models import User


class Title (models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    title=models.ForeignKey(Title, on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=300)
    description=models.TextField(null=True,blank=True)
    participant=models.ManyToManyField(User,related_name='participants',blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return self.name
    

class Message (models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-updated','-created']
    
    def __str__(self):
        return self.body[0:50]