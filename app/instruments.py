from flask import (
    Blueprint,
    send_file
)
import numpy as np
from scipy.io.wavfile import write

bp = Blueprint('instrument', __name__, url_prefix='/instrument')

@bp.route('/sound', methods=["POST"])
def create_sound():
    duration = 2 # seconds
    freq = 440.0 # Note A4
    sample_rate = 44100 # Constant

    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * freq * t)
    audio = np.int16(tone * 32767)

    file = write("sound.wav", sample_rate, audio)

    return send_file("sound.wav", mimetype="audio/wav")