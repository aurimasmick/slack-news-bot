import os
import logging
import asyncio
import json
from functools import wraps

import requests
from aiohttp import ClientSession
from slack_sdk import WebClient


HN_API_URL = os.environ.get("HN_API_URL", "https://hacker-news.firebaseio.com/v0")
HN_URL = os.environ.get("HN_URL", "https://news.ycombinator.com")
PH_API_URL = os.environ.get("PH_API_URL", "https://api.producthunt.com/v2/api/graphql")
PH_API_TOKEN = os.environ.get("PH_API_TOKEN", "")
STORIES_NUMBER = int(os.environ.get("STORIES_NUMBER", 3))


logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("Logger")
logger.setLevel(os.environ.get("LOGGING", logging.DEBUG))


def notify_cloudwatch(function):
    """Log wrapper for CloudWatch"""
    @wraps(function)
    def wrapper(event, context):
        logger.info(f"'{context.function_name}' - entry:'{event}'")
        result = function(event, context)
        logger.info(f"'{context.function_name}' - entry.'{result}'")
        return result
    return wrapper


class GetHN:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(os.environ.get("LOGGING", logging.DEBUG))

    async def fetch(self, session, url):
        """Fetch details for a single story"""
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            response = await response.text()
            return json.loads(response)

    async def fetch_all(self, urls):
        """Fetch details for all top stories"""
        async with ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.create_task(self.fetch(session, url))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            return results

    def get_top_stories(self):
        """Get a list of top stories with details"""
        stories = requests.get(f"{HN_API_URL}/topstories.json")
        stories_ids = json.loads(stories.text)
        urls = [f"{HN_API_URL}/item/{story_id}.json" for story_id in stories_ids]
        fetched_stories = asyncio.run(self.fetch_all(urls))
        sorted_stories = sorted(
            fetched_stories, key=lambda k: k["score"], reverse=True)
        return sorted_stories[:STORIES_NUMBER]

    def create_hn_text(self):
        """Create slack text with HackerNews top stories"""
        text_list = [f"Top {STORIES_NUMBER} from HackerNews:"]
        sorted_stories = self.get_top_stories()
        # Format slack text
        for story in sorted_stories:
            text_list.append(
                "*<{}|{}>* - <{}|{}>".format(
                    "{}/item?id={}".format(HN_URL, story["id"]),
                    story["score"],
                    story["url"],
                    story["title"],
                )
            )
        self.logger.debug(text_list)
        return "\n>".join(text_list)


class GetPH:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(os.environ.get("LOGGING", logging.DEBUG))

    def run_graphql_query(
            self,
            query,
            headers,
            status_code=200):
        """Get all daily Product Hunt posts with details"""
        request = requests.post(PH_API_URL, data=json.dumps(query), headers=headers)
        if request.status_code == status_code:
            return request.json()
        else:
            raise Exception(
                "Unexpected status code returned: {}".format(
                    request.status_code)
            )

    def create_ph_text(self):
        """Create slack text with Product Hunt top stories"""
        text_list = [f"Top {STORIES_NUMBER} from Product Hunt:"]
        query = {
            "query": """
            query todayPosts {
                posts {
                    edges {
                        node {
                            name
                            tagline
                            votesCount
                            website
                            url
                        }
                    }
                }
            }
            """
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + PH_API_TOKEN,
        }
        response = self.run_graphql_query(query, headers)
        today_posts = [
            post["node"] for post in response["data"]["posts"]["edges"]]
        top_posts = sorted(
            today_posts, key=lambda k: k["votesCount"], reverse=True)
        # Format slack text
        for post in top_posts[:STORIES_NUMBER]:
            text_list.append(
                "*<{}|{}>* - <{}|{} - {}>".format(
                    post["url"],
                    post["votesCount"],
                    post["website"],
                    post["name"],
                    post["tagline"],
                )
            )
        self.logger.debug(text_list)
        return "\n>".join(text_list)


def post_msg(text):
    """Send message to slack channel"""
    client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    client.chat_postMessage(
        channel=os.environ["SLACK_CHANNEL"],
        text="News",
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": (text)}}],
    )
    return text


@notify_cloudwatch
def lambda_handler(event, context):
    if os.environ["POST_HN"] == "true":
        post_msg(GetHN().create_hn_text())
    if os.environ["POST_PH"] == "true":
        post_msg(GetPH().create_ph_text())
    return "SUCCESS"
