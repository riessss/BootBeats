from .models import (
    Song, 
    Instrument, 
    InstrumentLoop, 
    db
)

# Please correct spelling and check against front end.
def instert_intruments():
    if Instrument.query.first() is None:
        piano = Instrument(name="Piano")
        drum = Instrument(name="Drum")
        guitar = Instrument(name="Guitar")
        reverse_bass = Instrument(name="Bass")
        flute = Instrument(name="Flute")
        violin = Instrument(name="Violon")
        hihat = Instrument(name="Trumpet")
        sine = Instrument(name="Sine")

        db.session.add(piano)
        db.session.add(drum)
        db.session.add(guitar)
        db.session.add(reverse_bass)
        db.session.add(flute)
        db.session.add(violin)
        db.session.add(hihat)
        db.session.add(sine)
        db.session.commit()

# Please correct spelling and check against front end.
def inster_default_song():
    if not Song.query.first():
        song = Song(title="My Dear Fish - Boots", tempo=120)
        db.session.add(song)
        db.session.flush()

        piano = Instrument.query.get(1)
        piano_loop = InstrumentLoop(song_id=song.id, instrument=piano, notes=["C5", "B5"])
        
        db.session.add(piano_loop)
        db.session.commit()

