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
from sqlalchemy import String

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash 

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(20))
    email: Mapped[str] = mapped_column(
        String(40))
    password_hash: Mapped[str] = mapped_column(
        String(256))
    
    songs: Mapped[list["Song"]] = relationship(
        "Song", back_populates="user")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)





class Song(db.Model):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(
        unique=True)
    artist: Mapped[str] = mapped_column(
        unique=True)
    tempo: Mapped[int] = mapped_column(default=120)

    instrument_loops: Mapped[list["InstrumentLoop"]] = relationship(
        back_populates="song")
    user: Mapped['User'] = relationship(
        "User", back_populates='songs')


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

