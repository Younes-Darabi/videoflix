from django.db import models


class Video(models.Model):

    class CATEGORY(models.TextChoices):
        DRAMA='drama','Drama'
        ROMANCE='romance','Romance'
        ACTION='action','Action'

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    thumbnail_url = models.ImageField(upload_to='thumbnails/')
    category = models.CharField(choices=CATEGORY.choices, max_length=20)

    def __str__(self):
        return self.title