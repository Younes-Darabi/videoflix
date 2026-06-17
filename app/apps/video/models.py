from django.db import models


class Video(models.Model):
    """Represents a video with metadata, thumbnail, and HLS-converted files."""

    class CATEGORY(models.TextChoices):
        DRAMA = "drama", "Drama"
        ROMANCE = "romance", "Romance"
        ACTION = "action", "Action"
        COMEDY = "comedy", "Comedy"
        THRILLER = "thriller", "Thriller"
        HORROR = "horror", "Horror"
        DOCUMENTARY = "documentary", "Documentary"
        ANIMATION = "animation", "Animation"
        SCIFI = "scifi", "Sci-Fi"

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    thumbnail_url = models.ImageField(upload_to="thumbnails/")
    category = models.CharField(choices=CATEGORY.choices, max_length=20)
    video_file = models.FileField(upload_to="videos/raw/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
