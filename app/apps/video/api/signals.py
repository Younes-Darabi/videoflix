import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq

from .tasks import convert_480p, convert_720p, convert_1080p
from ..models import Video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('New video created')
        queue = django_rq.get_queue('default')
        if instance.video_file:
            queue.enqueue(convert_480p, instance.video_file.path, instance.id)
            queue.enqueue(convert_720p, instance.video_file.path, instance.id)
            queue.enqueue(convert_1080p, instance.video_file.path, instance.id)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file :
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
