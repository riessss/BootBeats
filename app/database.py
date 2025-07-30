from .models import (
    User,
    Song, 
    Instrument, 
    InstrumentLoop, 
    db
)


def instert_intruments():
    if Instrument.query.first() is None:
        piano = Instrument(name="Piano")
        drum = Instrument(name="Drum")
        guitar = Instrument(name="Guitar")
        reverse_bass = Instrument(name="Reverse_bass")
        flute = Instrument(name="Flute")
        violin = Instrument(name="Violin")
        hihat = Instrument(name="Hihat")

        db.session.add(piano)
        db.session.add(drum)
        db.session.add(guitar)
        db.session.add(reverse_bass)
        db.session.add(flute)
        db.session.add(violin)
        db.session.add(hihat)
        db.session.commit()


def insert_default_song(user_id):
    if not Song.query.filter(User.id==user_id).first():
        song = Song(user_id=user_id, title="First", artist="Rapper",tempo=120)
        db.session.add(song)
        db.session.flush()

        piano = Instrument.query.get(1)
        piano_loop = InstrumentLoop(song_id=song.id, instrument=piano, notes=["C5", "B5"])
        
        db.session.add(piano_loop)
        db.session.commit()

