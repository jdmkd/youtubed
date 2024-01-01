from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ytd_app import views

urlpatterns = [
    path('',views.index, name='index'),
    path("index/", views.index, name="index"),
    path('youtube-video-download-request/',views.download_videos, name='download_videos'),
    # path('youtube-url-info-request/',views.yt_url_info, name='yt_url_info'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

