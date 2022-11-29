from datetime import datetime, timedelta, timezone
from typing import List, Optional
from dateutil import parser
import requests

from content.constants import YOUTUBE_VIDEOS_API_URL, YOUTUBE_VIDEOS_API_KEY, EXTERNAL_REQUESTS_TIMEOUT_IN_SECONDS
from content.models.video import Video
from content.services.elasticsearch import ContentES


class BaseYoutubeData:
    topic_id:str = None # * Youtube specified topic IDs https://developers.google.com/youtube/v3/docs/search/list

    def __init__(self, topic_id: Optional[str]=None) -> None:
        # ! Overrides the topic_id if a string is passed.
        self.topic_id = topic_id or self.topic_id

    @classmethod
    def fetch(cls, part: str="snippet", content_type: str="videos", seconds_ago: int=60, max_results: int=50) -> list:
        now = datetime.now(tz=timezone.utc)
        since_time = now - timedelta(seconds=seconds_ago)
        since_time_string = since_time.isoformat()
        items = []
        params = {"part": part, "type": content_type, "max_results": max_results, "topicId": cls.topic_id, "publishedAfter": since_time_string, "order": "date", "key": YOUTUBE_VIDEOS_API_KEY}
        response = requests.get(YOUTUBE_VIDEOS_API_URL, params=params, timeout=EXTERNAL_REQUESTS_TIMEOUT_IN_SECONDS)
        if not response.ok:
            print("No items found", response.text)
            return items
        response = response.json()
        items.extend(response["items"])

        while response.get("nextPageToken"):
            params["nextPageToken"] = response["nextPageToken"]
            response = requests.get(YOUTUBE_VIDEOS_API_URL, params=params, timeout=EXTERNAL_REQUESTS_TIMEOUT_IN_SECONDS)
            if not response.ok:
                # ! Some Error Occurred
                break
            response = response.json()
            items.extend(response["items"])

        return items

    @classmethod
    def process(cls) -> list:
        youtube_videos: list = cls.fetch()

        data = []
        for video in youtube_videos:
            video_snippet = video["snippet"]
            video_info = {
                "id": video["id"]["videoId"],
                "published_at": video_snippet["publishedAt"],
                "title": video_snippet["title"],
                "description": video_snippet["description"],
                "channel_id": video_snippet["channelId"],
                "channel_name": video_snippet["channelTitle"],
            }
            data.append(video_info)
        return data

    @classmethod
    def load_in_elasticsearch(cls, data: List[Video]):
        documents = []
        for video in data:
            document = {
                "id": str(video.id),
                "title": video.title,
                "description": video.description
            }
            documents.append(document)
            ContentES().insert(document)
        return documents

    @classmethod
    def load_in_database(cls, data: list) -> list:
        queries = []
        for video_info in data:
            published_timestamp_iso = video_info.get("published_at")
            published_at = parser.parse(published_timestamp_iso) if published_timestamp_iso else None
            video_obj = Video(
                source_video_id=video_info.get("id"),
                published_at=published_at,
                source_channel_id=video_info.get("channel_id"),
                source_channel_name=video_info.get("channel_name"),
                title=video_info.get("title"),
                description=video_info.get("description"),
            )
            queries.append(video_obj)

        videos = Video.objects.bulk_create(queries)
        return videos

    @classmethod
    def load(cls) -> None:
        data: list = cls.process()
        videos = cls.load_in_database(data)
        cls.load_in_elasticsearch(videos)
        return videos
