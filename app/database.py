from .models import (
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
        bass = Instrument(name="Bass")
        flute = Instrument(name="Flute")
        violin = Instrument(name="Violon")
        trumpet = Instrument(name="Trumpet")
        db.session.add(piano)
        db.session.add(drum)
        db.session.add(guitar)
        db.session.add(bass)
        db.session.add(flute)
        db.session.add(violin)
        db.session.add(trumpet)
        db.session.commit()

def inster_default_song():
    if not Song.query.first():
        song = Song(title="Your Song", tempo=120)
        db.session.add(song)
        db.session.flush()

        piano = Instrument.query.get(1)
        piano_loop = InstrumentLoop(song_id=song.id, instrument=piano)
        
        db.session.add(piano_loop)
        db.session.commit()
