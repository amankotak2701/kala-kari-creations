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

## We Wish You A Merry Christmas Short (we-wish-you-a-merry-christmas-short.mp4)

Audio: "We Wish You A Merry Christmas" (vocal) by Jingle Punks, from the
channel owner's file (not stored here). First full pass of the song, 0:00-2:22,
with a 1.7 s fade at the natural ending. The song is in 3/4: bar 1.405 s, verses
of 16 bars starting at 6.04 s.

    bash build_fam.sh                                    # -> family.html
    PAGE=family.html node render2.js video 142 fam_noaudio.mp4
    ffmpeg -i fam_noaudio.mp4 -t 142 -i <song audio> -map 0:v -map 1:a -c:v copy \
      -af "afade=t=out:st=140.3:d=1.7" -c:a aac -b:a 192k -shortest out.mp4

## O Christmas Tree Short (o-christmas-tree-short.mp4)

Audio: "O Christmas Tree" (vocal) by Jingle Punks, from the channel owner's file
(not stored here), used in full (2:43). 3/4 at 93 BPM: bar 1.935 s, lines of
2 bars, verses of 8 lines starting at 29.91 s. Lyrics are the traditional
public-domain English text.

    bash build_oct.sh                                    # -> octree.html
    PAGE=octree.html node render2.js video 163.4 oct_noaudio.mp4
    ffmpeg -i oct_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## Mary Had A Little Lamb, Christmas edition (mary-had-a-little-lamb-christmas-short.mp4)

Audio: "Mary Had A Little Lamb" (vocal) by The Green Orbs, YouTube Audio
Library, from the channel owner's file (not stored here), 0:00-2:16 (the
singing ends at 2:10). 4/4 at 85 BPM: bar 2.824 s, one lyric line per bar,
verses of 8 bars + 2-bar interlude starting at 5.92 s. Lyrics are the
public-domain 1830 text.

    bash build_mary.sh                                   # -> mary.html
    PAGE=mary.html node render2.js video 136 mary_noaudio.mp4
    ffmpeg -i mary_noaudio.mp4 -t 136 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## The Wheels On The Bus (wheels-on-the-bus-short.mp4)

Audio: "Wheels On The Bus" from the channel owner's file (not stored here), used
in full (2:04) and padded with silence to 2:08 for the end card. 4/4, bar
1.52 s; verses of 8 bars start at 12.2, 36.5, 73.0 and 109.5 s. Lyrics are the
traditional public-domain text.

    bash build_bus.sh                                    # -> bus.html
    PAGE=bus.html node render2.js video 128 bus_noaudio.mp4
    ffmpeg -i bus_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -af apad=whole_dur=128 -c:a aac -b:a 192k -t 128 out.mp4

## Old MacDonald Had A Farm (old-macdonald-had-a-farm-short.mp4)

Audio: "Old MacDonald Had A Farm" from the channel owner's file (not stored here),
used in full (2:20) and padded with silence to 2:24 for the end card. Lines are
2 bars (2.6085 s); verses of 8 lines + 2-line interlude start at 7.55 s; the
closing tag starts at 132.8 s. Lyrics are the traditional public-domain text.

    bash build_farm.sh                                   # -> farm.html
    PAGE=farm.html node render2.js video 144 farm_noaudio.mp4
    ffmpeg -i farm_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -af apad=whole_dur=144 -c:a aac -b:a 192k -t 144 out.mp4

## Hickory Dickory Dock (hickory-dickory-dock-short.mp4)

Audio: "Hickory Dickory Dock" from the channel owner's file (not stored here), used
in full (2:08.5). Animal version: mouse (one), bird (two), dog (three), bear
(four), bee (five), hen (six), then a closing "tick tock" outro. One lyric line
= 1 bar (2.125 s); verses start at 4.5 s every 18.06 s; outro at 112.9 s.

    bash build_hdd.sh                                    # -> hdd.html
    PAGE=hdd.html node render2.js video 128.5 hdd_noaudio.mp4
    ffmpeg -i hdd_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## Humpty Dumpty (humpty-dumpty-short.mp4)

Audio: "Humpty Dumpty Sat On A Wall" from the channel owner's file (not stored
here), used in full (2:16.6). Lyric lines are 2 bars (3.43 s); full verses start
at 18.4, 47.6 and 90.0 s; single lines at 119.6 and 126.4 s. The instrumental
breaks carry a happy-ending story: the kids bandage Humpty, then add a helmet
and a pillow so the third fall ends in a bounce.

    bash build_hum.sh                                    # -> hum.html
    PAGE=hum.html node render2.js video 136.6 hum_noaudio.mp4
    ffmpeg -i hum_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## Twinkle Twinkle Little Star (twinkle-twinkle-little-star-short.mp4)

Audio: "Twinkle Twinkle Little Star" from the channel owner's file (not stored
here), used in full (2:18). One lyric line every 6.0 s; verses start at 11.9,
53.9 and 95.9 s (the third repeats verse 1). Lyrics are the public-domain text.

    bash build_tw.sh                                     # -> tw.html
    PAGE=tw.html node render2.js video 138 tw_noaudio.mp4
    ffmpeg -i tw_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## Itsy Bitsy Spider (itsy-bitsy-spider-short.mp4)

Audio: "Itsy Bitsy Spider" from the channel owner's file (not stored here), used
in full (2:08). Lines every 4.8 s; verses start at 19.3, 57.7 and 96.1 s.
Lyrics are the traditional public-domain text. The breaks show Itsy spinning a
web, trying an umbrella and finally reaching the top with her bug friends.

    bash build_sp.sh                                     # -> sp.html
    PAGE=sp.html node render2.js video 128 sp_noaudio.mp4
    ffmpeg -i sp_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## Are You Sleeping, Brother John? (are-you-sleeping-brother-john-short.mp4)

Audio: "Are You Sleeping Brother John" from the channel owner's file (not stored
here), used in full (2:03.8). Lines every 4.13 s from 16.0 s; sung verses start
at line 0, 8, 16 and 20 (plus a closing "ding dong" line at 24). Lyrics are the
traditional public-domain English text.

    bash build_bj.sh                                     # -> bj.html
    PAGE=bj.html node render2.js video 123.8 bj_noaudio.mp4
    ffmpeg -i bj_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## Hush Little Baby (hush-little-baby-short.mp4)

Audio: "Hush Little Baby" from the channel owner's file (not stored here), used in
full (2:33). Couplets are 2 lines x 4.21 s on a grid from 8.0 s; sung couplet
slots are 0, 1, 3, 4, 6, 7, 10 and 11, with a "la la" outro at 143.5 s.
Lyrics are the traditional public-domain text.

    bash build_hb.sh                                     # -> hb.html
    PAGE=hb.html node render2.js video 153 hb_noaudio.mp4
    ffmpeg -i hb_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## The Muffin Man (the-muffin-man-short.mp4)

Audio: "The Muffin Man" from the channel owner's file (not stored here), used in
full (1:48). Lines every 2.667 s; the question-and-answer verse (8 lines) starts
at 10.0, 42.0 and 74.0 s. Lyrics are the traditional public-domain text.

    bash build_mm.sh                                     # -> mm.html
    PAGE=mm.html node render2.js video 108.1 mm_noaudio.mp4
    ffmpeg -i mm_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## London Bridge Is Falling Down (london-bridge-is-falling-down-short.mp4)

Audio: "London Bridge Is Falling Down" from the channel owner's file (not stored
here), used in full (2:14). Lines every 2.727 s; verses come in pairs (two
4-line verses + a 4-line break) starting at 10.2 s. Lyrics are the traditional
public-domain text. River scenes use a 1.6x camera zoom.

    bash build_lb.sh                                     # -> lb.html
    PAGE=lb.html node render2.js video 134.1 lb_noaudio.mp4
    ffmpeg -i lb_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4

## A Tisket, A Tasket (a-tisket-a-tasket-short.mp4)

Audio: "A Tisket A Tasket" from the channel owner's file (not stored here), used in
full (2:43.5). Lines every 2.4 s; verses (8 lines) start at 9.8, 38.6 and 81.8 s;
the instrumental ending runs from about 101 s. Lyrics are the traditional
public-domain text. All park scenes use a 1.35x camera zoom.

    bash build_tt.sh                                     # -> tt.html
    PAGE=tt.html node render2.js video 163.5 tt_noaudio.mp4
    ffmpeg -i tt_noaudio.mp4 -i <song audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4
