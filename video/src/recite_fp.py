"""Rhythmic recitation (venv): the Hindi voice speaks each line naturally (its own
pitch and rhythm); only the overall speaking rate is set so a line fits its 2 bars."""
import json, sys, os, wave, warnings; warnings.filterwarnings('ignore')
import numpy as np, torch
sys.argv = ['x']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hi_tts.py')).read().split("if __name__")[0])
m = s.tts_model
LIFT = 0.35   # gentle, cheerful lift of the predicted pitch (keeps the natural contour)
def fpp(o_en, x_mask, pitch=None, dr=None):
    o_pitch = m.pitch_predictor(o_en, x_mask) + LIFT
    return m.pitch_emb(o_pitch), o_pitch, None
m._forward_pitch_predictor = fpp
BAR = 4 * 0.4285
def say(text, ls):
    m.length_scale = ls
    w = np.array(s.tts(text, speaker_name='female'), dtype=np.float32)
    e = np.convolve(np.abs(w), np.ones(220) / 220, 'same'); nz = np.where(e > e.max() * 0.04)[0]
    return w[max(0, nz[0] - 200): nz[-1] + 1500]
plan = json.load(open('plan.json'))
ENDS = {3: '!', 19: '…', 21: '!', 22: '!'}
os.makedirs('rec_lines', exist_ok=True); meta = []
for li, L in enumerate(plan['lines']):
    text = L['text'].replace('|', '')
    text = text + ENDS.get(li, '!' if li % 4 == 3 else '')
    start = L['groups'][0][0][1]
    slot = (2 * BAR) * (1.25 if li == 22 else 1.0)
    w = say(text, 1.0); D = len(w) / 22050
    ls = float(np.clip(slot * 0.78 / D, 0.9, 1.18))
    if abs(ls - 1) > 0.02: w = say(text, ls)
    fn = f'rec_lines/l{li:02d}.wav'
    with wave.open(fn, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(22050)
        wf.writeframes((np.clip(w, -1, 1) * 32767).astype(np.int16).tobytes())
    meta.append({'file': fn, 't0': start - 0.06, 'dur': len(w) / 22050, 'ls': ls})
    print(li, text, round(D, 2), '->', round(len(w) / 22050, 2), 'ls', round(ls, 2))
json.dump(meta, open('rec_meta.json', 'w'))
