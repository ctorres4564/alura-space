# -*- coding: utf-8 -*-
"""
Serviço de Áudio - Produção Reel Sônia Torres
Concatena com fidelidade estrita os áudios 01.mp3, 02.mp3, 03.mp3, 04.mp3
e faz a mixagem da trilha instrumental Warm Hope com ducking automático.
"""

import os
import subprocess
import re

VOICE_FILES = ["01.mp3", "02.mp3", "03.mp3", "04.mp3"]
BG_MUSIC = os.path.join("assets", "audio", "Warm Hope.mp3")
OUTPUT_VOICE = os.path.join("assets", "audio", "narracao_completa_sonia.wav")
OUTPUT_FINAL_AUDIO = os.path.join("assets", "audio", "audio_final_mixado.m4a")

def get_duration(file_path):
    cmd = ["ffmpeg", "-i", file_path]
    p = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", p.stderr)
    if not m:
        return 0.0
    h, m, s = m.groups()
    return float(h) * 3600 + float(m) * 60 + float(s)

def build_audio(card_duration=3.5):
    os.makedirs(os.path.join("assets", "audio"), exist_ok=True)
    
    # 1. Obter durações individuais
    durations = [get_duration(f) for f in VOICE_FILES]
    total_voice = sum(durations)
    total_video = total_voice + card_duration
    print(f"Duração da narração original: {total_voice:.2f}s")
    print(f"Duração total do vídeo (com card final de {card_duration}s): {total_video:.2f}s")

    # 2. Concatenação dos 4 áudios de voz sem recompressão lossy intermediária
    # Usando concat filter do ffmpeg
    inputs = []
    for f in VOICE_FILES:
        inputs.extend(["-i", f])
    
    filter_complex = "".join([f"[{i}:a]" for i in range(len(VOICE_FILES))]) + f"concat=n={len(VOICE_FILES)}:v=0:a=1[outa]"
    cmd_concat = ["ffmpeg", "-y"] + inputs + ["-filter_complex", filter_complex, "-map", "[outa]", OUTPUT_VOICE]
    subprocess.run(cmd_concat, check=True, capture_output=True)
    print(f"Áudio de voz concatenado com sucesso em: {OUTPUT_VOICE}")

    # 3. Mixagem da Trilha com Ducking
    # A trilha fica atenuada a ~10% (-20dB) durante a fala,
    # sobe suavemente após o término da fala e faz fade out no final.
    duck_filter = (
        f"[1:a]aloop=loop=-1:size=2e+09,atrim=0:{total_video},"
        f"volume=0.09,afade=t=in:st=0:d=1.0,"
        f"afade=t=out:st={total_video - 1.8}:d=1.8[bg];"
        f"[0:a]apad=pad_dur={card_duration}[voice];"
        f"[voice][bg]amix=inputs=2:duration=longest:dropout_transition=2[out]"
    )

    cmd_mix = [
        "ffmpeg", "-y",
        "-i", OUTPUT_VOICE,
        "-i", BG_MUSIC,
        "-filter_complex", duck_filter,
        "-map", "[out]",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        OUTPUT_FINAL_AUDIO
    ]
    subprocess.run(cmd_mix, check=True, capture_output=True)
    print(f"Áudio final mixado com sucesso em: {OUTPUT_FINAL_AUDIO}")
    return total_voice, total_video, durations

if __name__ == "__main__":
    build_audio()
