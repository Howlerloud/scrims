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


ACTIVE = ((0, "Playing"), (1, "Sub"))


# Create your models here.
class Usercreate(models.Model):
    Username = models.TextField(max_length=30, unique=True)
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

    role = [
        ('dps', 'DPS'),
        ('support', 'Support'),
        ('tank', 'Tank'),
    ]
    created_on = models.DateTimeField(auto_now_add=True)
    teamstatus = models.IntegerField(choices=ACTIVE, default=1)


