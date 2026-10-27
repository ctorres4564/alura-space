# -*- coding: utf-8 -*-
"""
Script de Geração da Capa Oficial do Reel
Título: "SEU FILHO PODE ESTAR FALANDO SEM PALAVRAS."
Formato: 1080 x 1920 px (9:16) com enquadramento otimizado para o feed (1080 x 1080 px central)
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FONT_PATH = os.path.join("assets", "fonts", "PlusJakartaSans-Variable.ttf")
BASE_IMG_PATH = os.path.join("assets", "images", "capa_base.jpg")
OUTPUT_PATH = "capa_reel_sonia.png"

# Cores
PURPLE_MAIN = (109, 59, 147)    # #6D3B93
PURPLE_DARK = (44, 18, 64)       # #2C1240
LAVENDER    = (232, 220, 241)   # #E8DCF1
GOLD_ACCENT = (200, 169, 106)   # #C8A96A
WHITE       = (255, 255, 255)
SHADOW      = (20, 10, 30, 180)

def gerar_capa():
    img = Image.open(BASE_IMG_PATH).convert("RGBA")
    
    # Criar camada de overlay para escurecimento suave superior (garantindo contraste do título)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_overlay = ImageDraw.Draw(overlay)

    # Gradiente escuro no terço superior para contraste perfeito
    for y in range(0, 680):
        alpha = int(140 * (1.0 - (y / 680.0)**1.2))
        d_overlay.line([(0, y), (W, y)], fill=(25, 10, 35, alpha))

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Fontes
    font_badge = ImageFont.truetype(FONT_PATH, 28)
    font_title = ImageFont.truetype(FONT_PATH, 66)
    font_author = ImageFont.truetype(FONT_PATH, 32)

    # 1. Badge Superior
    badge_text = "COMUNICAÇÃO INFANTIL"
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    
    badge_x = (W - bw) // 2
    badge_y = 170
    
    # Pílula de fundo do badge
    draw.rounded_rectangle(
        [badge_x - 24, badge_y - 8, badge_x + bw + 24, badge_y + bh + 12],
        radius=20,
        fill=(44, 18, 64, 200),
        outline=GOLD_ACCENT,
        width=2
    )
    draw.text((badge_x, badge_y), badge_text, font=font_badge, fill=GOLD_ACCENT)

    # 2. Título Principal em 3 linhas de alto impacto
    # Linha 1: "SEU FILHO PODE"
    # Linha 2: "ESTAR FALANDO"
    # Linha 3: "SEM PALAVRAS."
    linhas = [
        ("SEU FILHO PODE", WHITE),
        ("ESTAR FALANDO", LAVENDER),
        ("SEM PALAVRAS.", GOLD_ACCENT)
    ]
    
    cur_y = 255
    for texto, cor in linhas:
        bbox = draw.textbbox((0, 0), texto, font=font_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = (W - tw) // 2
        
        # Sombra projetada para alta legibilidade
        for sx, sy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3), (3, 3)]:
            draw.text((tx + sx, cur_y + sy), texto, font=font_title, fill=PURPLE_DARK)
        
        draw.text((tx, cur_y), texto, font=font_title, fill=cor)
        cur_y += th + 28

    # 3. Assinatura discreta no rodapé seguro
    author_text = "SÔNIA TORRES • FONOAUDIÓLOGA"
    bbox_a = draw.textbbox((0, 0), author_text, font=font_author)
    aw = bbox_a[2] - bbox_a[0]
    ah = bbox_a[3] - bbox_a[1]
    ax = (W - aw) // 2
    ay = 1780
    
    draw.rounded_rectangle(
        [ax - 20, ay - 8, ax + aw + 20, ay + ah + 10],
        radius=16,
        fill=(44, 18, 64, 210),
        outline=LAVENDER,
        width=1
    )
    draw.text((ax, ay), author_text, font=font_author, fill=WHITE)

    # Converter para RGB e salvar
    final_img = img.convert("RGB")
    final_img.save(OUTPUT_PATH, quality=95)
    print(f"Capa do Reel salva com sucesso em: {OUTPUT_PATH}")

if __name__ == "__main__":
    gerar_capa()
