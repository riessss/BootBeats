from .models import (
    Song, 
    Instrument, 
    InstrumentLoop, 
    db
)

# Please correct spelling and check against front end.
def instert_intruments():
    if Instrument.query.first() is None:
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            piano = Instrument(name="Piano", wav=f.read())
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            drum = Instrument(name="Drum", wav=f.read())
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            guitar = Instrument(name="Guitar", wav=f.read())
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            reverse_bass = Instrument(name="Bass", wav=f.read())
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            flute = Instrument(name="Flute", wav=f.read())
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            violin = Instrument(name="Violon", wav=f.read())
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            hihat = Instrument(name="Trumpet", wav=f.read())
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            sine = Instrument(name="Sine", wav=f.read())
        with open("app/static/assets/samples/piano_c5.wav", "rb") as f:
            snare = Instrument(name="Snare", wav=f.read())

        db.session.add(piano)
        db.session.add(drum)
        db.session.add(guitar)
        db.session.add(reverse_bass)
        db.session.add(flute)
        db.session.add(violin)
        db.session.add(hihat)
        db.session.add(sine)
        db.session.add(snare)
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

