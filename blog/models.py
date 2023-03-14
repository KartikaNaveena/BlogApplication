from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField 
from django.utils import timezone
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content=RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()
    
   
    

   
    

class BlogComment(models.Model):
    blogpost_connected = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

    avatar = models.ImageField(default='avatar.jpg', upload_to='profile_images')
    bio = models.TextField(null=True)

    def __str__(self):
        return self.user.username
