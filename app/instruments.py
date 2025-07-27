from flask import (
    Blueprint,
    send_file
)
import os
import numpy as np
from scipy.io.wavfile import write, read
from database import save_note_to_db 

bp = Blueprint('instrument', __name__, url_prefix='/instrument')

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
        for file in os.listdir(self.sample_folder): #iterate through the files in sample_folder directory (we need to create a sample folder directory)
            if file.endswith(".wav"): #makes sure the files iterated over are wav
                note = file.replace(".wav", "") #turns an A4.wav file into an A4 note for the key in the self.notes dict
                path = os.path.join(self.sample_folder, file) #creates the filepath that will be read scipy.io.wavfile.read
                samplerate, data = read(path) #reads the file, and gives us the samplerate of the file and the data (numpy array of audio samples for the note)
                if samplerate != self.sample_rate: #check for consistency in sample rate
                    raise ValueError(f"Sample rate missmatch in {file}")
                self.notes[note] = data #stores the note:data pairs to self.notes dict


# Modified code to insert note + data into database
    def _play_note(self, note, instrument_loop_id=None, duration=1.0):
        if note not in self.notes:
            print("Note not available")
            return None
        
        note_file_name = self.name + "_" + note + ".wav"
        audio = self.notes[note]
        write(note_file_name, self.sample_rate, audio)

        # Store note in database if instrument_loop_id is provided
        if instrument_loop_id:
            save_note_to_db(pitch=note, start=0.0, duration=duration,
                            instrument_loop_id=instrument_loop_id)

        return send_file(note_file_name, mimetype="audio/wav")
    

    def _play_chord(self, note_list):
        if not self.notes:
            print("no samples loaded for this instrument")
            return
        
        first_note_audio = next(iter(self.notes.values()))
        combined_audio = np.zeros_like(first_note_audio)
        actual_notes_count = 0 #important for normalization
        chord_notes = []
        for n in note_list:
            if n in self.notes:
                current_note_audio = self.notes[n]
                actual_notes_count += 1
                combined_audio += current_note_audio
                chord_notes.append(n)

        if actual_notes_count == 0:
            print("No valid notes found to form a chord")
            return
        
        normalized_tone = combined_audio / actual_notes_count
        normalized_audio = np.int16(normalized_tone * 32767)

        chord_file_name = self.name + "_" + "-".join(chord_notes) + ".wav"
        write(chord_file_name, self.sample_rate, normalized_audio)
        return send_file(chord_file_name, mimetype="audio/wav")
        pass

class Drums():
    def __init__(self, sample_folder):
        self.name = "drums"
        self.sample_folder = sample_folder
        self.elements = {} #dict for notes
        self.sample_rate = 44100 #constant rate
        self._load_samples() #to be defined function to load the sample into the class

    def _load_samples(self):    
        for file in os.listdir(self.sample_folder):
            if file.endswith(".wav"): 
                element = file.replace(".wav", "")
                path = os.path.join(self.sample_folder, file) 
                samplerate, data = read(path) 
                if samplerate != self.sample_rate: 
                    raise ValueError(f"Sample rate missmatch in {file}")
                self.elements[element] = data 

    def _play_element(self, element, instrument_loop_id=None, duration=1.0):
        if element not in self.elements:
            print("Element not available")
            return None
        
        element_file_name = self.name + "_" + element + ".wav"
        audio = self.elements[element]
        write(element_file_name, self.sample_rate, audio)

        # Store note in database if instrument_loop_id is provided
        if instrument_loop_id:
            save_note_to_db(pitch=element, start=0.0, duration=duration,
                            instrument_loop_id=instrument_loop_id)

        return send_file(element_file_name, mimetype="audio/wav")
    
    def _play_beat(self, element_list):
        if not self.elements:
            print("no samples loaded for this instrument")
            return
        
        actual_element_count = 0 #important for normalization
        beat_elements_name = []
        audio_arrays_to_concatenate = []

        for n in element_list:
            if n in self.elements:
                current_element_audio = self.elements[n]
                actual_element_count += 1
                beat_elements_name.append(n)
                audio_arrays_to_concatenate.append(current_element_audio)

        if actual_element_count == 0:
            print("No valid elements found to form a beat")
            return
        
        concatenated_audio = np.concatenate(audio_arrays_to_concatenate)
        normalized_audio = concatenated_audio

        beat_file_name = self.name + "_" + "-".join(beat_elements_name) + ".wav"
        write(beat_file_name, self.sample_rate, normalized_audio)
        return send_file(beat_file_name, mimetype="audio/wav")
        

class Guitar():
    def __init__(self, sample_folder):
        self.name = "guitar"
        self.sample_folder = sample_folder
        self.notes = {} #dict for notes
        self.sample_rate = 44100 #constant rate
        self._load_samples() #to be defined function to load the sample into the class
    
    def _load_samples(self):    
        for file in os.listdir(self.sample_folder): #iterate through the files in sample_folder directory (we need to create a sample folder directory)
            if file.endswith(".wav"): #makes sure the files iterated over are wav
                note = file.replace(".wav", "") #turns an A4.wav file into an A4 note for the key in the self.notes dict
                path = os.path.join(self.sample_folder, file) #creates the filepath that will be read scipy.io.wavfile.read
                samplerate, data = read(path) #reads the file, and gives us the samplerate of the file and the data (numpy array of audio samples for the note)
                if samplerate != self.sample_rate: #check for consistency in sample rate
                    raise ValueError(f"Sample rate missmatch in {file}")
                self.notes[note] = data #stores the note:data pairs to self.notes dict


# Modified code to insert note + data into database
    def _play_note(self, note, instrument_loop_id=None, duration=1.0):
        if note not in self.notes:
            print("Note not available")
            return None
        
        note_file_name = self.name + "_" + note + ".wav"
        audio = self.notes[note]
        write(note_file_name, self.sample_rate, audio)

        # Store note in database if instrument_loop_id is provided
        if instrument_loop_id:
            save_note_to_db(pitch=note, start=0.0, duration=duration,
                            instrument_loop_id=instrument_loop_id)

        return send_file(note_file_name, mimetype="audio/wav")
    

    def _play_chord(self, note_list):
        if not self.notes:
            print("no samples loaded for this instrument")
            return
        
        first_note_audio = next(iter(self.notes.values()))
        combined_audio = np.zeros_like(first_note_audio)
        actual_notes_count = 0 #important for normalization
        chord_notes = []
        for n in note_list:
            if n in self.notes:
                current_note_audio = self.notes[n]
                actual_notes_count += 1
                combined_audio += current_note_audio
                chord_notes.append(n)

        if actual_notes_count == 0:
            print("No valid notes found to form a chord")
            return
        
        normalized_tone = combined_audio / actual_notes_count
        normalized_audio = np.int16(normalized_tone * 32767)

        chord_file_name = self.name + "_" + "-".join(chord_notes) + ".wav"
        write(chord_file_name, self.sample_rate, normalized_audio)
        return send_file(chord_file_name, mimetype="audio/wav")
        
class Violin():
    def __init__(self, sample_folder):
        self.name = "violin"
        self.sample_folder = sample_folder
        self.notes = {} #dict for notes
        self.sample_rate = 44100 #constant rate
        self._load_samples() #to be defined function to load the sample into the class
    
    def _load_samples(self):    
        for file in os.listdir(self.sample_folder): #iterate through the files in sample_folder directory (we need to create a sample folder directory)
            if file.endswith(".wav"): #makes sure the files iterated over are wav
                note = file.replace(".wav", "") #turns an A4.wav file into an A4 note for the key in the self.notes dict
                path = os.path.join(self.sample_folder, file) #creates the filepath that will be read scipy.io.wavfile.read
                samplerate, data = read(path) #reads the file, and gives us the samplerate of the file and the data (numpy array of audio samples for the note)
                if samplerate != self.sample_rate: #check for consistency in sample rate
                    raise ValueError(f"Sample rate missmatch in {file}")
                self.notes[note] = data #stores the note:data pairs to self.notes dict


# Modified code to insert note + data into database
    def _play_note(self, note, instrument_loop_id=None, duration=1.0):
        if note not in self.notes:
            print("Note not available")
            return None
        
        note_file_name = self.name + "_" + note + ".wav"
        audio = self.notes[note]
        write(note_file_name, self.sample_rate, audio)

        # Store note in database if instrument_loop_id is provided
        if instrument_loop_id:
            save_note_to_db(pitch=note, start=0.0, duration=duration,
                            instrument_loop_id=instrument_loop_id)

        return send_file(note_file_name, mimetype="audio/wav")
    

    def _play_chord(self, note_list):
        if not self.notes:
            print("no samples loaded for this instrument")
            return
        
        first_note_audio = next(iter(self.notes.values()))
        combined_audio = np.zeros_like(first_note_audio)
        actual_notes_count = 0 #important for normalization
        chord_notes = []
        for n in note_list:
            if n in self.notes:
                current_note_audio = self.notes[n]
                actual_notes_count += 1
                combined_audio += current_note_audio
                chord_notes.append(n)

        if actual_notes_count == 0:
            print("No valid notes found to form a chord")
            return
        
        normalized_tone = combined_audio / actual_notes_count
        normalized_audio = np.int16(normalized_tone * 32767)

        chord_file_name = self.name + "_" + "-".join(chord_notes) + ".wav"
        write(chord_file_name, self.sample_rate, normalized_audio)
        return send_file(chord_file_name, mimetype="audio/wav")
        
class Reverse_Base():
    def __init__(self, sample_folder):
        self.name = "reverse_base"
        self.sample_folder = sample_folder
        self.notes = {} #dict for notes
        self.sample_rate = 44100 #constant rate
        self._load_samples() #to be defined function to load the sample into the class
    
    def _load_samples(self):    
        for file in os.listdir(self.sample_folder): #iterate through the files in sample_folder directory (we need to create a sample folder directory)
            if file.endswith(".wav"): #makes sure the files iterated over are wav
                note = file.replace(".wav", "") #turns an A4.wav file into an A4 note for the key in the self.notes dict
                path = os.path.join(self.sample_folder, file) #creates the filepath that will be read scipy.io.wavfile.read
                samplerate, data = read(path) #reads the file, and gives us the samplerate of the file and the data (numpy array of audio samples for the note)
                if samplerate != self.sample_rate: #check for consistency in sample rate
                    raise ValueError(f"Sample rate missmatch in {file}")
                self.notes[note] = data #stores the note:data pairs to self.notes dict


# Modified code to insert note + data into database
    def _play_note(self, note, instrument_loop_id=None, duration=1.0):
        if note not in self.notes:
            print("Note not available")
            return None
        
        note_file_name = self.name + "_" + note + ".wav"
        audio = self.notes[note]
        write(note_file_name, self.sample_rate, audio)

        # Store note in database if instrument_loop_id is provided
        if instrument_loop_id:
            save_note_to_db(pitch=note, start=0.0, duration=duration,
                            instrument_loop_id=instrument_loop_id)

        return send_file(note_file_name, mimetype="audio/wav")
    

    def _play_chord(self, note_list):
        if not self.notes:
            print("no samples loaded for this instrument")
            return
        
        first_note_audio = next(iter(self.notes.values()))
        combined_audio = np.zeros_like(first_note_audio)
        actual_notes_count = 0 #important for normalization
        chord_notes = []
        for n in note_list:
            if n in self.notes:
                current_note_audio = self.notes[n]
                actual_notes_count += 1
                combined_audio += current_note_audio
                chord_notes.append(n)

        if actual_notes_count == 0:
            print("No valid notes found to form a chord")
            return
        
        normalized_tone = combined_audio / actual_notes_count
        normalized_audio = np.int16(normalized_tone * 32767)

        chord_file_name = self.name + "_" + "-".join(chord_notes) + ".wav"
        write(chord_file_name, self.sample_rate, normalized_audio)
        return send_file(chord_file_name, mimetype="audio/wav")    
        pass

class Flute():
    def __init__(self, sample_folder):
        self.name = "flute"
        self.sample_folder = sample_folder
        self.notes = {} #dict for notes
        self.sample_rate = 44100 #constant rate
        self._load_samples() #to be defined function to load the sample into the class
    
    def _load_samples(self):    
        for file in os.listdir(self.sample_folder): #iterate through the files in sample_folder directory (we need to create a sample folder directory)
            if file.endswith(".wav"): #makes sure the files iterated over are wav
                note = file.replace(".wav", "") #turns an A4.wav file into an A4 note for the key in the self.notes dict
                path = os.path.join(self.sample_folder, file) #creates the filepath that will be read scipy.io.wavfile.read
                samplerate, data = read(path) #reads the file, and gives us the samplerate of the file and the data (numpy array of audio samples for the note)
                if samplerate != self.sample_rate: #check for consistency in sample rate
                    raise ValueError(f"Sample rate missmatch in {file}")
                self.notes[note] = data #stores the note:data pairs to self.notes dict


# Modified code to insert note + data into database
    def _play_note(self, note, instrument_loop_id=None, duration=1.0):
        if note not in self.notes:
            print("Note not available")
            return None
        
        note_file_name = self.name + "_" + note + ".wav"
        audio = self.notes[note]
        write(note_file_name, self.sample_rate, audio)

        # Store note in database if instrument_loop_id is provided
        if instrument_loop_id:
            save_note_to_db(pitch=note, start=0.0, duration=duration,
                            instrument_loop_id=instrument_loop_id)

        return send_file(note_file_name, mimetype="audio/wav")
    

    def _play_chord(self, note_list):
        if not self.notes:
            print("no samples loaded for this instrument")
            return
        
        first_note_audio = next(iter(self.notes.values()))
        combined_audio = np.zeros_like(first_note_audio)
        actual_notes_count = 0 #important for normalization
        chord_notes = []
        for n in note_list:
            if n in self.notes:
                current_note_audio = self.notes[n]
                actual_notes_count += 1
                combined_audio += current_note_audio
                chord_notes.append(n)

        if actual_notes_count == 0:
            print("No valid notes found to form a chord")
            return
        
        normalized_tone = combined_audio / actual_notes_count
        normalized_audio = np.int16(normalized_tone * 32767)

        chord_file_name = self.name + "_" + "-".join(chord_notes) + ".wav"
        write(chord_file_name, self.sample_rate, normalized_audio)
        return send_file(chord_file_name, mimetype="audio/wav")   