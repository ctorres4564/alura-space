# -*- coding: utf-8 -*-
"""
Geração de Áudio e Narração - Reel: Limites x Comunicação (Sônia Torres)
Utiliza edge-tts com voz neural pt-BR-FranciscaNeural com entonações personalizadas.
"""

import os
import asyncio
import edge_tts
from mutagen.mp3 import MP3

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\1MATERIASIDASONIA\01reels_novos"
AUDIO_DIR = os.path.join(BASE_DIR, "publicacao", "limites-comunicacao", "audios")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE = "pt-BR-FranciscaNeural"

# Falas estruturadas conforme briefing
FALAS = [
    {
        "id": 1,
        "texto": "Essa criança não precisa de fono. Precisa é de limites!",
        "rate": "+0%",
        "pitch": "+0Hz"
    },
    {
        "id": 2,
        "texto": "Ela tenta dizer o que quer. Mas nem sempre consegue se fazer entender.",
        "rate": "-3%",
        "pitch": "-1Hz"
    },
    {
        "id": 3,
        "texto": "E se o problema não for falta de limites?",
        "rate": "-5%",
        "pitch": "+1Hz"
    },
    {
        "id": 4,
        "texto": "Dificuldades para compreender ou se expressar também podem gerar frustração.",
        "rate": "-4%",
        "pitch": "-2Hz"
    },
    {
        "id": 5,
        "texto": "Antes de julgar, procure compreender.",
        "rate": "-7%",
        "pitch": "-3Hz"
    }
]

async def gerar_audios():
    print("Iniciando geração de áudios neurais pt-BR...")
    concat_list = []
    
    for item in FALAS:
        out_file = os.path.join(AUDIO_DIR, f"audio_{item['id']}.mp3")
        communicate = edge_tts.Communicate(
            item["texto"],
            VOICE,
            rate=item["rate"],
            pitch=item["pitch"]
        )
        await communicate.save(out_file)
        
        audio_info = MP3(out_file).info
        dur = audio_info.length
        print(f"Cena {item['id']} gerada com sucesso ({dur:.2f}s): \"{item['texto']}\"")
        concat_list.append(out_file)
        
    concat_file_path = os.path.join(AUDIO_DIR, "concat_audios.txt")
    with open(concat_file_path, "w", encoding="utf-8") as f:
        for p in concat_list:
            f.write(f"file '{p.replace('\\', '/')}'\n")
            
    print(f"Lista de concatenação salva em: {concat_file_path}")

if __name__ == "__main__":
    asyncio.run(gerar_audios())
