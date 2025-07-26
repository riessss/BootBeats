from flask import send_file
import numpy as np
from scipy.io.wavfile import write


def create_sound():
    duration = 2 # seconds
    freq = 440.0 # Note A4
    sample_rate = 44100 # Constant

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    audio = np.int16(tone * 32767)

    file = write("sound.wav", sample_rate, audio)

    return send_file("sound.wav", mimetype="audio/wav")

class Piano():
    def __init__(self, sample_folder):
        self.name = "piano"
        self.sample_folder = sample_folder
        self.notes = {} #dict for notes
        self.sample_rate = 44100 #constant rate
        self._load_samples() #to be defined function to load the sample into the class
    
    def _load_samples(self):    
        pass
    
    def _play_note(self, note):
        if note not in self.notes:
            print("Note not available")
        freq = self.notes[note]
        duration = 2
        note_file = self.name + "_" + note + ".wav"

        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = 0.5 * np.sin(2 * np.pi * freq * t)
        audio = np.int16(tone * 32767)
        file = write(note_file, self.sample_rate, audio)
        return send_file(note_file, mimetype="audio/wav")