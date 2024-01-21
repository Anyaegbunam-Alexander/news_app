from sqlalchemy import select

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
