from re import S
from sqlalchemy import insert, select

from models import Source, Topic, session


class Query:
    def __init__(self):
        self.session = session

    def get_sources(self):
        stmt = select(Source)
        res = self.session.execute(stmt)
        return res.scalars()

    def get_one_source(self, id):
        stmt = select(Source).where(Source.id == id).join(Source.topics)
        res = self.session.execute(stmt)
        return res.scalar()

    def get_topics(self, id):
        stmt = select(Topic).where(Topic.source_id == id)
        res = self.session.execute(stmt)
        return res.scalars()

    def get_one_topic(self, id, name):
        stmt = select(Topic).where(Topic.source_id == id, Topic.name == name)
        res = self.session.execute(stmt)
        return res.scalar()

    def search_source_by_name(self, value):
        stmt = select(Source).where(Source.name.like(f"%{value}%"))
        res = self.session.execute(stmt)
        return res.scalars()

    def add_source(self, data: dict):
        topics = data.pop("topics")
        source = self.session.scalar(insert(Source).values(**data).returning(Source))
        for topic in topics:
            topic["source_id"] = source.id
        
        self.session.execute(insert(Topic), topics)
        self.session.commit()
        return source
