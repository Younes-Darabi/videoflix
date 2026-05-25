from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.authentication.api.urls')),
    # path('api/video/', include('apps.video.api.urls')),
]
