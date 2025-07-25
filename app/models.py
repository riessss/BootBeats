from sqlalchemy.orm import (
    Mapped, 
    mapped_column
)

from database import db

class Song(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)