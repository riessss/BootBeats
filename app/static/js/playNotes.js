const samplers = {
  piano: new Tone.Sampler({ C5: "static/assets/samples/piano_c5.wav" }).toDestination(),
  drum: new Tone.Sampler({ C5: "static/assets/samples/drum_c5.wav" }).toDestination(),
  guitar: new Tone.Sampler({ C5: "static/assets/samples/guitar_c5.wav" }).toDestination(),
  reverse_bass: new Tone.Sampler({ C5: "static/assets/samples/reverse_bass_c5.wav" }).toDestination(),
  flute: new Tone.Sampler({ C5: "static/assets/samples/flute_c5.wav" }).toDestination(),
  violin: new Tone.Sampler({ C5: "static/assets/samples/violin_c5.wav" }).toDestination(),
  hihat: new Tone.Sampler({ C5: "static/assets/samples/hihat_c5.wav" }).toDestination(),
  sine: new Tone.Sampler({ C5: "static/assets/samples/sine_c5.wav" }).toDestination()
};

const song = [
  { instrument: "piano", note: "C4", time: "0:0" },
  { instrument: "piano", note: "E4", time: "0:1" },
  { instrument: "piano", note: "G4", time: "0:2" },
  { instrument: "drum", note: "C5", time: "0:0" },
  { instrument: "drum", note: "C4", time: "0:2" }
];

function buildSongFromForms() {
  const song = [];
  const forms = document.querySelectorAll('form[data-instrument]');

  forms.forEach(form => {
    const instrument = form.dataset.instrument;
    const textarea = form.querySelector('textarea[name="notes"]');
    if (!instrument || !textarea) return;

    const notes = textarea.value.split(',').map(n => n.trim()).filter(Boolean);

    notes.forEach((note, index) => {
      song.push({
        instrument,
        note,
        time: '0:0:0'
      });
    });
  });

  return song;
}


function scheduleSong(song) {
  song.forEach(({ instrument, note, time }) => {
    Tone.Transport.schedule(time => {
      samplers[instrument].triggerAttack(note, time);
    }, time);
  });
}

document.getElementById("playBtn").addEventListener("click", async () => {
  await Tone.start();
  Tone.Transport.stop();
  Tone.Transport.cancel();

  const song = buildSongFromForms()
  scheduleSong(song);
  Tone.Transport.start()
});
