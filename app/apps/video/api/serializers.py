from rest_framework import serializers

from ..models import Video


class VideoSerializer(serializers.ModelSerializer):
    """Serializes video metadata for API responses."""

    class Meta:
        model = Video
        fields = [
            "id",
            "created_at",
            "title",
            "description",
            "thumbnail_url",
            "category",
        ]
