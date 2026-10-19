# -*- coding: utf-8 -*-
"""
Script de Renderização v2 - Reel Sônia Torres
Adaptação da narração humana gravada da pasta 'audios2'

Timeline:
- Cena 1: 0.00s a 6.53s (audio1.mp3)
- Cena 2: 6.53s a 12.64s (audio2.mp3)
- Cena 3: 12.64s a 21.08s (audio3.mp3)
- Cena 4: 21.08s a 29.05s (audio4.mp3)
- Cena 5: 29.05s a 35.32s (audio5.mp3)
- Cena 6: 35.32s a 41.50s (audio6.mp3 + card final Sônia Torres com 6.18s de exposição)
Duração total: 41.50s
"""

import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from mutagen.mp3 import MP3

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\1MATERIASIDASONIA\01reels_novos"
AUDIOS2_DIR = os.path.join(BASE_DIR, "audios2")
PUBLICACAO_DIR = os.path.join(BASE_DIR, "publicacao", "limites-comunicacao")
IMG_DIR = os.path.join(PUBLICACAO_DIR, "imagens")
AUDIO_DIR = os.path.join(PUBLICACAO_DIR, "audios")
CLIP_DIR = os.path.join(PUBLICACAO_DIR, "clipes")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(CLIP_DIR, exist_ok=True)

FFMPEG = "ffmpeg"
BGM_SOURCE = os.path.join(BASE_DIR, "publicacao", "telas-objecao", "musica_fundo.mp3")

FONT_POPPINS_BOLD = os.path.join(BASE_DIR, "assets", "fonts", "Poppins-Bold.ttf")
FONT_GEORGIA_BOLD = r"C:\Windows\Fonts\georgiab.ttf"
FONT_SEGOE = r"C:\Windows\Fonts\segoeui.ttf"

COR_DOURADO = (212, 175, 55, 255)
COR_DOURADO_CLARO = (235, 205, 110, 255)
COR_ROXO_LILAS = (157, 114, 178, 255)
COR_BRANCO = (255, 255, 255, 255)
COR_OFFWHITE = (248, 246, 242, 255)

def criar_caixa_texto(draw, lines, font, center_y, box_opacity=0.58, text_color=COR_BRANCO, highlight_word=None, highlight_color=COR_DOURADO):
    line_height = int(font.size * 1.34)
    total_h = len(lines) * line_height
    start_y = center_y - (total_h // 2)
    
    max_line_w = 0
    for line in lines:
        bbox = font.getbbox(line)
        max_line_w = max(max_line_w, bbox[2] - bbox[0])
        
    padding_x = 34
    padding_y = 22
    box_x0 = (1080 - max_line_w) // 2 - padding_x
    box_x1 = (1080 + max_line_w) // 2 + padding_x
    box_y0 = start_y - padding_y
    box_y1 = start_y + total_h + padding_y - (line_height - font.size)
    
    alpha = int(255 * box_opacity)
    draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=18, fill=(12, 8, 18, alpha), outline=(212, 175, 55, int(alpha * 0.4)), width=2)
    
    curr_y = start_y
    for line in lines:
        bbox = font.getbbox(line)
        lw = bbox[2] - bbox[0]
        lx = (1080 - lw) // 2
        
        draw.text((lx + 2, curr_y + 2), line, font=font, fill=(0, 0, 0, 200))
        
        if highlight_word and highlight_word in line:
            parts = line.split(highlight_word)
            before = parts[0]
            w_before = font.getbbox(before)[2] - font.getbbox(before)[0] if before else 0
            w_hl = font.getbbox(highlight_word)[2] - font.getbbox(highlight_word)[0]
            
            draw.text((lx, curr_y), before, font=font, fill=text_color)
            draw.text((lx + w_before, curr_y), highlight_word, font=font, fill=highlight_color)
            if len(parts) > 1 and parts[1]:
                draw.text((lx + w_before + w_hl, curr_y), parts[1], font=font, fill=text_color)
        else:
            draw.text((lx, curr_y), line, font=font, fill=text_color)
            
        curr_y += line_height

def gerar_quadros_visuais_v2():
    print("1. Gerando quadros visuais adaptados aos novos textos...")
    
    # -----------------------------
    # CENA 1: audio1 (6.53s)
    # Parte A (3.20s): "Na minha época, criança assim precisava era de limites."
    # Parte B (3.33s): "Quantas vezes você já ouviu essa frase?"
    # -----------------------------
    base1 = Image.open(os.path.join(IMG_DIR, "cena1_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    font_c1 = ImageFont.truetype(FONT_POPPINS_BOLD, 44)
    
    q1a = base1.copy()
    overlay = Image.new("RGBA", q1a.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["“NA MINHA ÉPOCA, CRIANÇA", "ASSIM PRECISAVA DE LIMITES!”"], font_c1, center_y=750, box_opacity=0.62, highlight_word="LIMITES!”", highlight_color=COR_DOURADO)
    Image.alpha_composite(q1a, overlay).convert("RGB").save(os.path.join(IMG_DIR, "c1_fase_a.png"))
    
    q1b = base1.copy()
    overlay = Image.new("RGBA", q1b.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["QUANTAS VEZES VOCÊ", "JÁ OUVIU ESSA FRASE?"], font_c1, center_y=750, box_opacity=0.62)
    Image.alpha_composite(q1b, overlay).convert("RGB").save(os.path.join(IMG_DIR, "c1_fase_b.png"))
    
    # -----------------------------
    # CENA 2: audio2 (6.11s)
    # Parte A (3.00s): "Mas será que todo comportamento interpretado como desobediência..."
    # Parte B (3.11s): "...é realmente falta de limites?"
    # -----------------------------
    base2 = Image.open(os.path.join(IMG_DIR, "cena2_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    font_c2 = ImageFont.truetype(FONT_POPPINS_BOLD, 44)
    
    q2a = base2.copy()
    overlay = Image.new("RGBA", q2a.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["TODO COMPORTAMENTO INTERPRETADO", "COMO DESOBEDIÊNCIA..."], font_c2, center_y=750, box_opacity=0.60)
    Image.alpha_composite(q2a, overlay).convert("RGB").save(os.path.join(IMG_DIR, "c2_fase_a.png"))
    
    q2b = base2.copy()
    overlay = Image.new("RGBA", q2b.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["...É REALMENTE", "FALTA DE LIMITES?"], font_c2, center_y=750, box_opacity=0.62, highlight_word="LIMITES?", highlight_color=COR_DOURADO)
    Image.alpha_composite(q2b, overlay).convert("RGB").save(os.path.join(IMG_DIR, "c2_fase_b.png"))
    
    # -----------------------------
    # CENA 3: audio3 (8.44s)
    # Parte A (4.20s): "Algumas crianças encontram dificuldades para compreender ou expressar..."
    # Parte B (4.24s): "...e essa dificuldade pode provocar frustração."
    # -----------------------------
    base3 = Image.open(os.path.join(IMG_DIR, "cena3_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    font_c3 = ImageFont.truetype(FONT_POPPINS_BOLD, 44)
    
    q3a = base3.copy()
    overlay = Image.new("RGBA", q3a.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["DIFICULDADES PARA", "COMPREENDER OU SE EXPRESSAR..."], font_c3, center_y=760, box_opacity=0.60)
    Image.alpha_composite(q3a, overlay).convert("RGB").save(os.path.join(IMG_DIR, "c3_fase_a.png"))
    
    q3b = base3.copy()
    overlay = Image.new("RGBA", q3b.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["...PODEM GERAR", "MUITA FRUSTRAÇÃO."], font_c3, center_y=760, box_opacity=0.62, highlight_word="FRUSTRAÇÃO.", highlight_color=COR_DOURADO)
    Image.alpha_composite(q3b, overlay).convert("RGB").save(os.path.join(IMG_DIR, "c3_fase_b.png"))
    
    # -----------------------------
    # CENA 4: audio4 (7.97s)
    # Parte A (3.90s): "Isso não significa que toda a crise esteja relacionada à linguagem."
    # Parte B (4.07s): "Significa que precisamos compreender antes de julgar."
    # -----------------------------
    base4 = Image.open(os.path.join(IMG_DIR, "cena4_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    font_c4 = ImageFont.truetype(FONT_POPPINS_BOLD, 44)
    
    q4a = base4.copy()
    overlay = Image.new("RGBA", q4a.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["NEM TODA CRISE", "ESTÁ NA LINGUAGEM."], font_c4, center_y=750, box_opacity=0.60)
    Image.alpha_composite(q4a, overlay).convert("RGB").save(os.path.join(IMG_DIR, "c4_fase_a.png"))
    
    q4b = base4.copy()
    overlay = Image.new("RGBA", q4b.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["PRECISAMOS COMPREENDER", "ANTES DE JULGAR."], font_c4, center_y=750, box_opacity=0.62, highlight_word="COMPREENDER", highlight_color=COR_DOURADO)
    Image.alpha_composite(q4b, overlay).convert("RGB").save(os.path.join(IMG_DIR, "c4_fase_b.png"))
    
    # -----------------------------
    # CENA 5: audio5 (6.27s)
    # Frase de Impacto reflexiva com tipografia grande
    # -----------------------------
    img5 = Image.new("RGBA", (1080, 1920), (12, 6, 18, 255))
    d5 = ImageDraw.Draw(img5)
    d5.rectangle([40, 60, 1040, 1860], outline=(212, 175, 55, 60), width=2)
    d5.rectangle([52, 72, 1028, 1848], outline=(157, 114, 178, 40), width=1)
    
    font_f1 = ImageFont.truetype(FONT_GEORGIA_BOLD, 48)
    font_f2 = ImageFont.truetype(FONT_GEORGIA_BOLD, 46)
    
    t_f1 = ["NEM TODA CRISE", "É BIRRA."]
    t_f2 = ["CONFUNDIMOS COMUNICAÇÃO", "COM FALTA DE EDUCAÇÃO?"]
    
    cy = 720
    for l in t_f1:
        bbox = font_f1.getbbox(l)
        w = bbox[2] - bbox[0]
        d5.text(((1080 - w) // 2 + 2, cy + 2), l, font=font_f1, fill=(0, 0, 0, 220))
        d5.text(((1080 - w) // 2, cy), l, font=font_f1, fill=COR_BRANCO)
        cy += 72
        
    cy += 40
    d5.line([(420, cy), (660, cy)], fill=(212, 175, 55, 180), width=3)
    cy += 60
    
    for l in t_f2:
        bbox = font_f2.getbbox(l)
        w = bbox[2] - bbox[0]
        d5.text(((1080 - w) // 2 + 2, cy + 2), l, font=font_f2, fill=(0, 0, 0, 220))
        d5.text(((1080 - w) // 2, cy), l, font=font_f2, fill=COR_DOURADO)
        cy += 70
        
    img5.convert("RGB").save(os.path.join(IMG_DIR, "cena5_v2_render.png"))
    
    # -----------------------------
    # CENA 6: Card Final Sônia Torres (6.18s)
    # audio6 (2.19s) toca no início: "Conte sua opinião nos comentários."
    # -----------------------------
    bg6 = base4.filter(ImageFilter.GaussianBlur(radius=14))
    dimmer6 = Image.new("RGBA", (1080, 1920), (14, 7, 22, 170))
    comp6 = Image.alpha_composite(bg6, dimmer6)
    
    card_w = 960
    card_h = 760
    card_x0 = (1080 - card_w) // 2
    card_y0 = (1920 - card_h) // 2 - 20
    card_x1 = card_x0 + card_w
    card_y1 = card_y0 + card_h
    
    d6 = ImageDraw.Draw(comp6)
    d6.rounded_rectangle([card_x0 - 4, card_y0 + 8, card_x1 + 4, card_y1 + 18], radius=32, fill=(0, 0, 0, 120))
    d6.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=30, fill=(24, 12, 36, 248), outline=COR_DOURADO, width=3)
    
    font_c6_title = ImageFont.truetype(FONT_POPPINS_BOLD, 38)
    font_c6_cta = ImageFont.truetype(FONT_POPPINS_BOLD, 34)
    font_c6_name = ImageFont.truetype(FONT_GEORGIA_BOLD, 42)
    font_c6_sub = ImageFont.truetype(FONT_POPPINS_BOLD, 24)
    font_c6_info = ImageFont.truetype(FONT_SEGOE, 26)
    font_c6_link = ImageFont.truetype(FONT_POPPINS_BOLD, 28)
    
    cy6 = card_y0 + 55
    p_lines = ["FALTA DE LIMITES OU", "DIFICULDADE DE COMUNICAÇÃO?"]
    for l in p_lines:
        bw = font_c6_title.getbbox(l)[2] - font_c6_title.getbbox(l)[0]
        d6.text(((1080 - bw) // 2, cy6), l, font=font_c6_title, fill=COR_BRANCO)
        cy6 += 48
        
    cy6 += 14
    cta_txt = "O QUE VOCÊ PENSA? COMENTE!"
    cw = font_c6_cta.getbbox(cta_txt)[2] - font_c6_cta.getbbox(cta_txt)[0]
    d6.text(((1080 - cw) // 2, cy6), cta_txt, font=font_c6_cta, fill=COR_DOURADO_CLARO)
    
    cy6 += 64
    d6.line([(card_x0 + 80, cy6), (card_x1 - 80, cy6)], fill=(212, 175, 55, 140), width=2)
    
    cy6 += 36
    nw = font_c6_name.getbbox("SÔNIA TORRES")[2] - font_c6_name.getbbox("SÔNIA TORRES")[0]
    d6.text(((1080 - nw) // 2, cy6), "SÔNIA TORRES", font=font_c6_name, fill=COR_DOURADO)
    
    cy6 += 50
    sw = font_c6_sub.getbbox("FONOAUDIÓLOGA")[2] - font_c6_sub.getbbox("FONOAUDIÓLOGA")[0]
    d6.text(((1080 - sw) // 2, cy6), "FONOAUDIÓLOGA", font=font_c6_sub, fill=COR_ROXO_LILAS)
    
    cy6 += 46
    for l in ["Av. Vicente de Carvalho, 909 — Sala 413", "Vicente de Carvalho • Rio de Janeiro — RJ"]:
        bw = font_c6_info.getbbox(l)[2] - font_c6_info.getbbox(l)[0]
        d6.text(((1080 - bw) // 2, cy6), l, font=font_c6_info, fill=COR_OFFWHITE)
        cy6 += 34
        
    cy6 += 8
    tel = "Telefone: (21) 97748-6801"
    tw = font_c6_info.getbbox(tel)[2] - font_c6_info.getbbox(tel)[0]
    d6.text(((1080 - tw) // 2, cy6), tel, font=font_c6_info, fill=COR_DOURADO_CLARO)
    
    cy6 += 44
    site = "sonia.fonosuite.com"
    siw = font_c6_link.getbbox(site)[2] - font_c6_link.getbbox(site)[0]
    d6.text(((1080 - siw) // 2, cy6), site, font=font_c6_link, fill=COR_ROXO_LILAS)
    
    comp6.convert("RGB").save(os.path.join(IMG_DIR, "cena6_v2_render.png"))

def renderizar_clipes_v2():
    print("2. Renderizando clipes de vídeo com os novos tempos...")
    
    # CENA 1: total 6.53s (3.20s + 3.33s)
    # Slow push-in suave
    c1a = os.path.join(CLIP_DIR, "v2_c1a.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "c1_fase_a.png"),
        "-t", "3.200",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0006,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=96:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c1a
    ], check=True)
    
    c1b = os.path.join(CLIP_DIR, "v2_c1b.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "c1_fase_b.png"),
        "-t", "3.330",
        "-vf", "scale=1188:2112,zoompan=z='min(1.03+0.0006*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=100:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c1b
    ], check=True)
    
    # CENA 2: total 6.11s (3.00s + 3.11s)
    # Pan suave
    c2a = os.path.join(CLIP_DIR, "v2_c2a.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "c2_fase_a.png"),
        "-t", "3.000",
        "-vf", "scale=1188:2112,zoompan=z='1.04':x='iw*0.04+on*0.4':y='ih*0.04':d=90:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c2a
    ], check=True)
    
    c2b = os.path.join(CLIP_DIR, "v2_c2b.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "c2_fase_b.png"),
        "-t", "3.110",
        "-vf", "scale=1188:2112,zoompan=z='1.04':x='iw*0.07+on*0.4':y='ih*0.04':d=93:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c2b
    ], check=True)
    
    # CENA 3: total 8.44s (4.20s + 4.24s)
    # Slow close-in no rosto emotivo
    c3a = os.path.join(CLIP_DIR, "v2_c3a.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "c3_fase_a.png"),
        "-t", "4.200",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0005,1.05)':x='iw/2-(iw/zoom/2)':y='ih*0.45-(ih/zoom*0.45)':d=126:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c3a
    ], check=True)
    
    c3b = os.path.join(CLIP_DIR, "v2_c3b.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "c3_fase_b.png"),
        "-t", "4.240",
        "-vf", "scale=1188:2112,zoompan=z='min(1.03+0.0005*on,1.07)':x='iw/2-(iw/zoom/2)':y='ih*0.45-(ih/zoom*0.45)':d=127:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c3b
    ], check=True)
    
    # CENA 4: total 7.97s (3.90s + 4.07s)
    # Tracking suave na conexão acolhedora
    c4a = os.path.join(CLIP_DIR, "v2_c4a.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "c4_fase_a.png"),
        "-t", "3.900",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0004,1.04)':x='iw*0.04+on*0.25':y='ih/2-(ih/zoom/2)':d=117:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c4a
    ], check=True)
    
    c4b = os.path.join(CLIP_DIR, "v2_c4b.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "c4_fase_b.png"),
        "-t", "4.070",
        "-vf", "scale=1188:2112,zoompan=z='min(1.02+0.0004*on,1.06)':x='iw*0.06+on*0.25':y='ih/2-(ih/zoom/2)':d=122:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c4b
    ], check=True)
    
    # CENA 5: total 6.27s (audio5.mp3)
    c5 = os.path.join(CLIP_DIR, "v2_c5.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena5_v2_render.png"),
        "-t", "6.270",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0003,1.03)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=188:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c5
    ], check=True)
    
    # CENA 6: total 6.18s (audio6 toca de 0 a 2.19s, card continua visível)
    c6 = os.path.join(CLIP_DIR, "v2_c6.mp4")
    subprocess.run([
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena6_v2_render.png"),
        "-t", "6.180",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0002,1.02)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=185:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        c6
    ], check=True)
    
    clip_list = [c1a, c1b, c2a, c2b, c3a, c3b, c4a, c4b, c5, c6]
    concat_txt = os.path.join(CLIP_DIR, "concat_video_v2.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clip_list:
            f.write(f"file '{c.replace('\\', '/')}'\n")
            
    print("Clipes v2 gerados com sucesso!")

def mixar_audio_e_video_v2():
    print("3. Mixando áudios da pasta audios2 com trilha sonora e normalização...")
    
    # Delays exatos baseados na timeline dos áudios:
    # audio1: 0ms (dura 6531ms)
    # audio2: 6531ms (dura 6113ms)
    # audio3: 12644ms (dura 8438ms)
    # audio4: 21082ms (dura 7967ms)
    # audio5: 29049ms (dura 6269ms)
    # audio6: 35318ms (dura 2194ms)
    # Final da voz: 37512ms
    # Card final encerra em: 41500ms
    
    a1 = os.path.join(AUDIOS2_DIR, "audio1.mp3")
    a2 = os.path.join(AUDIOS2_DIR, "audio2.mp3")
    a3 = os.path.join(AUDIOS2_DIR, "audio3.mp3")
    a4 = os.path.join(AUDIOS2_DIR, "audio4.mp3")
    a5 = os.path.join(AUDIOS2_DIR, "audio5.mp3")
    a6 = os.path.join(AUDIOS2_DIR, "audio6.mp3")
    
    # Impacto discreto de abertura (55Hz senoidal com decay suave)
    impact_wav = os.path.join(AUDIO_DIR, "impacto_cena1.wav")
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", "sine=frequency=55:duration=0.7",
        "-af", "afade=t=out:st=0.1:d=0.6,volume=0.45",
        impact_wav
    ], check=True)
    
    voice_mix_wav = os.path.join(AUDIO_DIR, "narracao_mixada_v2.wav")
    cmd_voice_mix = [
        FFMPEG, "-y",
        "-i", a1,
        "-i", a2,
        "-i", a3,
        "-i", a4,
        "-i", a5,
        "-i", a6,
        "-i", impact_wav,
        "-filter_complex",
        "[0:a]adelay=0|0[v1];"
        "[1:a]adelay=6531|6531[v2];"
        "[2:a]adelay=12644|12644[v3];"
        "[3:a]adelay=21082|21082[v4];"
        "[4:a]adelay=29049|29049[v5];"
        "[5:a]adelay=35318|35318[v6];"
        "[6:a]adelay=50|50[imp];"
        "[v1][v2][v3][v4][v5][v6][imp]amix=inputs=7:duration=longest:dropout_transition=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=11[outv]",
        "-map", "[outv]",
        voice_mix_wav
    ]
    subprocess.run(cmd_voice_mix, check=True)
    
    print("4. Montando vídeo final renderizado v2...")
    concat_video_txt = os.path.join(CLIP_DIR, "concat_video_v2.txt")
    output_video = os.path.join(PUBLICACAO_DIR, "reel_sonia_limites_final.mp4")
    
    # Mixagem com trilha de fundo:
    # 0s a 37.5s: música sob a voz em segundo plano suave (-26 dB)
    # 37.5s a 39.5s: subida suave para -15 dB
    # 39.5s a 41.5s: fade out musical suave
    cmd_final = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_video_txt,
        "-i", voice_mix_wav,
        "-i", BGM_SOURCE,
        "-filter_complex",
        "[1:a]apad=pad_dur=4.5[padded_voice];"
        "[2:a]afade=t=in:ss=0:d=1.0,"
        "volume=enable='between(t,0,37.5)':volume=-26dB:eval=frame,"
        "volume=enable='gte(t,37.5)':volume=-15dB:eval=frame,"
        "afade=t=out:st=39.5:d=2.0[bgm_curved];"
        "[padded_voice][bgm_curved]amix=inputs=2:duration=first:dropout_transition=2,"
        "loudnorm=I=-16:TP=-1.5:LRA=11[out_audio]",
        "-map", "0:v", "-map", "[out_audio]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", "41.50",
        output_video
    ]
    subprocess.run(cmd_final, check=True)
    
    # Copiar também para a raiz do workspace
    shutil.copy2(output_video, os.path.join(BASE_DIR, "reel_sonia_limites_final.mp4"))
    print(f"Vídeo final renderizado v2 salvo em: {output_video}")

def atualizar_legendas_srt_v2():
    print("5. Atualizando reel_sonia_legendas.srt com os novos tempos...")
    srt_content = """1
00:00:00,000 --> 00:00:03,200
Na minha época, criança assim precisava era de limites.

2
00:00:03,200 --> 00:00:06,530
Quantas vezes você já ouviu essa frase?

3
00:00:06,530 --> 00:00:09,500
Mas será que todo comportamento interpretado como desobediência...

4
00:00:09,500 --> 00:00:12,640
...é realmente falta de limites?

5
00:00:12,640 --> 00:00:16,800
Algumas crianças encontram dificuldades para compreender ou expressar o que desejam...

6
00:00:16,800 --> 00:00:21,080
...e essa dificuldade pode provocar frustração.

7
00:00:21,080 --> 00:00:25,000
Isso não significa que toda crise esteja relacionada à linguagem.

8
00:00:25,000 --> 00:00:29,050
Significa que precisamos compreender antes de julgar.

9
00:00:29,050 --> 00:00:35,320
E você, acha que muitos adultos confundem dificuldades de comunicação com falta de educação?

10
00:00:35,320 --> 00:00:41,500
Conte sua opinião nos comentários.
"""
    for dest in [
        os.path.join(PUBLICACAO_DIR, "reel_sonia_legendas.srt"),
        os.path.join(BASE_DIR, "reel_sonia_legendas.srt")
    ]:
        with open(dest, "w", encoding="utf-8") as f:
            f.write(srt_content.strip() + "\n")
            
    print("Legendas SRT sincronizadas atualizadas com sucesso!")

if __name__ == "__main__":
    gerar_quadros_visuais_v2()
    renderizar_clipes_v2()
    mixar_audio_e_video_v2()
    atualizar_legendas_srt_v2()
    print("\nADAPTAÇÃO DA NOVA NARRAÇÃO CONCLUÍDA COM SUCESSO!")
