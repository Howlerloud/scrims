from django.db import models
from django.contrib.auth.models import User


STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"The title of this post is {self.title}"


ACTIVE = ((0, "Playing"), (1, "Sub"))


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.body[:20], f"by {self.author}" 
    
    


# Create your models here.
class Userstat(models.Model):
    player = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="The_Users_name")
    RANK = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
        ('grandmaster', 'Grandmaster'),
        ('clestial', 'Celestial'),
        ('eternity', 'Eternity'),
    ]

    rank = models.CharField(max_length=200, choices=RANK, default='Bronze')

    ROLE = [
        ('dps', 'DPS'),
        ('support', 'Support'),
        ('tank', 'Tank'),
    ]

    role = models.CharField(max_length=30, choices=ROLE, default='dps')
    created_on = models.DateTimeField(auto_now_add=True)
    teamstatus = models.IntegerField(choices=ACTIVE, default=1)
