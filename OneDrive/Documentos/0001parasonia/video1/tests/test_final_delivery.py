# -*- coding: utf-8 -*-
"""
Validação Técnica Automatizada dos Entregáveis do Reel
Sônia Torres — Fonoaudióloga
"""

import os
import subprocess
import json
import pytest
from PIL import Image

VIDEO_PATH = "reel_sonia_comunicacao_infantil.mp4"
COVER_PATH = "capa_reel_sonia.png"
CAPTION_PATH = "legenda_reel_sonia.txt"

def test_video_deliverable():
    assert os.path.exists(VIDEO_PATH), "Arquivo de vídeo reel_sonia_comunicacao_infantil.mp4 não encontrado."
    file_size_mb = os.path.getsize(VIDEO_PATH) / (1024 * 1024)
    assert file_size_mb >= 5.0, f"Tamanho do vídeo suspeito: {file_size_mb:.2f} MB"
    
    # Inspecionar via FFmpeg
    cmd = ["ffmpeg", "-i", VIDEO_PATH]
    p = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    
    # Validar resolução 1080x1920
    assert "1080x1920" in p.stderr, "Resolução do vídeo não é 1080x1920."
    assert "h264" in p.stderr, "Codec do vídeo não é H.264."
    assert "aac" in p.stderr, "Codec de áudio não é AAC."
    
    # Validar duração (~39s)
    import re
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", p.stderr)
    assert m is not None, "Duração do vídeo não pôde ser determinada."
    h, mins, s = m.groups()
    dur = float(h)*3600 + float(mins)*60 + float(s)
    assert 38.0 <= dur <= 40.0, f"Duração do vídeo fora da faixa esperada: {dur:.2f}s"

def test_cover_deliverable():
    assert os.path.exists(COVER_PATH), "Arquivo de capa capa_reel_sonia.png não encontrado."
    img = Image.open(COVER_PATH)
    assert img.size == (1080, 1920), f"Dimensões da capa incorretas: {img.size}"

def test_caption_deliverable():
    assert os.path.exists(CAPTION_PATH), "Arquivo legenda_reel_sonia.txt não encontrado."
    with open(CAPTION_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Sônia Torres" in content, "Nome da profissional ausente na legenda."
    assert "sonia.fonosuite.com" in content, "Site da profissional ausente na legenda."
    assert "(21) 97748-6801" in content, "Telefone da profissional ausente na legenda."
    assert "#Fonoaudiologia" in content, "Hashtag essencial ausente."
