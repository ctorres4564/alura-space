# -*- coding: utf-8 -*-
"""
Script Completo de Renderização e Montagem - Reel Sônia Torres
"Essa criança não precisa de fono. Precisa é de limites!"

Gera:
1. Imagens com lettering, safe-area e acabamento profissional (Cenas 1 a 6 e Capa)
2. Clipes com movimento de câmera cinematográfico (Ken Burns push/pan) a 1080x1920 30fps
3. Efeito sonoro de impacto discreto na Cena 1
4. Mixagem de voz, trilha com ducking e normalização EBU R128 (-16 LUFS)
5. Arquivo final reel_sonia_limites_final.mp4 (30s)
6. Capa vertical reel_sonia_capa.png
7. Arquivo de legendas reel_sonia_legendas.srt
8. Arquivo de postagem reel_sonia_legenda.txt
"""

import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from mutagen.mp3 import MP3

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\1MATERIASIDASONIA\01reels_novos"
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
FONT_GEORGIA = r"C:\Windows\Fonts\georgia.ttf"
FONT_SEGOE_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEGOE = r"C:\Windows\Fonts\segoeui.ttf"

# Paleta de Cores Institucional
COR_DOURADO = (212, 175, 55, 255)       # #D4AF37
COR_DOURADO_CLARO = (235, 205, 110, 255) # #EBCD6E
COR_ROXO_FUNDO = (20, 10, 32, 255)       # #140A20
COR_ROXO_LILAS = (157, 114, 178, 255)    # #9D72B2
COR_BRANCO = (255, 255, 255, 255)
COR_OFFWHITE = (248, 246, 242, 255)

def criar_caixa_texto(draw, lines, font, center_y, box_opacity=0.55, text_color=COR_BRANCO, highlight_word=None, highlight_color=COR_DOURADO):
    """
    Desenha caixa translúcida com cantos arredondados e texto centralizado dentro da safe area.
    """
    line_height = int(font.size * 1.32)
    total_h = len(lines) * line_height
    start_y = center_y - (total_h // 2)
    
    max_line_w = 0
    for line in lines:
        bbox = font.getbbox(line)
        max_line_w = max(max_line_w, bbox[2] - bbox[0])
        
    padding_x = 32
    padding_y = 20
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
        
        # Desenha sombra suave do texto
        draw.text((lx + 2, curr_y + 2), line, font=font, fill=(0, 0, 0, 200))
        
        # Se houver palavra destacada na linha
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

def gerar_quadros_visuais():
    print("1. Gerando quadros visuais tratados...")
    
    # -----------------------------
    # CENA 1: Dois estados de texto
    # -----------------------------
    base1 = Image.open(os.path.join(IMG_DIR, "cena1_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    font_cena1 = ImageFont.truetype(FONT_POPPINS_BOLD, 46)
    
    # 1A: “ESSA CRIANÇA NÃO PRECISA DE FONO!”
    q1a = base1.copy()
    overlay = Image.new("RGBA", q1a.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["“ESSA CRIANÇA NÃO", "PRECISA DE FONO!”"], font_cena1, center_y=760, box_opacity=0.60, highlight_word="FONO!”", highlight_color=COR_DOURADO)
    q1a = Image.alpha_composite(q1a, overlay).convert("RGB")
    q1a.save(os.path.join(IMG_DIR, "cena1_fase_a.png"))
    
    # 1B: “PRECISA É DE LIMITES!”
    q1b = base1.copy()
    overlay = Image.new("RGBA", q1b.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["“PRECISA É DE LIMITES!”"], font_cena1, center_y=760, box_opacity=0.65, highlight_word="LIMITES!”", highlight_color=COR_DOURADO)
    q1b = Image.alpha_composite(q1b, overlay).convert("RGB")
    q1b.save(os.path.join(IMG_DIR, "cena1_fase_b.png"))
    
    # -----------------------------
    # CENA 2: Três estados de texto
    # -----------------------------
    base2 = Image.open(os.path.join(IMG_DIR, "cena2_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    font_cena2 = ImageFont.truetype(FONT_POPPINS_BOLD, 48)
    
    # 2A: “ELA TENTA FALAR.”
    q2a = base2.copy()
    overlay = Image.new("RGBA", q2a.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["ELA TENTA FALAR."], font_cena2, center_y=760, box_opacity=0.55)
    Image.alpha_composite(q2a, overlay).convert("RGB").save(os.path.join(IMG_DIR, "cena2_fase_a.png"))
    
    # 2B: “NÃO CONSEGUE SE EXPLICAR.”
    q2b = base2.copy()
    overlay = Image.new("RGBA", q2b.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["NÃO CONSEGUE SE EXPLICAR."], font_cena2, center_y=760, box_opacity=0.58)
    Image.alpha_composite(q2b, overlay).convert("RGB").save(os.path.join(IMG_DIR, "cena2_fase_b.png"))
    
    # 2C: “E FICA FRUSTRADA.”
    q2c = base2.copy()
    overlay = Image.new("RGBA", q2c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["E FICA FRUSTRADA."], font_cena2, center_y=760, box_opacity=0.62, highlight_word="FRUSTRADA.", highlight_color=COR_DOURADO)
    Image.alpha_composite(q2c, overlay).convert("RGB").save(os.path.join(IMG_DIR, "cena2_fase_c.png"))
    
    # -----------------------------
    # CENA 3: A Virada
    # -----------------------------
    base3 = Image.open(os.path.join(IMG_DIR, "cena3_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    font_cena3 = ImageFont.truetype(FONT_POPPINS_BOLD, 46)
    q3 = base3.copy()
    overlay = Image.new("RGBA", q3.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["MAS E SE NÃO FOR", "FALTA DE LIMITES?"], font_cena3, center_y=780, box_opacity=0.60, highlight_word="LIMITES?", highlight_color=COR_DOURADO)
    Image.alpha_composite(q3, overlay).convert("RGB").save(os.path.join(IMG_DIR, "cena3_render.png"))
    
    # -----------------------------
    # CENA 4: A Compreensão
    # -----------------------------
    base4 = Image.open(os.path.join(IMG_DIR, "cena4_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    font_cena4 = ImageFont.truetype(FONT_POPPINS_BOLD, 44)
    q4 = base4.copy()
    overlay = Image.new("RGBA", q4.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    criar_caixa_texto(d, ["DIFICULDADES DE COMUNICAÇÃO", "PODEM GERAR FRUSTRAÇÃO."], font_cena4, center_y=760, box_opacity=0.60, highlight_word="FRUSTRAÇÃO.", highlight_color=COR_DOURADO)
    Image.alpha_composite(q4, overlay).convert("RGB").save(os.path.join(IMG_DIR, "cena4_render.png"))
    
    # -----------------------------
    # CENA 5: Frase de Impacto
    # -----------------------------
    img5 = Image.new("RGBA", (1080, 1920), (12, 6, 18, 255))
    d5 = ImageDraw.Draw(img5)
    # Moldura sutil elegante
    d5.rectangle([40, 60, 1040, 1860], outline=(212, 175, 55, 60), width=2)
    d5.rectangle([52, 72, 1028, 1848], outline=(157, 114, 178, 40), width=1)
    
    font_f1 = ImageFont.truetype(FONT_GEORGIA_BOLD, 52)
    font_f2 = ImageFont.truetype(FONT_GEORGIA_BOLD, 52)
    
    t_f1 = ["NEM TODA CRISE", "É BIRRA."]
    t_f2 = ["NEM TODA DIFICULDADE", "É DESOBEDIÊNCIA."]
    
    curr_y = 740
    for l in t_f1:
        bbox = font_f1.getbbox(l)
        w = bbox[2] - bbox[0]
        d5.text(((1080 - w) // 2 + 2, curr_y + 2), l, font=font_f1, fill=(0, 0, 0, 220))
        d5.text(((1080 - w) // 2, curr_y), l, font=font_f1, fill=COR_BRANCO)
        curr_y += 76
        
    curr_y += 40
    # Divisor dourado sutil
    d5.line([(440, curr_y), (640, curr_y)], fill=(212, 175, 55, 180), width=3)
    curr_y += 60
    
    for l in t_f2:
        bbox = font_f2.getbbox(l)
        w = bbox[2] - bbox[0]
        d5.text(((1080 - w) // 2 + 2, curr_y + 2), l, font=font_f2, fill=(0, 0, 0, 220))
        d5.text(((1080 - w) // 2, curr_y), l, font=font_f2, fill=COR_DOURADO)
        curr_y += 76
        
    img5.convert("RGB").save(os.path.join(IMG_DIR, "cena5_render.png"))
    
    # -----------------------------
    # CENA 6: Card Final Institucional Sônia Torres
    # -----------------------------
    # Base com blur e vinheta da cena 4
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
    # Sombra do card
    d6.rounded_rectangle([card_x0 - 4, card_y0 + 8, card_x1 + 4, card_y1 + 18], radius=32, fill=(0, 0, 0, 120))
    # Corpo do card em roxo escuro acetinado com borda dourada
    d6.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=30, fill=(24, 12, 36, 248), outline=COR_DOURADO, width=3)
    
    font_c6_title = ImageFont.truetype(FONT_POPPINS_BOLD, 38)
    font_c6_cta = ImageFont.truetype(FONT_POPPINS_BOLD, 34)
    font_c6_name = ImageFont.truetype(FONT_GEORGIA_BOLD, 42)
    font_c6_sub = ImageFont.truetype(FONT_POPPINS_BOLD, 24)
    font_c6_info = ImageFont.truetype(FONT_SEGOE, 26)
    font_c6_link = ImageFont.truetype(FONT_POPPINS_BOLD, 28)
    
    cy = card_y0 + 55
    # Pergunta Principal
    p_lines = ["FALTA DE LIMITES OU", "DIFICULDADE DE COMUNICAÇÃO?"]
    for l in p_lines:
        bw = font_c6_title.getbbox(l)[2] - font_c6_title.getbbox(l)[0]
        d6.text(((1080 - bw) // 2, cy), l, font=font_c6_title, fill=COR_BRANCO)
        cy += 48
        
    cy += 14
    # Chamada CTA
    cta_txt = "O QUE VOCÊ PENSA? COMENTE!"
    cw = font_c6_cta.getbbox(cta_txt)[2] - font_c6_cta.getbbox(cta_txt)[0]
    d6.text(((1080 - cw) // 2, cy), cta_txt, font=font_c6_cta, fill=COR_DOURADO_CLARO)
    
    cy += 64
    # Divisor dourado elegante
    d6.line([(card_x0 + 80, cy), (card_x1 - 80, cy)], fill=(212, 175, 55, 140), width=2)
    
    cy += 36
    # Nome Sônia Torres
    nw = font_c6_name.getbbox("SÔNIA TORRES")[2] - font_c6_name.getbbox("SÔNIA TORRES")[0]
    d6.text(((1080 - nw) // 2, cy), "SÔNIA TORRES", font=font_c6_name, fill=COR_DOURADO)
    
    cy += 50
    # Fonoaudióloga
    sw = font_c6_sub.getbbox("FONOAUDIÓLOGA")[2] - font_c6_sub.getbbox("FONOAUDIÓLOGA")[0]
    d6.text(((1080 - sw) // 2, cy), "FONOAUDIÓLOGA", font=font_c6_sub, fill=COR_ROXO_LILAS)
    
    cy += 46
    # Endereço
    end1 = "Av. Vicente de Carvalho, 909 — Sala 413"
    end2 = "Vicente de Carvalho • Rio de Janeiro — RJ"
    for l in [end1, end2]:
        bw = font_c6_info.getbbox(l)[2] - font_c6_info.getbbox(l)[0]
        d6.text(((1080 - bw) // 2, cy), l, font=font_c6_info, fill=COR_OFFWHITE)
        cy += 34
        
    cy += 8
    # Telefone
    tel = "Telefone: (21) 97748-6801"
    tw = font_c6_info.getbbox(tel)[2] - font_c6_info.getbbox(tel)[0]
    d6.text(((1080 - tw) // 2, cy), tel, font=font_c6_info, fill=COR_DOURADO_CLARO)
    
    cy += 44
    # Site
    site = "sonia.fonosuite.com"
    siw = font_c6_link.getbbox(site)[2] - font_c6_link.getbbox(site)[0]
    d6.text(((1080 - siw) // 2, cy), site, font=font_c6_link, fill=COR_ROXO_LILAS)
    
    comp6.convert("RGB").save(os.path.join(IMG_DIR, "cena6_render.png"))
    
    # -----------------------------
    # CAPA DO REEL (1080x1920)
    # -----------------------------
    print("2. Gerando reel_sonia_capa.png...")
    capa_base = Image.open(os.path.join(IMG_DIR, "cena1_base.jpg")).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    capa_dimmer = Image.new("RGBA", (1080, 1920), (12, 6, 20, 100))
    capa_comp = Image.alpha_composite(capa_base, capa_dimmer)
    
    d_capa = ImageDraw.Draw(capa_comp)
    # Card central translúcido para a capa
    cc_w = 980
    cc_h = 480
    cc_x0 = (1080 - cc_w) // 2
    cc_y0 = (1920 - cc_h) // 2 - 80
    cc_x1 = cc_x0 + cc_w
    cc_y1 = cc_y0 + cc_h
    
    d_capa.rounded_rectangle([cc_x0 - 4, cc_y0 + 8, cc_x1 + 4, cc_y1 + 16], radius=28, fill=(0, 0, 0, 130))
    d_capa.rounded_rectangle([cc_x0, cc_y0, cc_x1, cc_y1], radius=26, fill=(18, 9, 28, 235), outline=COR_DOURADO, width=3)
    
    font_capa_t = ImageFont.truetype(FONT_POPPINS_BOLD, 42)
    font_capa_sub = ImageFont.truetype(FONT_GEORGIA_BOLD, 32)
    
    cy_capa = cc_y0 + 75
    capa_lines = ["FALTA DE LIMITES OU", "DIFICULDADE DE COMUNICAÇÃO?"]
    for l in capa_lines:
        w = font_capa_t.getbbox(l)[2] - font_capa_t.getbbox(l)[0]
        d_capa.text(((1080 - w) // 2, cy_capa), l, font=font_capa_t, fill=COR_BRANCO)
        cy_capa += 56
        
    cy_capa += 24
    d_capa.line([(cc_x0 + 120, cy_capa), (cc_x1 - 120, cy_capa)], fill=(212, 175, 55, 160), width=2)
    cy_capa += 45
    
    sub_capa = "SÔNIA TORRES | FONOAUDIÓLOGA"
    w_sub = font_capa_sub.getbbox(sub_capa)[2] - font_capa_sub.getbbox(sub_capa)[0]
    d_capa.text(((1080 - w_sub) // 2, cy_capa), sub_capa, font=font_capa_sub, fill=COR_DOURADO)
    
    capa_final_path = os.path.join(PUBLICACAO_DIR, "reel_sonia_capa.png")
    capa_comp.convert("RGB").save(capa_final_path)
    print(f"Capa gerada com sucesso: {capa_final_path}")

def gerar_clipes_animados():
    print("3. Renderizando clipes de vídeo com interpolação de movimento Ken Burns...")
    
    # Cena 1: 4.50s total (Fase A: 2.0s, Fase B: 2.5s)
    # Slow push-in suave
    clip1a = os.path.join(CLIP_DIR, "c1a.mp4")
    cmd1a = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena1_fase_a.png"),
        "-t", "2.000",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0008,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=60:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip1a
    ]
    subprocess.run(cmd1a, check=True)
    
    clip1b = os.path.join(CLIP_DIR, "c1b.mp4")
    cmd1b = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena1_fase_b.png"),
        "-t", "2.500",
        "-vf", "scale=1188:2112,zoompan=z='min(1.03+0.0008*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=75:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip1b
    ]
    subprocess.run(cmd1b, check=True)
    
    # Cena 2: 5.30s total (2A: 1.70s, 2B: 1.70s, 2C: 1.90s)
    # Pan suave em direção ao gesto da criança e mãe
    clip2a = os.path.join(CLIP_DIR, "c2a.mp4")
    cmd2a = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena2_fase_a.png"),
        "-t", "1.700",
        "-vf", "scale=1188:2112,zoompan=z='1.04':x='iw*0.04+on*0.5':y='ih*0.04':d=51:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip2a
    ]
    subprocess.run(cmd2a, check=True)
    
    clip2b = os.path.join(CLIP_DIR, "c2b.mp4")
    cmd2b = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena2_fase_b.png"),
        "-t", "1.700",
        "-vf", "scale=1188:2112,zoompan=z='1.04':x='iw*0.06+on*0.5':y='ih*0.04':d=51:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip2b
    ]
    subprocess.run(cmd2b, check=True)
    
    clip2c = os.path.join(CLIP_DIR, "c2c.mp4")
    cmd2c = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena2_fase_c.png"),
        "-t", "1.900",
        "-vf", "scale=1188:2112,zoompan=z='1.04':x='iw*0.08+on*0.5':y='ih*0.04':d=57:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip2c
    ]
    subprocess.run(cmd2c, check=True)
    
    # Cena 3: 4.20s (áudio 3.38s + pausa dramática de 0.82s)
    # Slow close-in no olhar emotivo
    clip3 = os.path.join(CLIP_DIR, "c3.mp4")
    cmd3 = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena3_render.png"),
        "-t", "4.200",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0006,1.06)':x='iw/2-(iw/zoom/2)':y='ih*0.45-(ih/zoom*0.45)':d=126:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip3
    ]
    subprocess.run(cmd3, check=True)
    
    # Cena 4: 5.80s (áudio 5.59s + respiro de 0.21s)
    # Slow tracking mantendo conexão mãe-filha
    clip4 = os.path.join(CLIP_DIR, "c4.mp4")
    cmd4 = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena4_render.png"),
        "-t", "5.800",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0005,1.05)':x='iw*0.05+on*0.3':y='ih/2-(ih/zoom/2)':d=174:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip4
    ]
    subprocess.run(cmd4, check=True)
    
    # Cena 5: 4.20s (áudio 3.34s + pausa solene de 0.86s)
    # Zoom suave e solene
    clip5 = os.path.join(CLIP_DIR, "c5.mp4")
    cmd5 = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena5_render.png"),
        "-t", "4.200",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0004,1.03)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=126:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip5
    ]
    subprocess.run(cmd5, check=True)
    
    # Cena 6: 6.00s (Card Final Institucional)
    clip6 = os.path.join(CLIP_DIR, "c6.mp4")
    cmd6 = [
        FFMPEG, "-y", "-loop", "1", "-i", os.path.join(IMG_DIR, "cena6_render.png"),
        "-t", "6.000",
        "-vf", "scale=1188:2112,zoompan=z='min(zoom+0.0002,1.02)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=180:s=1080x1920:fps=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-r", "30",
        clip6
    ]
    subprocess.run(cmd6, check=True)
    
    # Lista de concatenação dos clipes
    clip_list = [clip1a, clip1b, clip2a, clip2b, clip2c, clip3, clip4, clip5, clip6]
    concat_txt = os.path.join(CLIP_DIR, "concat_video.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clip_list:
            f.write(f"file '{c.replace('\\', '/')}'\n")
            
    print("Todos os clipes animados foram renderizados com sucesso!")

def mixar_audio_e_video():
    print("4. Montando áudio contínuo e sincronizando com trilha sonora...")
    
    # Durações dos segmentos visuais:
    # C1: 4.50s (voz dura 4.42s)
    # C2: 5.30s (voz dura 5.18s)
    # C3: 4.20s (voz dura 3.38s + pausa 0.82s)
    # C4: 5.80s (voz dura 5.59s + pausa 0.21s)
    # C5: 4.20s (voz dura 3.34s + pausa 0.86s)
    # C6: 6.00s (sem voz)
    # Total Video = 30.00 segundos
    
    # Gerando áudio de impacto sutil para a Cena 1 (0.0s)
    impact_wav = os.path.join(AUDIO_DIR, "impacto_cena1.wav")
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", "sine=frequency=55:duration=0.7",
        "-af", "afade=t=out:st=0.1:d=0.6,volume=0.45",
        impact_wav
    ], check=True)
    
    # Criamos os tempos exatos com atraso (delay) para cada faixa de voz
    # c1: 0ms
    # c2: 4500ms
    # c3: 9800ms
    # c4: 14000ms
    # c5: 19800ms
    
    a1 = os.path.join(AUDIO_DIR, "audio_1.mp3")
    a2 = os.path.join(AUDIO_DIR, "audio_2.mp3")
    a3 = os.path.join(AUDIO_DIR, "audio_3.mp3")
    a4 = os.path.join(AUDIO_DIR, "audio_4.mp3")
    a5 = os.path.join(AUDIO_DIR, "audio_5.mp3")
    
    voice_mix_wav = os.path.join(AUDIO_DIR, "narracao_mixada.wav")
    
    cmd_voice_mix = [
        FFMPEG, "-y",
        "-i", a1,
        "-i", a2,
        "-i", a3,
        "-i", a4,
        "-i", a5,
        "-i", impact_wav,
        "-filter_complex",
        "[0:a]adelay=0|0[v1];"
        "[1:a]adelay=4500|4500[v2];"
        "[2:a]adelay=9800|9800[v3];"
        "[3:a]adelay=14000|14000[v4];"
        "[4:a]adelay=19800|19800[v5];"
        "[5:a]adelay=50|50[imp];"
        "[v1][v2][v3][v4][v5][imp]amix=inputs=6:duration=longest:dropout_transition=0,"
        "loudnorm=I=-16:TP=-1.5:LRA=11[outv]",
        "-map", "[outv]",
        voice_mix_wav
    ]
    subprocess.run(cmd_voice_mix, check=True)
    
    print("5. Renderizando vídeo final com trilha sonora e normalização...")
    concat_video_txt = os.path.join(CLIP_DIR, "concat_video.txt")
    output_video = os.path.join(PUBLICACAO_DIR, "reel_sonia_limites_final.mp4")
    
    # Mixagem com trilha de fundo:
    # 0s a 24.0s: música em segundo plano suave (-26 dB)
    # 24.0s a 28.0s: música em destaque suave (-15 dB) durante o card final
    # 28.0s a 30.0s: fade-out suave
    cmd_final = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_video_txt,
        "-i", voice_mix_wav,
        "-i", BGM_SOURCE,
        "-filter_complex",
        "[1:a]apad=pad_dur=6.5[padded_voice];"
        "[2:a]afade=t=in:ss=0:d=1.0,"
        "volume=enable='between(t,0,24.0)':volume=-26dB:eval=frame,"
        "volume=enable='gte(t,24.0)':volume=-15dB:eval=frame,"
        "afade=t=out:st=28.0:d=2.0[bgm_curved];"
        "[padded_voice][bgm_curved]amix=inputs=2:duration=first:dropout_transition=2,"
        "loudnorm=I=-16:TP=-1.5:LRA=11[out_audio]",
        "-map", "0:v", "-map", "[out_audio]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", "30.00",
        output_video
    ]
    subprocess.run(cmd_final, check=True)
    print(f"Vídeo final renderizado com sucesso: {output_video}")

def gerar_legendas_srt_e_txt():
    print("6. Gerando arquivos de legenda (SRT e TXT para publicação)...")
    
    # 1. SRT sincronizado
    srt_content = """1
00:00:00,000 --> 00:00:02,000
Essa criança não precisa de fono!

2
00:00:02,000 --> 00:00:04,450
Precisa é de limites!

3
00:00:04,500 --> 00:00:07,000
Ela tenta dizer o que quer...

4
00:00:07,000 --> 00:00:09,700
...mas nem sempre consegue se fazer entender.

5
00:00:09,800 --> 00:00:13,800
E se o problema não for falta de limites?

6
00:00:14,000 --> 00:00:19,600
Dificuldades para compreender ou se expressar também podem gerar frustração.

7
00:00:19,800 --> 00:00:23,800
Antes de julgar, procure compreender.

8
00:00:24,000 --> 00:00:30,000
Falta de limites ou dificuldade de comunicação? O que você pensa? Comente!
"""
    srt_path = os.path.join(PUBLICACAO_DIR, "reel_sonia_legendas.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content.strip() + "\n")
        
    # 2. Legenda de postagem (TXT)
    legenda_txt = """“Na minha época, criança assim precisava era de limites!”

Quantas vezes você já ouviu essa frase?

Mas será que todo comportamento interpretado como desobediência é realmente falta de limites?

Algumas crianças encontram dificuldades para compreender ou expressar o que desejam. E essa dificuldade pode provocar frustração.

Isso não significa que toda crise esteja relacionada à linguagem. Significa que precisamos compreender antes de julgar.

E você? Acha que muitos adultos confundem dificuldades de comunicação com falta de educação?

Conte sua opinião nos comentários.

Sônia Torres | Fonoaudióloga
Telefone: (21) 97748-6801
sonia.fonosuite.com

#Fonoaudiologia #DesenvolvimentoInfantil #ComunicaçãoInfantil #EducaçãoInfantil #FalaInfantil
"""
    txt_path = os.path.join(PUBLICACAO_DIR, "reel_sonia_legenda.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(legenda_txt.strip() + "\n")
        
    print(f"Arquivos de legenda salvos em:\n - {srt_path}\n - {txt_path}")

if __name__ == "__main__":
    gerar_quadros_visuais()
    gerar_clipes_animados()
    mixar_audio_e_video()
    gerar_legendas_srt_e_txt()
    print("\nPRODUÇÃO COMPLETA CONCLUÍDA COM SUCESSO!")
