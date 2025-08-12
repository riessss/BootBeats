const DURATION = {
    MIN: 60000,
    SEC: 1000
}
const samplers = {
    Piano: new Tone.Sampler({ C5: "static/assets/samples/piano_c5.wav" }).toDestination(),
    Drum: new Tone.Sampler({ C5: "static/assets/samples/drum_c5.wav" }).toDestination(),
    Guitar: new Tone.Sampler({ C5: "static/assets/samples/guitar_c5.wav" }).toDestination(),
    Reverse_bass: new Tone.Sampler({ C5: "static/assets/samples/reverse_bass_c5.wav" }).toDestination(),
    Flute: new Tone.Sampler({ C5: "static/assets/samples/flute_c5.wav" }).toDestination(),
    Violin: new Tone.Sampler({ C5: "static/assets/samples/violin_c5.wav" }).toDestination(),
    Hihat: new Tone.Sampler({ C5: "static/assets/samples/hihat_c5.wav" }).toDestination(),
};

let isPlaying = false;
let totalTime;
let closeTime;
let timerLoop;
let songsPool = [];

async function handleAudioNotes(event) {
    isPlaying = !isPlaying;
    if (isPlaying) {
        await Tone.start();
        handleAudioTimer();
        Tone.Transport.start();
        // event.target.innerText = "Start";
    } else {
        Tone.Transport.pause();
        removeAudioTimer();
        // event.target.innerText = "Pause";
    }
}

function renderAudioNotes(songs) {
    songs.forEach((song) => {
        const { instrument, note, time } = song;
        Tone.Transport.schedule((time) => {
            samplers[instrument].triggerAttack(note, time);
        }, time);
    });
}

function handleAudioTimer() {
    removeAudioTimer(timerLoop);
    timerLoop = setInterval(() => {
        if (closeTime <= 0) { 
            isPlaying = !isPlaying;
            closeTime = totalTime;
            Tone.Transport.stop();
            handleAudioRange(closeTime);
            removeAudioTimer(timerLoop);
        } else {
            closeTime = closeTime - 1000;
            handleAudioRange(closeTime);
        }
    }, 1000);
}

function removeAudioTimer(param) {
    clearInterval(param);
}

function handleAudioRange(param) {
    const goingTime = totalTime - closeTime;

    $rangePipe.value = goingTime;
    $startTime.innerText = getNotesDuration(
        goingTime
    );
    $closeTime.innerText = getNotesDuration(
        totalTime
    );
}

function renderAudioRange(param) {
    $rangePipe.max = totalTime;
}

function formatAudioNotes(param) {
    const notes = [];
    const {
        instrument,
        notesInput
    } = param;

    if (!instrument) {
        console.log("");
        return [];
    }
    if (!notesInput) {
        console.log("");
        return [];
    }

    notesInput.split(",").forEach((note, indx) => {
        const time = `0:${indx.toString().padStart(2, "0")}`;
        const text = note.trim();
        notes.push({ instrument, note: text, time });
    });
    return notes;
}

function getNotesFromForm(event) {
    const forms = document.querySelectorAll(
        "form[data-instrument]"
    );

    forms.forEach((form) => {
        const instrument = form.dataset.instrument;
        const notesInput = form.notes.value.trim();

        songsPool = [...songsPool, ...formatAudioNotes({
            instrument,
            notesInput
        })];
    });

    setNotesDuration(
        songsPool
    );
    renderAudioNotes(
        songsPool
    );
    renderAudioRange();
    handleAudioRange();
}

function setNotesFromForm(event) {
    const instrument = event.currentTarget.dataset.instrument;
    const notesInput = event.currentTarget.notes.value.trim();

    const songsStale = songsPool.filter((song) => (
        song.instrument !== instrument
    ));
    const songsFresh = formatAudioNotes({
        instrument,
        notesInput
    });

    songsPool = [...songsFresh, ...songsStale];
    
    setNotesDuration(
        songsPool
    );
    renderAudioNotes(
        songsPool
    );
    renderAudioRange();
    handleAudioRange();
}

function getNotesDuration(value) {
    const min = `${Math.floor(value / DURATION.MIN)}`;
    const sec = `${Math.floor(value / DURATION.SEC)}`;

    return `${min}:${sec.padStart(2, "0")}`;
}

function setNotesDuration(songs) {
    const duration = songs.reduce((acc, val) => {
        const arr = val.time.split(":");
        const min = parseInt(arr[0]);
        const sec = parseInt(arr[1]);

        const amt = (min * DURATION.MIN) + (sec * DURATION.SEC);
        return amt > acc ? amt : acc;
    }, 0);

    totalTime = duration;
    closeTime = duration;
}

document.getElementById("playBtn")
.addEventListener(
    "click",
    (e) => handleAudioNotes(e)
);

window.document
.addEventListener(
    "DOMContentLoaded",
    (e) => getNotesFromForm(e)
);


document.querySelectorAll(
    "form[data-instrument]"
).forEach(form => {
    form.addEventListener(
        "change",
        (e) => setNotesFromForm(e)
    );
});



// function buildSongFromForms() {
//     const song = [];
//     const forms = document.querySelectorAll('form[data-instrument]');

//     forms.forEach((form, formIndex) => {
//         const instrument = form.dataset.instrument;
//         const textarea = form.querySelector('textarea[name="notes"]');

//         if (!instrument || !textarea) {
//             console.warn(`Skipping form #${formIndex} due to missing instrument or textarea`);
//             return;
//         }

//         const rawText = textarea.value;

//         const notes = rawText.split(',').map(n => n.trim()).filter(Boolean);
//         notes.forEach((note, index) => {
//             const time = `0:${index}`;
//             song.push({ instrument, note, time });
//         });
//     });

//     return song;
// }

// function scheduleSong(song) {
//     song.forEach(({ instrument, note, time }) => {
//         Tone.Transport.schedule(time => {
//             samplers[instrument].triggerAttack(note, time);
//         }, time);
//     });
// }

// document.getElementById("playBtn")
//     .addEventListener("click", async () => {
//         await Tone.start();
//         Tone.Transport.stop();
//         Tone.Transport.cancel();

//         const song = buildSongFromForms()
//         scheduleSong(song);
//         Tone.Transport.start()
        // startSlider(duration);
// });
