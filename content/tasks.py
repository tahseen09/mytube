from celery import shared_task


@shared_task
def load_youtube_videos():
    from content.pipelines.youtube.motorsport import MotorsportYoutubeData

    print("Starting task", "load_youtube_videos")
    MotorsportYoutubeData().load()
    print("Ending task", "load_youtube_videos")
