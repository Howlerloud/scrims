from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import TeamMembership, Userstat


@receiver(post_save, sender=TeamMembership)
def update_userstat_on_approval(sender, instance, created, **kwargs):
    if instance.approved:
        try:
            userstat = Userstat.objects.get(player=instance.user)
            userstat.six_team = instance.team 
            userstat.team_name = instance.team.name
            userstat.save()
        except Userstat.DoesNotExist:
            Userstat.objects.create(
                player=instance.user,
                six_team=instance.team,
                team_name=instance.team.name
            )
    elif not instance.approved:
        try:
            userstat = Userstat.objects.get(player=instance.user)
            userstat.six_team = None
            userstat.team_name = "teamless"
            userstat.save()
        except Userstat.DoesNotExist:
            pass


@receiver(post_delete, sender=TeamMembership)
def remove_userstat_team_on_leave(sender, instance, **kwargs):
    try:
        userstat = Userstat.objects.get(player=instance.user)
        userstat.six_team = None
        userstat.team_name = "teamless"
        userstat.save()
    except Userstat.DoesNotExist:
        pass