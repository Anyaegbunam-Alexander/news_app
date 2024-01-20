import time
from datetime import datetime, timezone

import feedparser


class BaseParser:
    def __init__(self, url) -> None:
        self.url = url

    def get_entries(self):
        data = feedparser.parse(self.url).entries
        return data

    def get_data(self):
        pass


class CNNParser(BaseParser):
    def get_data(self):
        entries = self.get_entries()
        data = []

        for entry in entries:
            date = entry.get("published")
            media_content = entry.get("media_content")

            if date is None:
                continue

            else:
                data.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "date": date,
                        "image": media_content[0]["url"] if media_content else None,
                    }
                )

        return data


class BBCParser(BaseParser):
    ...


class CNBCParser(BaseParser):
    ...
