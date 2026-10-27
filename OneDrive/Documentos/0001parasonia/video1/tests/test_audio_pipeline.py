import os
import subprocess
import re
import pytest

AUDIO_FILES = ['01.mp3', '02.mp3', '03.mp3', '04.mp3']
FONT_FILE = os.path.join('assets', 'fonts', 'PlusJakartaSans-Variable.ttf')
MUSIC_FILE = os.path.join('assets', 'audio', 'Warm Hope.mp3')

def get_audio_duration(file_path):
    cmd = ['ffmpeg', '-i', file_path]
    p = subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    m = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', p.stderr)
    if not m:
        return 0.0
    hours, minutes, seconds = m.groups()
    return float(hours) * 3600 + float(minutes) * 60 + float(seconds)

def test_audio_files_exist():
    for f in AUDIO_FILES:
        assert os.path.exists(f), f"Arquivo de áudio {f} não encontrado."

def test_audio_durations():
    durations = [get_audio_duration(f) for f in AUDIO_FILES]
    assert 4.5 <= durations[0] <= 5.0, f"Duração do áudio 01 fora do esperado: {durations[0]}"
    assert 9.0 <= durations[1] <= 10.0, f"Duração do áudio 02 fora do esperado: {durations[1]}"
    assert 9.0 <= durations[2] <= 10.2, f"Duração do áudio 03 fora do esperado: {durations[2]}"
    assert 11.0 <= durations[3] <= 12.0, f"Duração do áudio 04 fora do esperado: {durations[3]}"
    
    total_voice = sum(durations)
    assert 35.0 <= total_voice <= 36.5, f"Duração total da locução fora do esperado: {total_voice}"

def test_assets_exist():
    assert os.path.exists(FONT_FILE), "Fonte institucional Plus Jakarta Sans não encontrada."
    assert os.path.exists(MUSIC_FILE), "Trilha musical institucional Warm Hope não encontrada."
