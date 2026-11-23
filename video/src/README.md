# One Little Elephant: build steps

All audio and visuals are original. The singing voice is the CC0-licensed
Piper "Kathleen" voice (en-us-kathleen-low, rhasspy/piper release v0.0.2),
retimed and retuned to the melody with the WORLD vocoder.

    pip install numpy scipy pyworld piper-tts
    python3 music.py music_raw.wav                         # band
    python3 vocals.py <path>/en-us-kathleen-low.onnx vocals.wav
    python3 mix.py                                         # -> song_raw.wav
    ffmpeg -i song_raw.wav -af loudnorm=I=-14:TP=-1.5 song.wav
    node render.js video 121.8 video_noaudio.mp4          # needs Playwright
    ffmpeg -i video_noaudio.mp4 -i song.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k out.mp4

## Hindi kid-voice version (ek-nanha-haathi-short.mp4)

Voice: AI4Bharat Indic-TTS Hindi FastPitch + HiFi-GAN, female speaker (MIT
licence; hi.zip from the v1-checkpoints-release on GitHub). Run hi_tts.py in a
venv with `coqui-tts[codec]`, torch, torchaudio and six. Its working directory
must contain voice/hi/hi.

    python3 vocals_hi.py words words.json         # then build jobs.json [[word, wavpath], ...]
    python hi_tts.py jobs.json                     # (venv) speaks every word
    python3 vocals_hi.py sing hiwords vocals_hi.wav
    python3 mix.py vocals_hi.wav && ffmpeg -i song_raw.wav -af loudnorm=I=-14:TP=-1.5 song_hi.wav

### Less robotic vocal (current ek-nanha-haathi-short.mp4)

The song is now in C major (`KEY` in music.py; the English video was rendered
in F). Instead of splicing single words, FastPitch sings each whole line: its
per-character durations and pitch are overridden so syllables land on the
notes. WORLD then only re-tunes the pitch (no time-stretching) into the child
register, keeping the voice's own micro-intonation.

    python3 plan_hi.py                                 # -> plan.json
    python sing_fp.py                                  # (venv, needs ../hi_tts.py and voice/) -> fp_lines/, fp_meta.json
    python3 sing_world.py vocals_fp.wav [formant=1.12]
    python3 music.py music_raw.wav && python3 mix.py vocals_fp.wav

### Natural adult voice (current ek-nanha-haathi-short.mp4)

Song in G (`KEY = 392`); the vocal sings an octave below the lead (G3-G4), close
to the voice's natural pitch. No child/formant effect. Tuning uses Praat PSOLA
(`pip install praat-parselmouth`) instead of WORLD.

    python3 plan_hi.py && python sing_fp.py   # (venv)
    python3 sing_praat.py vocals_nat.wav
    python3 music.py music_raw.wav && python3 mix.py vocals_nat.wav

### Rhythmic recitation (current ek-nanha-haathi-short.mp4)

Forced singing made the Hindi voice sound metallic, so the rhyme is now recited:
the voice speaks each line with its own natural pitch and rhythm (small pitch
lift, speaking rate capped at 1.18x), starting on the line's downbeat. The music
carries the melody. anim.html's SPEECH array times the karaoke sweep to the
spoken lines.

    python3 plan_hi.py && python recite_fp.py      # (venv) -> rec_lines/, rec_meta.json
    # place lines -> vocals_rec.wav (see commit), then:
    python3 music.py music_raw.wav && python3 mix.py vocals_rec.wav

## Ninni Aa Gayi lullaby Short (ninni-aa-gayi-short.mp4)

Audio: "Nini Aa Gayi - Nursery Rhymes for Kids" by dkfilms (Pixabay ID 540557,
downloaded by the channel owner; not stored in this repo). First pass of the
song, 0:00-2:31.5, fading out over the last 2.2 s. Visuals are original
(92.7 BPM sway; captions timed from a Whisper transcription).

    bash build_nini.sh                                   # anim.html helpers + nini_scenes.js -> nini.html
    PAGE=nini.html node render2.js video 151.5 nini_noaudio.mp4
    ffmpeg -i nini_noaudio.mp4 -t 151.5 -i <song.mp3> -map 0:v -map 1:a -c:v copy \
      -af "afade=t=out:st=149.3:d=2.2" -c:a aac -b:a 192k -shortest out.mp4

## Jingle Bells Short (jingle-bells-short.mp4)

Audio: "Jingle Bells" by Sascha Ende (ende.app), CC BY 4.0. Credit is required:
it is shown on the end card and must also go in the YouTube description. Uses
audio 0:15.38-3:00.65 (64 bars after the first chorus downbeat at 20.39 s;
bar = 8 x 0.313 s), with a 0.3 s fade-in and a 2.2 s fade-out.

    bash build_jb.sh                                     # -> jb.html
    PAGE=jb.html node render2.js video 165.266 jb_noaudio.mp4
    ffmpeg -i jb_noaudio.mp4 -ss 15.38 -t 165.266 -i <jingle-bells.mp3> -map 0:v -map 1:a -c:v copy \
      -af "afade=t=in:d=0.3,afade=t=out:st=163.066:d=2.2" -c:a aac -b:a 192k -shortest out.mp4
