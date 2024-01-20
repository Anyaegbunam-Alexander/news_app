from sqlalchemy import select

from models import Extension, Source, session


class Query:
    def __init__(self) -> None:
        self.session = session

    def get_sources(self):
        stmt = select(Source)
        res = self.session.execute(stmt)
        return res.scalars()

    def get_one_source(self, id):
        stmt = select(Source).where(Source.id == id).join(Source.extensions)
        res = self.session.execute(stmt)
        return res.scalar()

    def get_source_extensions(self, id):
        stmt = select(Extension).where(Extension.source_id == id)
        res = self.session.execute(stmt)
        return res.scalars()

    def get_one_source_extension(self, id, name):
        stmt = select(Extension).where(Extension.source_id == id, Extension.name == name)
        res = self.session.execute(stmt)
        return res.scalar()
