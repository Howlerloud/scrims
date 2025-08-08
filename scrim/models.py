from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class CreateTeam(models.Model):
    RANK = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
        ('grandmaster', 'Grandmaster'),
        ('celestial', 'Celestial'),
        ('eternity', 'Eternity'),
    ]

    created_on = models.DateTimeField(auto_now_add=True)
    team_name = models.CharField(max_length=30, default="No Team!")
    discord_name = models.CharField(max_length=30, default="NA")
    slug = models.SlugField(unique=True, blank=True)
    rank = models.CharField(max_length=200, choices=RANK, default='Bronze')

    # to rename the model to the team name for users to select
    def __str__(self):
        return self.team_name

    # To create a unique slug
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.team_name)
            slug = base_slug
            count = 1
            while CreateTeam.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        super().save(*args, **kwargs)


class LfpModel(models.Model):
    RANK = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
        ('grandmaster', 'Grandmaster'),
        ('celestial', 'Celestial'),
        ('eternity', 'Eternity'),
    ]

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    team = models.ForeignKey(CreateTeam, on_delete=models.CASCADE, related_name='memberships')
    average_rank = models.CharField(max_length=200, choices=RANK, default='Bronze')
    date_created = models.DateTimeField(auto_now_add=True)
