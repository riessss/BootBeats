from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship,
)
from sqlalchemy import (
    ForeignKey,
    LargeBinary
)
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


# Database used to store all of our wav files as a queryable library.
'''class Sample(db.Model):
    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    note: Mapped[str] = mapped_column()  # example: "C4", "A#3"
    filepath: Mapped[str] = mapped_column()  # .wav file path
    duration: Mapped[float] = mapped_column(default=0.0)  # optional (seconds)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id"))
        # Link to an instrument (each sample belongs to an instrument)
    instrument: Mapped["Instrument"] = relationship(back_populates="samples")'''


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
