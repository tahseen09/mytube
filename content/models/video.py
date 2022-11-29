from django.db import models
from content.models.base import BaseModel


class Video(BaseModel):
    class VideoSource(models.TextChoices):
        YOUTUBE = "youtube", "YOUTUBE"

    source = models.CharField(
        choices=VideoSource.choices,
        default=VideoSource.YOUTUBE,
        null=True,
        blank=True,
        max_length=128,
    )
    published_at = models.DateTimeField(null=True, blank=True)
    source_video_id = models.CharField(null=True, blank=True, max_length=128)
    source_channel_id = models.CharField(null=True, blank=True, max_length=128)
    source_channel_name = models.CharField(null=True, blank=True, max_length=128)
    title = models.CharField(max_length=256, db_index=True)
    description = models.TextField(null=True, blank=True, db_index=True)

    def __str__(self) -> str:
        return self.title
