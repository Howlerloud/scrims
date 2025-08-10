from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


# This allows the user to crate a team on the CreateTeam page which is used in the lfp post
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

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')
    created_on = models.DateTimeField(auto_now_add=True)
    team_name = models.CharField(max_length=30, default="No Team!")
    discord_name = models.CharField(max_length=30, default="NA")
    slug = models.SlugField(unique=False, blank=True)
    rank = models.CharField(max_length=200, choices=RANK, default='Bronze')
    team_logo = CloudinaryField('image', default='placeholder')

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


# Used when making a team post
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
    slug = models.SlugField(unique=False, blank=True)

    # To create a unique slug
    def save(self, *args, **kwargs):
        creating = self.pk is None  # Check if this is a new object

        # Slug generation
        if not self.slug:
            base_slug = slugify(f"{self.team.team_name} - {self.host.username}")
            slug = base_slug
            count = 1
            while LfpModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        super().save(*args, **kwargs)

        # Create 6 empty player slots only for new LfpModel objects
        if creating:
            from .models import PlayerSlot  # Avoid circular imports
            for _ in range(6):
                PlayerSlot.objects.create(lfp=self)


# This links to the player slots when joining or leaving a team
class PlayerSlot(models.Model):
    lfp = models.ForeignKey(LfpModel, on_delete=models.CASCADE, related_name='slots')
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.lfp} - {self.player if self.player else 'Empty slot'}"
