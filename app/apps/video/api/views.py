from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import VideoSerializer
from ..models import Video

class VideoView(generics.ListAPIView):
    
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]