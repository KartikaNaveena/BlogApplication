from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from ckeditor.fields import RichTextField 
from django.utils import timezone



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
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()
    def number_of_likes(self):
        return self.likes.count()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images',null=True)
    bio = models.TextField(null=True)

    def __str__(self):
        return self.user.username
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)
        instance.profile.save()
   
    

class BlogComment(models.Model):
    blogpost_connected = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]
