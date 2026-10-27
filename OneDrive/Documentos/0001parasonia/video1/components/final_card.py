# -*- coding: utf-8 -*-
"""
Componente do Card Final de Identificação Profissional
Sônia Torres — Fonoaudióloga — Rio de Janeiro / RJ
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

# Paleta Oficial Sônia Torres
PURPLE_MAIN = (109, 59, 147)    # #6D3B93
PURPLE_DARK = (44, 18, 64)       # #2C1240
LAVENDER    = (232, 220, 241)   # #E8DCF1
GOLD_ACCENT = (200, 169, 106)   # #C8A96A
BG_CREAM    = (251, 250, 247)   # #FBFAF7
WHITE       = (255, 255, 255)
GRAY_TEXT   = (90, 85, 95)

FONT_PATH = os.path.join("assets", "fonts", "PlusJakartaSans-Variable.ttf")

def generate_final_card(output_path="assets/images/scene_05_card.png"):
    img = Image.new("RGB", (W, H), BG_CREAM)
    draw = ImageDraw.Draw(img)

    # Elementos decorativos suaves e elegantes
    # Moldura sutil interna
    margin = 70
    draw.rounded_rectangle(
        [margin, margin + 80, W - margin, H - margin - 80],
        radius=40,
        outline=LAVENDER,
        width=3
    )

    # Detalhe superior dourado discreto
    draw.line([(W // 2 - 60, 480), (W // 2 + 60, 480)], fill=GOLD_ACCENT, width=4)

    # Tipografias
    font_badge = ImageFont.truetype(FONT_PATH, 32)
    font_name = ImageFont.truetype(FONT_PATH, 74)
    font_role = ImageFont.truetype(FONT_PATH, 42)
    font_city = ImageFont.truetype(FONT_PATH, 36)
    font_site = ImageFont.truetype(FONT_PATH, 44)
    font_phone = ImageFont.truetype(FONT_PATH, 42)

    # Badge ou chamada superior
    badge_text = "DESENVOLVIMENTO INFANTIL & LINGUAGEM"
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox_b[2] - bbox_b[0]
    draw.text(((W - bw) // 2, 530), badge_text, font=font_badge, fill=GOLD_ACCENT)

    # Nome da Profissional
    name_text = "SÔNIA TORRES"
    bbox_n = draw.textbbox((0, 0), name_text, font=font_name)
    nw = bbox_n[2] - bbox_n[0]
    draw.text(((W - nw) // 2, 630), name_text, font=font_name, fill=PURPLE_DARK)

    # Profissão
    role_text = "Fonoaudióloga"
    bbox_r = draw.textbbox((0, 0), role_text, font=font_role)
    rw = bbox_r[2] - bbox_r[0]
    draw.text(((W - rw) // 2, 735), role_text, font=font_role, fill=PURPLE_MAIN)

    # Cidade
    city_text = "Rio de Janeiro — RJ"
    bbox_c = draw.textbbox((0, 0), city_text, font=font_city)
    cw = bbox_c[2] - bbox_c[0]
    draw.text(((W - cw) // 2, 805), city_text, font=font_city, fill=GRAY_TEXT)

    # Linha divisória sutil
    draw.line([(W // 2 - 120, 920), (W // 2 + 120, 920)], fill=LAVENDER, width=2)

    # Card central de contato
    card_top = 980
    card_bot = 1260
    card_left = 160
    card_right = W - 160
    draw.rounded_rectangle(
        [card_left, card_top, card_right, card_bot],
        radius=28,
        fill=WHITE,
        outline=LAVENDER,
        width=2
    )

    # Site
    site_label = "Acesse o site oficial:"
    font_lbl = ImageFont.truetype(FONT_PATH, 26)
    bbox_sl = draw.textbbox((0, 0), site_label, font=font_lbl)
    draw.text(((W - (bbox_sl[2] - bbox_sl[0])) // 2, card_top + 35), site_label, font=font_lbl, fill=GRAY_TEXT)

    site_text = "sonia.fonosuite.com"
    bbox_s = draw.textbbox((0, 0), site_text, font=font_site)
    sw = bbox_s[2] - bbox_s[0]
    draw.text(((W - sw) // 2, card_top + 75), site_text, font=font_site, fill=PURPLE_MAIN)

    # Linha interna
    draw.line([(card_left + 60, card_top + 145), (card_right - 60, card_top + 145)], fill=LAVENDER, width=1)

    # Telefone WhatsApp
    phone_label = "Orientações e Atendimento:"
    bbox_pl = draw.textbbox((0, 0), phone_label, font=font_lbl)
    draw.text(((W - (bbox_pl[2] - bbox_pl[0])) // 2, card_top + 165), phone_label, font=font_lbl, fill=GRAY_TEXT)

    phone_text = "(21) 97748-6801"
    bbox_p = draw.textbbox((0, 0), phone_text, font=font_phone)
    pw = bbox_p[2] - bbox_p[0]
    draw.text(((W - pw) // 2, card_top + 205), phone_text, font=font_phone, fill=PURPLE_DARK)

    # Mensagem acolhedora de encerramento
    footer_text = "Cuidar da comunicação é cuidar do futuro."
    font_foot = ImageFont.truetype(FONT_PATH, 30)
    bbox_f = draw.textbbox((0, 0), footer_text, font=font_foot)
    fw = bbox_f[2] - bbox_f[0]
    draw.text(((W - fw) // 2, 1370), footer_text, font=font_foot, fill=PURPLE_MAIN)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Card final gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    generate_final_card()
