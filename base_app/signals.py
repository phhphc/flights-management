from django.db.models.signals import post_save
from django.contrib.auth.models import User
from base_app.models import CustomUser


def custom_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        CustomUser.objects.create(
            user=instance,
            email=instance.email,
        )
        
post_save.connect(custom_user_profile, sender=User)
