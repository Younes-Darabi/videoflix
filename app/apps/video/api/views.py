from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
import os

from .serializers import VideoSerializer
from ..models import Video


class VideoView(generics.ListAPIView):
    
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class VideoManifestView(APIView):

    def get(self, request, movie_id, resolution):
        path = f'/app/media/videos/{movie_id}/{resolution}/index.m3u8'
        if not os.path.exists(path):
            return Response(status=status.HTTP_404_NOT_FOUND)
        return FileResponse(open(path, 'rb'), content_type='application/vnd.apple.mpegurl')
    
    
class VideoSegmentView(APIView):
    
    def get(self, request, movie_id, resolution, segment):
        path = f'/app/media/videos/{movie_id}/{resolution}/{segment}'
        if not os.path.exists(path):
            return Response(status=status.HTTP_404_NOT_FOUND)
        return FileResponse(open(path, 'rb'), content_type='video/MP2T')