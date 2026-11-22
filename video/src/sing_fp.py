"""Stage A (venv with coqui-tts): render each sung line with FastPitch, forcing
per-character durations (so syllables land on the notes) and per-character pitch."""
import json, sys, os, warnings; warnings.filterwarnings('ignore')
import numpy as np, torch
sys.argv = ['x']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hi_tts.py')).read().split("if __name__")[0])
m = s.tts_model; tok = m.tokenizer
FPS = 22050 / 256
MATRA = set('ािीुूृेैोौॅॉ'); VOWEL = set('अआइईउऊऋएऐओऔऑ'); MOD = set('ंँः़्')
OV = {}
_fd = m.format_durations
def fmt(o_dr_log, x_mask):
    pred = (torch.exp(o_dr_log) - 1).squeeze().detach().numpy()
    d = OV['dur_fn'](pred)
    return torch.tensor(d, dtype=torch.float32).view(1, 1, -1)
m.format_durations = fmt
def fpp(o_en, x_mask, pitch=None, dr=None):
    o_pitch = m.pitch_predictor(o_en, x_mask)
    o_pitch = torch.tensor(OV['pitch'], dtype=torch.float32).view_as(o_pitch)
    return m.pitch_emb(o_pitch), o_pitch, None
m._forward_pitch_predictor = fpp

def to_p(hzv):
    return float(np.clip(np.interp(hzv, [168, 215, 271, 304], [0, 1, 2, 3]), 0, 2.9))

plan = json.load(open('plan.json')); KEY = plan['key']
os.makedirs('fp_lines', exist_ok=True); meta = []
for li, L in enumerate(plan['lines']):
    raw = L['text']; text = raw.replace('|', '')
    # syllable -> char indices
    syls = []; i = 0; cur = []
    for ch in raw:
        if ch == '|': syls.append(cur); cur = []; continue
        if ch == ' ': syls.append(cur); cur = []; i += 1; continue
        cur.append(i); i += 1
    syls.append(cur)
    ids = tok.text_to_ids(text); assert len(ids) == len(text), (text, len(ids))
    def stretch_idx(idx):
        cand = [k for k in idx if text[k] in MATRA or text[k] in VOWEL]
        if cand: return cand[-1]
        for j, k in enumerate(idx):
            if text[k] in MOD: continue
            nxt = [q for q in idx[j + 1:] if text[q] != '़']
            if not nxt or text[nxt[0]] != '्': return k
        return idx[0]
    groups = L['groups']
    def dur_fn(pred):
        d = np.zeros(len(text))
        S = []; plans = []
        for si, idx in enumerate(syls):
            v = stretch_idx(idx); on = [k for k in idx if k < v]; co = [k for k in idx if k > v]
            onf = [min(pred[k], 8.0) for k in on]
            while sum(onf) > 14: onf = [x * .9 for x in onf]
            plans.append((v, on, co, onf)); S.append(groups[si][0][1] - sum(onf) / FPS)
        t0 = S[0]; acc = 0; OV['t0'] = t0
        for si, (v, on, co, onf) in enumerate(plans):
            for k, f in zip(on, onf): d[k] = max(1, round(f)); acc += d[k]
            end = S[si + 1] if si + 1 < len(plans) else groups[si][0][1] + sum(n[2] for n in groups[si]) * 0.92
            cof = [max(1, round(min(pred[k], 7.0))) for k in co]
            vf = round((end - t0) * FPS) - acc - sum(cof)
            if vf < 3:
                cof = [1] * len(co); vf = max(3, round((end - t0) * FPS) - acc - len(co))
            d[v] = vf; acc += vf
            for k, f in zip(co, cof): d[k] = f; acc += f
        OV['frames'] = d.sum()
        return d
    pitch = np.zeros(len(text))
    for si, idx in enumerate(syls):
        h = KEY * 2 ** (groups[si][0][0] / 12) / 2
        for k in idx: pitch[k] = to_p(h)
    for k in range(len(text)):
        if text[k] == ' ': pitch[k] = pitch[k - 1] if k else 0
    OV['dur_fn'] = dur_fn; OV['pitch'] = pitch
    w = np.array(s.tts(text, speaker_name='female'), dtype=np.float32)
    fn = f'fp_lines/line{li:02d}.wav'
    import wave
    with wave.open(fn, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(22050)
        wf.writeframes((np.clip(w, -1, 1) * 32767).astype(np.int16).tobytes())
    meta.append({'file': fn, 'groups': groups, 't0': float(OV['t0']), 'frames': float(OV['frames']), 'samples': len(w)})
    print(li, text, len(w) / 22050)
json.dump({'key': KEY, 'lines': meta}, open('fp_meta.json', 'w'), ensure_ascii=False)
