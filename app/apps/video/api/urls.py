from django.urls import path

from .views import VideoView, VideoManifestView, VideoSegmentView

urlpatterns = [
    path("", VideoView.as_view(), name="video"),
    path(
        "<int:movie_id>/<str:resolution>/index.m3u8",
        VideoManifestView.as_view(),
        name="manifest",
    ),
    path(
        "<int:movie_id>/<str:resolution>/<str:segment>/",
        VideoSegmentView.as_view(),
        name="segment",
    ),
]
