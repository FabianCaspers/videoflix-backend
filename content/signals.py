from django.db.models.signals import post_save, post_delete
from .models import Video
from django.dispatch import receiver
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        print('New Video created')
        post_save.connect(video_post_save, sender=Video)
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, created, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)