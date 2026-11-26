"""Control de la narracion: transcribe cada frase y la compara con el guion.

Uso: python3 -I engine/qa.py videos/<id>/out_<idioma> <en|es>
"""
import difflib
import glob
import json
import re
import sys
import unicodedata
import soundfile as sf
import sherpa_onnx

D = "/home/claude/models/asr/sherpa-onnx-whisper-base"


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


def main(out, lang):
    m = json.load(open(out + "/cache/voice.json"))
    x, sr = sf.read(out + "/cache/voice.wav", dtype="float32")
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{D}/base-encoder.int8.onnx", decoder=f"{D}/base-decoder.int8.onnx",
                                                     tokens=f"{D}/base-tokens.txt", language=lang, task="transcribe", num_threads=2)
    bad = 0
    for s in m["sentences"]:
        a, b = int(max(0, s["start"] - 0.15) * sr), int((s["end"] + 0.15) * sr)
        st = rec.create_stream()
        st.accept_waveform(sr, x[a:b])
        rec.decode_stream(st)
        hyp = st.result.text.strip()
        r = max(difflib.SequenceMatcher(None, norm(hyp), norm(ref)).ratio() for ref in (s["display"], s["spoken"]))
        flag = "OK " if r >= 0.8 else "REVISAR"
        bad += r < 0.8
        print("%s %.2f | guion: %s\n            | oido:  %s" % (flag, r, s["display"], hyp))
    print("duracion %.2fs | frases a revisar: %d de %d" % (m["total"], bad, len(m["sentences"])))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
