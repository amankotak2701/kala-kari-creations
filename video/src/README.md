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
