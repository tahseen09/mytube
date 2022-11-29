from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from content.constants import API_LOCALHOST_BASE_URL
from content.models.video import Video
from content.services.elasticsearch import ContentES
from django.core.paginator import Paginator


class VideosAPI(View):
    default_page_size = 10

    def get(self, request):
        """
        Gets the videos whose title or description matches the search query.

        Request URL Example - localhost:8000/content/videos?q=lost charles

        Response Example -
        {
            "result": {
                "page": {
                    "current": 1,
                    "has_next": false,
                    "has_previous": false,
                    "next": null,
                    "previous": null
                },
                "data": [
                    {
                        "title": "Charles Gets Lost in the Smoke! 💨 #Shorts",
                        "description": "Ferrari's Charles Leclerc indulged in some post-race donuts in Abu Dhabi... but the smoke was so thick, he couldn't find where to ...",
                        "source": "youtube",
                        "published_at": null
                    }
                ]
            }
        }
        """
        query = request.GET.get("q")
        page_number = int(request.GET.get("page", 1))
        if not query:
            return HttpResponseBadRequest("Please provide query to be searched")

        search_results = ContentES().search(query)

        hits = search_results["hits"]["hits"]
        objects_ids = [result["_source"]["id"] for result in hits]
        videos = (
            Video.objects.filter(id__in=objects_ids)
            .order_by("-published_at")
            .values("title", "description", "source", "published_at")
        )

        paginator = Paginator(videos, self.default_page_size)
        page_obj = paginator.get_page(page_number)
        data = data = list(page_obj.object_list)
        payload = {
            "page": {
                "current": page_obj.number,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
                "next": f"{API_LOCALHOST_BASE_URL}/content/videos?q={query}&page={page_obj.number + 1}"
                if page_obj.has_next()
                else None,
                "previous": f"{API_LOCALHOST_BASE_URL}/content/videos?q={query}&page={page_obj.number - 1}"
                if page_obj.has_previous()
                else None,
            },
            "data": data,
        }
        return JsonResponse({"result": payload})
