from .models import (
    Song, 
    Instrument, 
    InstrumentLoop, 
    Note,
    db
)

# Please correct spelling and check against front end.
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

# Please correct spelling and check against front end.
def inster_default_song():
    if not Song.query.first():
        song = Song(title="My Dear Fish - Boots", tempo=120)
        db.session.add(song)
        db.session.flush()

        piano = Instrument.query.get(1)
        piano_loop = InstrumentLoop(song_id=song.id, instrument=piano)
        
        db.session.add(piano_loop)
        db.session.commit()

# Function to save notes & meta data to the database from each instrument input in instruments.py
def save_note_to_db(pitch, start, duration, instrument_loop_id):
    loop = db.session.get(InstrumentLoop, instrument_loop_id)
    if not loop:
        raise ValueError(f"InstrumentLoop {instrument_loop_id} does not exist")

    new_note = Note(
        pitch=pitch,
        start=start,
        duration=duration,
        instrument_loop_id=instrument_loop_id
    )
    db.session.add(new_note)
    db.session.commit()
    return new_note.id
