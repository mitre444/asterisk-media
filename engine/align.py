"""Tiempos reales por palabra: un reconocedor de voz local (Parakeet TDT v3) escucha la narracion
y devuelve cuando empieza cada palabra. Sirve para dos cosas: sincronizar los subtitulos y comprobar
que la voz dijo lo que dice el guion.
"""
import difflib
import os
import re
import unicodedata
import numpy as np

D = "/home/claude/models/asr_parakeet_v3/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
OFFSET = -0.03      # el reconocedor marca un pelo tarde; se adelanta para que el resaltado no llegue despues de la voz
_rec = None


def available():
    return os.path.exists(D + "/encoder.int8.onnx")


def recognizer():
    global _rec
    if _rec is None:
        import sherpa_onnx
        _rec = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=f"{D}/encoder.int8.onnx", decoder=f"{D}/decoder.int8.onnx", joiner=f"{D}/joiner.int8.onnx",
            tokens=f"{D}/tokens.txt", num_threads=2, sample_rate=16000, feature_dim=80,
            decoding_method="greedy_search", model_type="nemo_transducer")
    return _rec


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", w)


def listen(x, sr):
    """Devuelve (texto, [(palabra, inicio_en_segundos)])."""
    st = recognizer().create_stream()
    st.accept_waveform(sr, x)
    recognizer().decode_stream(st)
    r = st.result
    words, cur, t0 = [], "", None
    for tok, ts in zip(r.tokens, r.timestamps):
        if tok.startswith(" "):
            if cur.strip():
                words.append((cur, t0))
            cur, t0 = "", None
            tok = tok[1:]
        if tok and t0 is None and norm(tok):
            t0 = ts
        cur += tok
    if cur.strip():
        words.append((cur, t0))
    words = [(w, t) for w, t in words if t is not None and norm(w)]
    return r.text.strip(), words


def token_starts(x, sr, toks):
    """Inicio de cada token del guion (o None si no se pudo anclar) y el texto reconocido."""
    hyp, heard = listen(x, sr)
    script, owner = [], []
    for i, tk in enumerate(toks):
        for j, w in enumerate(tk["spoken"].split()):
            n = norm(w)
            if n:
                script.append(n)
                owner.append((i, len([o for o in owner if o[0] == i]) == 0))
    hn = [norm(w) for w, _ in heard]
    starts = [None] * len(toks)
    sm = difflib.SequenceMatcher(None, script, hn, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                ti, first = owner[i1 + k]
                if first:
                    starts[ti] = heard[j1 + k][1] + OFFSET
        elif tag == "replace":
            ti, first = owner[i1]
            if first:
                starts[ti] = heard[j1][1] + OFFSET
    dur = len(x) / sr
    last = -1.0
    for i, s in enumerate(starts):          # orden estricto: descarta anclas que retroceden
        if s is not None:
            s = max(0.0, min(s, dur - 0.05))
            if s <= last + 0.02:
                starts[i] = None
            else:
                starts[i] = s
                last = s
    ratio = sm.ratio()
    return starts, hyp, ratio


def fill(starts, weights, dur):
    """Completa los inicios que faltan repartiendo por peso (fonemas) entre anclas vecinas."""
    n = len(starts)
    known = [(-1, 0.0)] + [(i, s) for i, s in enumerate(starts) if s is not None] + [(n, dur)]
    out = list(starts)
    if out[0] is None:
        out[0] = 0.0
        known = [(-1, 0.0), (0, 0.0)] + [k for k in known[1:] if k[0] != 0]
    for (ia, ta), (ib, tb) in zip(known, known[1:]):
        lo = max(ia, 0)
        if ib - lo <= 1:
            continue
        ws = np.array(weights[lo:ib], dtype=float)
        edges = ta + np.concatenate([[0], np.cumsum(ws) / ws.sum()]) * (tb - ta)
        for k in range(lo + 1, ib):
            out[k] = float(edges[k - lo])
    return out
