from django.urls import path

from content.apis.videos import VideosAPI

urlpatterns = [
    path("videos", VideosAPI.as_view()),
]
