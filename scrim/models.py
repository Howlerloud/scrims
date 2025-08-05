from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


ACTIVE = ((0, "Playing"), (1, "Sub"))


class Sixteam(models.Model):
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
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_on = models.DateTimeField(auto_now_add=True)
    average_rank = models.CharField(max_length=200, choices=RANK, default='Bronze')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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
        ('celestial', 'Celestial'),
        ('eternity', 'Eternity'),
    ]

    rank = models.CharField(max_length=200, choices=RANK, default='Bronze')

    ROLE = [
        ('dps', 'DPS'),
        ('support', 'Support'),
        ('tank', 'Tank'),
    ]

    six_team = models.ForeignKey(
        'Sixteam', on_delete=models.SET_NULL, null=True, blank=True, related_name="userstats"
    )

    team_name = models.CharField(max_length=30, default="teamless!")
    slug = models.SlugField(max_length=30, unique=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE, default='dps')
    created_on = models.DateTimeField(auto_now_add=True)
    team_status = models.IntegerField(choices=ACTIVE, default=1)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Userstat for {self.player.username}"

    def save(self, *args, **kwargs):
        if self.six_team:
            self.team_name = self.six_team.name
        elif not self.team_name:
            self.team_name = "teamless"

        if not self.slug:
            self.slug = slugify(self.team_name)

        super().save(*args, **kwargs)


class TeamMembership(models.Model):
    team = models.ForeignKey('Sixteam', on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_memberships")
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)