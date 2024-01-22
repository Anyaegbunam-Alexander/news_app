import feedparser
from datetime import datetime
import time

class BaseParser:
    def __init__(self, url) -> None:
        self.url = url

    def get_entries(self):
        data = feedparser.parse(self.url).entries
        return [MediaContent(e) for e in data]

    def get_data(self):
        return self.get_entries()


class MediaContent:
    def __init__(self, entry) -> None:
        self.entry = entry

    def __getattr__(self, attr):
        return getattr(self.entry, attr, None)

    @property
    def image_url(self):
        media_content = self.entry.get("media_content")
        return media_content[0]["url"] if media_content else "/placeholder.jpg"

    @property
    def readable_date(self):
        published_parsed = self.entry.get("published_parsed")
        if not published_parsed:
            return None

        published_time = datetime.fromtimestamp(time.mktime(published_parsed))
        time_diff = datetime.now() - published_time

        if time_diff.days > 0:
            return time.strftime("%a, %b %d %Y - %I:%M %p", published_parsed)
        elif time_diff.seconds // 3600 > 0:
            return f"{time_diff.seconds // 3600}h {time_diff.seconds % 3600 // 60}m ago"
        else:
            return f"{time_diff.seconds // 60}m ago"

