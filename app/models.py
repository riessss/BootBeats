from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship,
)
from sqlalchemy import (
    ForeignKey,
    JSON
)
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Song(db.Model):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(
        unique=True)
    tempo: Mapped[int] = mapped_column(default=120)
    instrument_loops: Mapped[list["InstrumentLoop"]] = relationship(
        back_populates="song")


class InstrumentLoop(db.Model):
    __tablename__ = "instrument_loops"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    song_id: Mapped[int] = mapped_column(
        ForeignKey("songs.id"))
    instrument_id: Mapped[int] = mapped_column(
        ForeignKey("instruments.id"))
    notes: Mapped[list[str]] = mapped_column(JSON)

    instrument: Mapped["Instrument"] = relationship(
        back_populates="instrument_loops")
    song: Mapped["Song"] = relationship(
        back_populates="instrument_loops")


class Instrument(db.Model):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        unique=True)
    
    instrument_loops: Mapped[list["InstrumentLoop"]] = relationship(
        back_populates="instrument")

