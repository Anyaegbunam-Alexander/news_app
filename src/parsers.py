import feedparser


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
        return media_content[0]["url"] if media_content else "/placeholder.png"
