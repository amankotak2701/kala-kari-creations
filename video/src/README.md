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
