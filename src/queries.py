from sqlalchemy import delete, insert, select, update

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
        self.add_topics_to_source(topics, source.id)
        return source
    
    def add_topics_to_source(self, data: list[dict], source_id: int):
        if not data:
            return
        
        for topic in data:
            topic["source_id"] = source_id

        self.session.execute(insert(Topic), data)
        return source_id
    
    def update_source(self, data: dict, id):
        stmt = update(Source).where(Source.id == id).values(data)
        self.session.execute(stmt)

    def update_topics(self, data: list[dict], source_id: int):
        for topic in data:
            topic["source_id"] = source_id
        self.session.execute(update(Topic), data)

    def update_source_and_topics(self, data:dict, source_id: int):
        new_topics = data.pop("new_topics")
        existing_topics = data.pop("existing_topics")
        self.update_source(data, source_id)
        self.update_topics(existing_topics, source_id)
        self.add_topics_to_source(new_topics, source_id)

    def delete_topic(self, id):
        stmt = delete(Topic).where(Topic.id == id)
        self.session.execute(stmt)
        return True

    def delete_source(self, id):
        stmt = delete(Source).where(Source.id == id)
        self.session.execute(stmt)
        return True

    def rollback(self):
        self.session.rollback()
        return True

    def save(self):
        self.session.commit()
        return True
