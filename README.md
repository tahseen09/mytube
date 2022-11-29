# MyTube

### Components / Tools
1. Python with Django framework
2. SQLite Database
3. Elasticsearch for optimised & fast text searches
4. Celery to run periodic asynchronous tasks.
5. Redis as a message broker to celery.


### Usage
1. Clone the repository.
2. Overwrite the Youtube API key in `content/constants.py` in the variable - `YOUTUBE_VIDEOS_API_KEY`.
3. On terminal, run `docker compose up --build` which would build the docker image and also start the container.
4. The cron is set up to run every minute and writes the API response to Database & Elasticsearch.
5. The Search API can be reached at `localhost:8000/content/videos?q=search_text`. Pagination is supported.


#### Improvements (ToDo)
1. An env file should be used for values such as API KEY.
2. Rotation of API Keys could be achieved using Redis and setting the new value of API Key could happen when the current one reaches it's quota.
3. Being an F1 fan, I have chosen motorsports as a topic, feel free to change the topic_id in `content/pipelines/youtube/motorsport.py`
