#!/usr/bin/env bash
# Prepara el motor en un entorno nuevo (unos 3-5 min). Uso: bash setup.sh
set -e
pip install --break-system-packages -q kokoro-onnx==0.6.1 sherpa-onnx soundfile pillow numpy onnxruntime
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
M=/home/claude/models
mkdir -p $M/kokoro $M/asr_parakeet_v3
R=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f $M/kokoro/kokoro-v1.0.onnx ] || curl -sL -o $M/kokoro/kokoro-v1.0.onnx $R/kokoro-v1.0.onnx
[ -f $M/kokoro/voices-v1.0.bin ] || curl -sL -o $M/kokoro/voices-v1.0.bin $R/voices-v1.0.bin
P=sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8
[ -d $M/asr_parakeet_v3/$P ] || curl -sL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/$P.tar.bz2 | tar -xj -C $M/asr_parakeet_v3
# el motor espera vivir en /home/claude/pipeline
mkdir -p /home/claude/pipeline
ln -sfn "$(cd "$(dirname "$0")" && pwd)/engine" /home/claude/pipeline/engine
ln -sfn "$(cd "$(dirname "$0")" && pwd)/guiones" /home/claude/pipeline/videos
python3 -c "import sys; sys.path.insert(0,'/home/claude/pipeline/engine'); import core, fx, scenes2, voice, align, v4; print('motor listo')"
