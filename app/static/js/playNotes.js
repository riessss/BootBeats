const samplers = {
  Piano: new Tone.Sampler({ C5: "static/assets/samples/piano_c5.wav" }).toDestination(),
  Drum: new Tone.Sampler({ C5: "static/assets/samples/drum_c5.wav" }).toDestination(),
  Guitar: new Tone.Sampler({ C5: "static/assets/samples/guitar_c5.wav" }).toDestination(),
  Reverse_bass: new Tone.Sampler({ C5: "static/assets/samples/reverse_bass_c5.wav" }).toDestination(),
  Flute: new Tone.Sampler({ C5: "static/assets/samples/flute_c5.wav" }).toDestination(),
  Violin: new Tone.Sampler({ C5: "static/assets/samples/violin_c5.wav" }).toDestination(),
  Hihat: new Tone.Sampler({ C5: "static/assets/samples/hihat_c5.wav" }).toDestination(),
  Sine: new Tone.Sampler({ C5: "static/assets/samples/sine_c5.wav" }).toDestination()
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
  console.log(`Found ${forms.length} forms`);

  forms.forEach((form, formIndex) => {
    const instrument = form.dataset.instrument;
    const textarea = form.querySelector('textarea[name="notes"]');
    console.log(`Form #${formIndex} — instrument: ${instrument}`);

    if (!instrument || !textarea) {
      console.warn(`Skipping form #${formIndex} due to missing instrument or textarea`);
      return;
    }

    const rawText = textarea.value;
    console.log(`Textarea raw input: "${rawText}"`);

    const notes = rawText.split(',').map(n => n.trim()).filter(Boolean);
    console.log(`Parsed notes:`, notes);

    notes.forEach((note, index) => {
      const time = `0:${index}`;
      console.log(`→ Adding: { instrument: "${instrument}", note: "${note}", time: "${time}" }`);
      song.push({ instrument, note, time });
    });
  });

  console.log("Final song array:", song);
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
