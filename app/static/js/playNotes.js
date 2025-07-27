const samplers = {
  Piano: new Tone.Sampler({ C5: "static/assets/samples/piano_c5.wav" }).toDestination(),
  Drum: new Tone.Sampler({ C5: "static/assets/samples/drum_c5.wav" }).toDestination(),
  Guitar: new Tone.Sampler({ C5: "static/assets/samples/guitar_c5.wav" }).toDestination(),
  Reverse_bass: new Tone.Sampler({ C5: "static/assets/samples/reverse_bass_c5.wav" }).toDestination(),
  Flute: new Tone.Sampler({ C5: "static/assets/samples/flute_c5.wav" }).toDestination(),
  Violin: new Tone.Sampler({ C5: "static/assets/samples/violin_c5.wav" }).toDestination(),
  Hihat: new Tone.Sampler({ C5: "static/assets/samples/hihat_c5.wav" }).toDestination(),
};

function buildSongFromForms() {
  const song = [];
  const forms = document.querySelectorAll('form[data-instrument]');

  forms.forEach((form, formIndex) => {
    const instrument = form.dataset.instrument;
    const textarea = form.querySelector('textarea[name="notes"]');

    if (!instrument || !textarea) {
      console.warn(`Skipping form #${formIndex} due to missing instrument or textarea`);
      return;
    }

    const rawText = textarea.value;

    const notes = rawText.split(',').map(n => n.trim()).filter(Boolean);

    notes.forEach((note, index) => {
      const time = `0:${index}`;
      song.push({ instrument, note, time });
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
  startSlider(duration);
});
