"""Builds the sung-line plan (text, syllables, notes with times) -> plan.json"""
import json
from lyrics_hi import verse, FINALE, TAG, SPLIT
ns = {}
exec(open('music.py').read().split("if __name__ != '__main__'")[0], ns)
VERSE, bt, BEAT = ns['VERSE'], ns['bt'], ns['BEAT']
def notes_for(bar0, ml):
    out = []
    for b, li in enumerate((2 * ml, 2 * ml + 1)):
        beat = 0
        for semi, d in VERSE[li]:
            if semi is not None: out.append([semi, bt(bar0 + b, beat), d * BEAT])
            beat += d
    return out
plan = []
def add(text, notes, split):
    syl = [s for w in text.split(' ') for s in w.split('|')]
    assert len(syl) == len(split) and sum(split) == len(notes), (text, len(syl), len(split), len(notes))
    groups = []; k = 0
    for c in split: groups.append(notes[k:k + c]); k += c
    plan.append({'text': text, 'groups': groups})
for v, b0 in enumerate([6, 14, 24, 34, 42]):
    for li, line in enumerate(verse(v + 1)):
        add(line, notes_for(b0 + 2 * li, li), SPLIT[li])
for b0, ml, line in FINALE:
    add(line, notes_for(b0, ml), SPLIT[ml])
TAGM = [[(9, 1), (11, 1), (12, 1), (14, 1)], [(16, 1), (14, .5), (12, .5), (12, 2)]]
tn = []
for b, l in enumerate(TAGM):
    beat = 0
    for semi, d in l:
        tn.append([semi, bt(56 + b, beat), d * BEAT * (1.4 if (b, beat) == (1, 2) else 1)]); beat += d
add(TAG, tn, [1] * 8)
json.dump({'key': ns['KEY'], 'lines': plan}, open('plan.json', 'w'), ensure_ascii=False, indent=0)
print(len(plan), 'lines')
