# -*- coding: utf-8 -*-
"""
Script de Renderização Principal do Reel — Sônia Torres
Produz: reel_sonia_comunicacao_infantil.mp4 (1080x1920, 30fps, H.264, AAC)
"""

import os
import sys
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30

FONT_PATH = os.path.join("assets", "fonts", "PlusJakartaSans-Variable.ttf")
AUDIO_MIX = os.path.join("assets", "audio", "audio_final_mixado.m4a")
OUTPUT_VIDEO = "reel_sonia_comunicacao_infantil.mp4"

# Cores da Identidade Visual
PURPLE_MAIN = (109, 59, 147)    # #6D3B93
PURPLE_DARK = (44, 18, 64)       # #2C1240
LAVENDER    = (232, 220, 241)   # #E8DCF1
GOLD_ACCENT = (200, 169, 106)   # #C8A96A
WHITE       = (255, 255, 255)

# Carregar imagens base
img_01 = Image.open("assets/images/scene_01.jpg").convert("RGB")
img_02a = Image.open("assets/images/scene_02a.jpg").convert("RGB")
img_02b = Image.open("assets/images/scene_02b.jpg").convert("RGB")
img_03 = Image.open("assets/images/scene_03.jpg").convert("RGB")
img_04 = Image.open("assets/images/scene_04.jpg").convert("RGB")
img_05 = Image.open("assets/images/scene_05_card.png").convert("RGB")

# Cronograma exato de cenas (em segundos)
SCENES = [
    {"name": "01", "img": img_01, "start": 0.00, "end": 4.75, "scale_start": 1.00, "scale_end": 1.05, "focus_y": 0.55},
    {"name": "02a", "img": img_02a, "start": 4.75, "end": 9.60, "scale_start": 1.00, "scale_end": 1.04, "focus_y": 0.50},
    {"name": "02b", "img": img_02b, "start": 9.60, "end": 14.39, "scale_start": 1.00, "scale_end": 1.05, "focus_y": 0.45},
    {"name": "03", "img": img_03, "start": 14.39, "end": 24.16, "scale_start": 1.00, "scale_end": 1.05, "focus_y": 0.52},
    {"name": "04", "img": img_04, "start": 24.16, "end": 35.63, "scale_start": 1.00, "scale_end": 1.04, "focus_y": 0.48},
    {"name": "05", "img": img_05, "start": 35.63, "end": 39.13, "scale_start": 1.00, "scale_end": 1.02, "focus_y": 0.50},
]

TOTAL_DURATION = SCENES[-1]["end"]
TOTAL_FRAMES = int(round(TOTAL_DURATION * FPS))

# Fontes
font_title = ImageFont.truetype(FONT_PATH, 44)
font_badge = ImageFont.truetype(FONT_PATH, 28)
font_sub = ImageFont.truetype(FONT_PATH, 38)
font_sub_bold = ImageFont.truetype(FONT_PATH, 40)

# Overlays de texto de destaque (Top Area: Y ~ 200 - 320)
HIGHLIGHTS = [
    {"start": 0.00, "end": 4.75, "text": "SEU FILHO AINDA NÃO FALA?", "badge": "DESENVOLVIMENTO INFANTIL"},
    {"start": 4.75, "end": 14.39, "text": "GESTOS TAMBÉM COMUNICAM.", "badge": "LINGUAGEM NÃO VERBAL"},
    {"start": 14.39, "end": 16.50, "text": "1. OBSERVE OS SINAIS", "badge": "COMO RESPONDER"},
    {"start": 16.50, "end": 18.80, "text": "2. RESPONDA E DÊ NOME", "badge": "ESTÍMULO DIÁRIO"},
    {"start": 18.80, "end": 24.16, "text": "3. CRIE INTERAÇÃO", "badge": "MUITO ALÉM DAS PALAVRAS"},
    {"start": 24.16, "end": 35.63, "text": "NA DÚVIDA, PROCURE ORIENTAÇÃO", "badge": "ATENÇÃO AOS MARCOS"},
]

# Legendas Sincronizadas (Bottom Safe Zone: Y ~ 1400 - 1580)
SUBTITLES = [
    {"start": 0.00, "end": 1.80, "text": "Seu filho ainda não fala?"},
    {"start": 1.82, "end": 4.75, "text": "Talvez ele já esteja tentando\nconversar com você."},
    {"start": 4.75, "end": 9.60, "text": "Quando ele aponta, estende os braços\nou leva você até um brinquedo..."},
    {"start": 9.60, "end": 14.39, "text": "...pode estar comunicando um desejo,\numa necessidade ou um interesse."},
    {"start": 14.39, "end": 18.00, "text": "Observe esses sinais. Responda,\ndê nome ao que ele está mostrando..."},
    {"start": 18.00, "end": 20.80, "text": "...e crie oportunidades de interação."},
    {"start": 20.80, "end": 24.16, "text": "A comunicação vai muito além das palavras."},
    {"start": 24.16, "end": 29.42, "text": "Mas atenção: reconhecer esses sinais\nnão significa ignorar atrasos na fala."},
    {"start": 29.42, "end": 35.63, "text": "Se você tem dúvidas sobre o desenvolvimento\ndo seu filho, procure orientação fonoaudiológica."},
]

def render_frame_base(scene, t):
    progress = (t - scene["start"]) / max(0.001, (scene["end"] - scene["start"]))
    progress = max(0.0, min(1.0, progress))
    
    # Easing suave (smootherstep)
    smooth_p = progress * progress * (3 - 2 * progress)
    scale = scene["scale_start"] + (scene["scale_end"] - scene["scale_start"]) * smooth_p
    
    nw = int(round(W * scale))
    nh = int(round(H * scale))
    
    # Redimensionamento
    scaled = scene["img"].resize((nw, nh), Image.Resampling.BILINEAR)
    
    cx = nw / 2.0
    cy = nh * scene["focus_y"]
    
    left = int(round(cx - W / 2.0))
    top = int(round(cy - H / 2.0))
    
    left = max(0, min(left, nw - W))
    top = max(0, min(top, nh - H))
    
    cropped = scaled.crop((left, top, left + W, top + H))
    return cropped

def draw_text_overlays(frame, t):
    # Se for o card final (última cena), não sobrepor legendas ou títulos adicionais
    if t >= 35.63:
        return frame

    draw = ImageDraw.Draw(frame, "RGBA")

    # 1. Título de Destaque Superior
    hl = None
    for h in HIGHLIGHTS:
        if h["start"] <= t < h["end"]:
            hl = h
            break
            
    if hl:
        # Fade in suave do título
        time_in_hl = t - hl["start"]
        alpha = min(255, int(time_in_hl * 600)) if time_in_hl < 0.4 else 255
        
        # Pílula de fundo do título
        badge_txt = hl["badge"]
        title_txt = hl["text"]
        
        bbox_t = draw.textbbox((0, 0), title_txt, font=font_title)
        tw = bbox_t[2] - bbox_t[0]
        th = bbox_t[3] - bbox_t[1]
        
        bbox_b = draw.textbbox((0, 0), badge_txt, font=font_badge)
        bw = bbox_b[2] - bbox_b[0]
        bh = bbox_b[3] - bbox_b[1]
        
        box_w = max(tw, bw) + 60
        box_h = th + bh + 45
        box_x = (W - box_w) // 2
        box_y = 190
        
        # Fundo escuro semitransparente roxo
        bg_color = (44, 18, 64, int(alpha * 0.88))
        draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=24, fill=bg_color, outline=(200, 169, 106, int(alpha * 0.9)), width=2)
        
        # Texto Badge
        draw.text(((W - bw) // 2, box_y + 16), badge_txt, font=font_badge, fill=(200, 169, 106, alpha))
        # Texto Título
        draw.text(((W - tw) // 2, box_y + 20 + bh + 10), title_txt, font=font_title, fill=(255, 255, 255, alpha))

    # 2. Legenda Sincronizada Inferior
    sub = None
    for s in SUBTITLES:
        if s["start"] <= t < s["end"]:
            sub = s
            break
            
    if sub:
        lines = sub["text"].split("\n")
        line_heights = []
        line_widths = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_sub)
            line_widths.append(bbox[2] - bbox[0])
            line_heights.append(bbox[3] - bbox[1])
            
        box_w = max(line_widths) + 54
        total_text_h = sum(line_heights) + (len(lines) - 1) * 14
        box_h = total_text_h + 36
        
        box_x = (W - box_w) // 2
        box_y = 1460 - (box_h // 2)
        
        # Pílula da legenda
        draw.rounded_rectangle(
            [box_x, box_y, box_x + box_w, box_y + box_h],
            radius=20,
            fill=(44, 18, 64, 215),
            outline=(232, 220, 241, 160),
            width=2
        )
        
        cur_y = box_y + 18
        for i, line in enumerate(lines):
            lw = line_widths[i]
            lx = (W - lw) // 2
            draw.text((lx, cur_y), line, font=font_sub, fill=(255, 255, 255, 255))
            cur_y += line_heights[i] + 14

    return frame

def main():
    print(f"Iniciando renderização de {TOTAL_FRAMES} frames ({TOTAL_DURATION:.2f}s) a {FPS} fps...")
    
    # Iniciar processo do ffmpeg para receber rawvideo via stdin pipe
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO_MIX,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "copy",
        "-shortest",
        OUTPUT_VIDEO
    ]
    
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE)
    
    # Pré-alocação e loop de renderização
    scene_idx = 0
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / float(FPS)
        
        # Localizar cena ativa
        while scene_idx < len(SCENES) - 1 and t >= SCENES[scene_idx]["end"]:
            scene_idx += 1
            
        scene = SCENES[scene_idx]
        frame = render_frame_base(scene, t)
        frame = draw_text_overlays(frame, t)
        
        # Enviar bytes para o ffmpeg
        proc.stdin.write(frame.tobytes())
        
        if frame_idx % 150 == 0 or frame_idx == TOTAL_FRAMES - 1:
            print(f"Progresso: frame {frame_idx}/{TOTAL_FRAMES} ({frame_idx*100//TOTAL_FRAMES}%) - tempo: {t:.2f}s")
            
    proc.stdin.close()
    proc.wait()
    
    if proc.returncode == 0:
        print(f"\n=======================================================")
        print(f"Reel renderizado com SUCESSO: {OUTPUT_VIDEO}")
        print(f"=======================================================")
    else:
        print(f"Erro na renderização. Código: {proc.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
