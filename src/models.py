from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

engine = create_engine("sqlite:///sources.db", echo=True)
session = Session(engine)

class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "source"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    source_url: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(Text)
    default_ext: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    extensions: Mapped[List["Extension"]] = relationship(
        back_populates="source", cascade="all, delete-orphan"
    )


class Extension(Base):
    __tablename__ = "extension"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(Text)
    source_id: Mapped[int] = mapped_column(ForeignKey("source.id"))
    source: Mapped["Source"] = relationship(back_populates="extensions")
