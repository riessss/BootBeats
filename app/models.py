from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship,
)
from sqlalchemy import (
    ForeignKey,
    LargeBinary
)

from .database import db


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

    instrument: Mapped["Instrument"] = relationship(
        back_populates="instrument_loops")
    notes: Mapped[list["Note"]] = relationship(
        back_populates="instrument_loop")
    song: Mapped["Song"] = relationship(
        back_populates="instrument_loops")


class Instrument(db.Model):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        unique=True)
    '''wav: Mapped[bytes] = mapped_column(
        LargeBinary)'''
    
    instrument_loops: Mapped[list["InstrumentLoop"]] = relationship(
        back_populates="instrument")

# TODO: Notes need to be optional in instrument loop

class Note(db.Model):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    pitch: Mapped[str]
    start: Mapped[float]
    duration: Mapped[float] # In seconds

    instrument_loop_id: Mapped[int] = mapped_column(
        ForeignKey("instrument_loops.id"))
    instrument_loop: Mapped["InstrumentLoop"] = relationship(
        back_populates="notes")