"""
Script de Produção Automatizada — Carrossel Instagram 4:5 (1080 x 1350 px)
Carrossel: "O que esperar da fala, por idade"
Cliente: Sônia Torres — Fonoaudióloga (CRFa 1-17701)

Gera:
1. Cópia e redimensionamento das fotos brutas para raw-photos/ (01 a 08)
2. Renderização de todos os 10 slides prontos para publicação em slides-finais/ (01 a 10)
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia"
CARROSSEL_DIR = os.path.join(BASE_DIR, "carrosseis", "carrossel-o-que-esperar-da-fala-por-idade")
RAW_DIR = os.path.join(CARROSSEL_DIR, "raw-photos")
FINAL_DIR = os.path.join(CARROSSEL_DIR, "slides-finais")
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "PlusJakartaSans-Variable.ttf")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

# Paleta oficial Sônia Torres
COLOR_DEEP_GREEN = (29, 56, 43)       # #1D382B
COLOR_OFF_WHITE = (250, 247, 242)     # #FAF7F2 (bege fundo)
COLOR_DARK_BEIGE = (234, 228, 216)    # #EAE4D8
COLOR_MEDIUM_GREEN = (68, 99, 75)     # #44634B
COLOR_LIGHT_GREEN_TINT = (241, 246, 242) # Fundo de cards suaves
COLOR_CARD_BORDER = (205, 219, 210)
COLOR_TEXT_MAIN = (32, 45, 38)        # Quase preto esverdeado legível
COLOR_TEXT_MUTED = (85, 95, 89)

# Fotos fotográficas geradas nesta sessão
BRAIN_DIR = r"C:\Users\Gamer\.gemini\antigravity-ide\brain\459fb140-62c0-43de-8bce-6741abb62109"
RAW_IMAGES_SOURCE = [
    ("01-capa.jpg", os.path.join(BRAIN_DIR, "slide01_capa_mao_bebe_1791244048601.jpg")),
    ("02-0-a-6-meses.jpg", os.path.join(BRAIN_DIR, "slide02_bebe_colo_1791244066847.jpg")),
    ("03-7-a-11-meses.jpg", os.path.join(BRAIN_DIR, "slide03_bebe_palminhas_1791244089220.jpg")),
    ("04-1-ano.jpg", os.path.join(BRAIN_DIR, "slide04_maozinhas_apontando_1791244113811.jpg")),
    ("05-1-ano-e-6-meses.jpg", os.path.join(BRAIN_DIR, "slide05_apontando_janela_1791244144851.jpg")),
    ("06-2-anos.jpg", os.path.join(BRAIN_DIR, "slide06_blocos_montar_1791244177977.jpg")),
    ("07-3-a-6-anos.jpg", os.path.join(BRAIN_DIR, "slide07_historia_livro_1791244211709.jpg")),
    ("08-observe-alertas.jpg", os.path.join(BRAIN_DIR, "slide08_observe_cuidado_1791244249781.jpg")),
]

def get_font(size, weight=400):
    """Carrega Plus Jakarta Sans com suporte a pesos de variável ou fontes nativas."""
    try:
        font = ImageFont.truetype(FONT_PATH, size)
        if hasattr(font, 'set_variation_by_axes'):
            font.set_variation_by_axes([weight])
        return font
    except Exception:
        # Fallbacks no Windows
        if weight >= 700 and os.path.exists(r"C:\Windows\Fonts\segoeuib.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", size)
        elif weight >= 500 and os.path.exists(r"C:\Windows\Fonts\seguisb.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\seguisb.ttf", size)
        elif os.path.exists(r"C:\Windows\Fonts\segoeui.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", size)
        return ImageFont.load_default()

def prepare_raw_photos():
    """Copia e ajusta fotos para proporção 4:5 (1080 x 1350) em raw-photos/"""
    target_w, target_h = 1080, 1350
    target_ratio = target_w / target_h
    for target_name, src_path in RAW_IMAGES_SOURCE:
        dest_path = os.path.join(RAW_DIR, target_name)
        if not os.path.exists(src_path):
            print(f"Aviso: fonte não encontrada {src_path}")
            continue
        img = Image.open(src_path).convert("RGB")
        img_ratio = img.width / img.height
        if img_ratio > target_ratio:
            new_w = int(img.height * target_ratio)
            left = (img.width - new_w) // 2
            img = img.crop((left, 0, left + new_w, img.height))
        else:
            new_h = int(img.width / target_ratio)
            top = (img.height - new_h) // 2
            img = img.crop((0, top, img.width, top + new_h))
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        img.save(dest_path, "JPEG", quality=95)
    print("Fotos brutas preparadas em raw-photos.")

def wrap_text_to_width(text, font, max_width, draw):
    """Quebra texto considerando a largura em pixels."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_pill_badge(draw, x, y, text, font, bg_color, text_color, px=20, py=8, radius=16, outline=None):
    """Desenha badge em formato de pílula."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x1, y1 = x, y
    x2 = x + tw + (px * 2)
    y2 = y + th + (py * 2) + 2
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg_color, outline=outline, width=1)
    text_y = y1 + py - bbox[1] + (th - (bbox[3] - bbox[1])) // 2
    draw.text((x1 + px, text_y), text, font=font, fill=text_color)
    return (x1, y1, x2, y2)

def draw_card_with_shadow(base_img, card_box, fill_color, radius=28, shadow_blur=10, shadow_alpha=40, outline_color=None):
    """Desenha card com cantos arredondados e sombra difusa elegante."""
    w, h = base_img.size
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    x1, y1, x2, y2 = card_box
    for s in range(shadow_blur, 0, -2):
        alpha = int(shadow_alpha * (s / shadow_blur))
        s_draw.rounded_rectangle(
            [x1 - s, y1 - s + 5, x2 + s, y2 + s + 5],
            radius=radius + s,
            fill=(0, 0, 0, alpha)
        )
    base_img.alpha_composite(shadow_layer)
    card_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card_layer)
    c_draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill_color, outline=outline_color, width=1)
    base_img.alpha_composite(card_layer)

def render_slide_01():
    """Slide 1 — Capa
    1080 x 1350 px.
    Mão de bebê recém-nascido no terço inferior, espaço negativo generoso no topo.
    Card em verde escuro profundo (#1D382B) perfeitamente na safe zone (y1=170, y2=660).
    """
    raw_path = os.path.join(RAW_DIR, "01-capa.jpg")
    img = Image.open(raw_path).convert("RGBA")

    # Gradiente sutil superior para conforto visual
    grad = Image.new("RGBA", (1080, 1350), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grad)
    for y in range(700):
        alpha = int(60 * (1.0 - (y / 700.0)))
        g_draw.line([(0, y), (1080, y)], fill=(29, 56, 43, alpha))
    img = Image.alpha_composite(img, grad)

    card_x1 = 70
    card_x2 = 1010
    card_y1 = 170
    card_y2 = 670

    card_fill = (29, 56, 43, 245)
    draw_card_with_shadow(img, (card_x1, card_y1, card_x2, card_y2), fill_color=card_fill, radius=32, outline_color=(234, 228, 216, 70))

    draw = ImageDraw.Draw(img)

    # Badge no topo do card
    font_badge = get_font(20, weight=700)
    draw_pill_badge(draw, card_x1 + 45, card_y1 + 42, "DESENVOLVIMENTO INFANTIL", font_badge,
                    bg_color=COLOR_DARK_BEIGE, text_color=COLOR_DEEP_GREEN, px=20, py=8)

    # Título principal
    font_title = get_font(56, weight=800)
    title_text = "O que esperar da fala, por idade"
    title_lines = wrap_text_to_width(title_text, font_title, max_width=card_x2 - card_x1 - 90, draw=draw)
    ty = card_y1 + 128
    for line in title_lines:
        draw.text((card_x1 + 45, ty), line, font=font_title, fill=COLOR_OFF_WHITE)
        ty += 70

    # Subtítulo explicativo
    font_sub = get_font(26, weight=500)
    sub_text = "Dos primeiros sons às historinhas completas: o que é esperado e quando vale observar mais de perto."
    sub_lines = wrap_text_to_width(sub_text, font_sub, max_width=card_x2 - card_x1 - 90, draw=draw)
    ty += 8
    for line in sub_lines:
        draw.text((card_x1 + 45, ty), line, font=font_sub, fill=COLOR_DARK_BEIGE)
        ty += 38

    # Indicador de swipe
    font_swipe = get_font(20, weight=700)
    swipe_text = "Arraste para o lado  →"
    sw_bbox = draw.textbbox((0, 0), swipe_text, font=font_swipe)
    sw_w = sw_bbox[2] - sw_bbox[0]
    draw_pill_badge(draw, card_x2 - sw_w - 75, card_y2 - 62, swipe_text, font_swipe,
                    bg_color=COLOR_DARK_BEIGE, text_color=COLOR_DEEP_GREEN, px=18, py=7, radius=14)

    # Assinatura de autoria no rodapé
    font_author = get_font(22, weight=700)
    auth_text = "Sônia Torres · Fonoaudióloga (CRFa 1-17701)"
    draw_pill_badge(draw, 70, 1220, auth_text, font_author,
                    bg_color=(29, 56, 43, 235), text_color=COLOR_OFF_WHITE, px=24, py=10, radius=18, outline=(234, 228, 216, 60))

    dest_path = os.path.join(FINAL_DIR, "01-capa.png")
    img.save(dest_path, "PNG")
    print("Slide 01 gerado.")

def render_content_slide(slide_num, raw_file_name, age_badge, title, bullets, tip_text=None, is_alert=False):
    """
    Renderiza os slides com fotografia (Slides 02 a 08).
    Card editorial semi-transparente claro com borda e sombra suave,
    posicionado de forma a respeitar a safe zone central (1080x1080)
    sem encobrir o gesto fotográfico principal.
    """
    raw_path = os.path.join(RAW_DIR, raw_file_name)
    img = Image.open(raw_path).convert("RGBA")

    card_x1 = 65
    card_x2 = 1015
    max_w = card_x2 - card_x1 - 80

    draw_temp = ImageDraw.Draw(img)
    font_badge = get_font(20, weight=700)
    font_title = get_font(44, weight=800)
    font_bullet = get_font(26, weight=500)
    font_tip = get_font(22, weight=600)
    font_page = get_font(18, weight=700)

    title_lines = wrap_text_to_width(title, font_title, max_w, draw_temp)
    wrapped_bullets = []
    for b in bullets:
        w_b = wrap_text_to_width(b, font_bullet, max_w - 28, draw_temp)
        wrapped_bullets.append(w_b)

    tip_lines = wrap_text_to_width(tip_text, font_tip, max_w - 20, draw_temp) if tip_text else []

    # Cálculo da altura do card
    card_h = 42 + 40 + (len(title_lines) * 56) + 24
    for wb in wrapped_bullets:
        card_h += (len(wb) * 36) + 16
    if tip_lines:
        card_h += 24 + (len(tip_lines) * 32) + 36
    card_h += 30

    # Posicionamento na parte superior/média (Safe Zone)
    card_y1 = 155
    card_y2 = card_y1 + card_h

    if is_alert:
        card_fill = (250, 247, 242, 248)
        border_color = (195, 95, 80, 180)
        badge_bg = (195, 75, 60)
        badge_fg = (255, 255, 255)
        title_color = (165, 45, 35)
    else:
        card_fill = (250, 247, 242, 248)
        border_color = (29, 56, 43, 90)
        badge_bg = COLOR_DEEP_GREEN
        badge_fg = COLOR_OFF_WHITE
        title_color = COLOR_DEEP_GREEN

    draw_card_with_shadow(img, (card_x1, card_y1, card_x2, card_y2), fill_color=card_fill,
                          radius=28, shadow_blur=10, shadow_alpha=35, outline_color=border_color)

    draw = ImageDraw.Draw(img)

    # Badge de Idade
    draw_pill_badge(draw, card_x1 + 40, card_y1 + 36, age_badge, font_badge,
                    bg_color=badge_bg, text_color=badge_fg, px=18, py=7, radius=14)

    # Indicador de slide (ex: 02 / 10)
    page_text = f"{slide_num:02d} / 10"
    p_bbox = draw.textbbox((0, 0), page_text, font=font_page)
    p_w = p_bbox[2] - p_bbox[0]
    draw.text((card_x2 - 40 - p_w, card_y1 + 44), page_text, font=font_page, fill=COLOR_MEDIUM_GREEN)

    # Título do Slide
    curr_y = card_y1 + 104
    for line in title_lines:
        draw.text((card_x1 + 40, curr_y), line, font=font_title, fill=title_color)
        curr_y += 56

    curr_y += 14
    # Linha divisória fina
    draw.line([(card_x1 + 40, curr_y), (card_x2 - 40, curr_y)], fill=(215, 222, 217, 200), width=1)
    curr_y += 24

    # Tópicos / Bullets
    bullet_dot_color = COLOR_MEDIUM_GREEN if not is_alert else (195, 75, 60)
    for wb in wrapped_bullets:
        draw.ellipse([card_x1 + 40, curr_y + 10, card_x1 + 50, curr_y + 20], fill=bullet_dot_color)
        bx = card_x1 + 64
        for i, bline in enumerate(wb):
            draw.text((bx, curr_y), bline, font=font_bullet, fill=COLOR_TEXT_MAIN)
            curr_y += 36
        curr_y += 14

    # Caixa de Dica / Acolhimento
    if tip_lines:
        curr_y += 10
        tip_box_y1 = curr_y
        tip_box_y2 = curr_y + (len(tip_lines) * 32) + 26
        tip_bg = (235, 242, 237, 220) if not is_alert else (255, 238, 235, 230)
        tip_border = (185, 205, 192, 200) if not is_alert else (240, 180, 175, 200)
        draw.rounded_rectangle([card_x1 + 35, tip_box_y1, card_x2 - 35, tip_box_y2], radius=14, fill=tip_bg, outline=tip_border, width=1)

        ty = tip_box_y1 + 12
        tip_text_color = COLOR_DEEP_GREEN if not is_alert else (150, 40, 30)
        for tline in tip_lines:
            draw.text((card_x1 + 52, ty), tline, font=font_tip, fill=tip_text_color)
            ty += 32

    # Rodapé sutil com assinatura institucional
    auth_text = "Sônia Torres · Fonoaudióloga"
    draw_pill_badge(draw, 70, 1225, auth_text, get_font(20, weight=700),
                    bg_color=(250, 247, 242, 230), text_color=COLOR_DEEP_GREEN, px=20, py=8, radius=14, outline=(29, 56, 43, 60))

    clean_name = raw_file_name.replace('.jpg', '')
    if clean_name.startswith(f"{slide_num:02d}-"):
        out_name = f"{clean_name}.png"
    else:
        out_name = f"{slide_num:02d}-{clean_name}.png"
    dest_path = os.path.join(FINAL_DIR, out_name)
    img.save(dest_path, "PNG")
    print(f"Slide {slide_num:02d} gerado.")

def render_slide_09():
    """
    Slide 09 — Slide-resumo: Guia Prático por Idade
    Estilo 'página de caderno/fichamento clínico elegante', fundo bege (#FAF7F2),
    sem fotografia, com tabela organizada dos marcos por idade e ícone vetorial de lápis.
    """
    img = Image.new("RGBA", (1080, 1350), COLOR_OFF_WHITE)
    draw = ImageDraw.Draw(img)

    # Moldura decorativa sutil
    draw.rounded_rectangle([45, 45, 1035, 1305], radius=24, fill=None, outline=(218, 228, 221), width=2)
    draw.rounded_rectangle([52, 52, 1028, 1298], radius=20, fill=None, outline=(235, 240, 237), width=1)

    # Ícone vetorial estilizado de lápis / anotação no canto superior direito
    # Desenho geométrico limpo do lápis
    px, py = 920, 115
    draw.polygon([(px+15, py), (px+35, py+20), (px+10, py+45), (px-10, py+25)], fill=COLOR_MEDIUM_GREEN)
    draw.polygon([(px-10, py+25), (px+10, py+45), (px-18, py+53)], fill=COLOR_DEEP_GREEN)
    draw.polygon([(px+35, py+20), (px+15, py), (px+22, py-7), (px+42, py+13)], fill=(200, 150, 120))

    # Badge e Título
    font_badge = get_font(20, weight=700)
    draw_pill_badge(draw, 80, 95, "GUIA RÁPIDO", font_badge,
                    bg_color=COLOR_DARK_BEIGE, text_color=COLOR_DEEP_GREEN, px=20, py=8, radius=14)

    page_text = "09 / 10"
    font_page = get_font(18, weight=700)
    draw.text((790, 105), page_text, font=font_page, fill=COLOR_MEDIUM_GREEN)

    font_title = get_font(46, weight=800)
    draw.text((80, 168), "Resumo: O que esperar da fala", font=font_title, fill=COLOR_DEEP_GREEN)

    font_subtitle = get_font(23, weight=500)
    draw.text((80, 232), "Consulte as etapas principais em cada faixa etária:", font=font_subtitle, fill=COLOR_TEXT_MUTED)

    # Tabela / Cartões das faixas etárias
    stages = [
        ("0 a 6 meses", "Balbucios, risadas, reações a vozes e sons altos e 'troca de turnos' sonoros."),
        ("7 a 11 meses", "Repetição de sílabas (mamama, bababa), palminhas, dar tchau e entender o 'não'."),
        ("1 ano (12m)", "Aponta com intenção clara, compreende comandos e diz as primeiras palavras."),
        ("1 ano e meio", "Fala entre 10 e 20+ palavras, aponta o que quer e imita sons do ambiente."),
        ("2 anos", "Junta 2 palavras ('dá água', 'bola caiu') e tem mais de 50 palavras no vocabulário."),
        ("3 a 6 anos", "Frases completas, fase dos 'por quês', conta histórias e domina quase todos os sons.")
    ]

    card_y = 285
    card_w = 920
    card_x = 80
    font_age = get_font(23, weight=800)
    font_desc = get_font(22, weight=500)

    for i, (age, desc) in enumerate(stages):
        bg = (244, 248, 245) if i % 2 == 0 else (255, 255, 255)
        border = (205, 220, 212)
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + 118], radius=16, fill=bg, outline=border, width=1)

        # Badge lateral de idade
        draw_pill_badge(draw, card_x + 22, card_y + 20, age, font_age,
                        bg_color=COLOR_DEEP_GREEN, text_color=COLOR_OFF_WHITE, px=16, py=6, radius=12)

        # Descrição quebrada
        lines = wrap_text_to_width(desc, font_desc, max_width=card_w - 240, draw=draw)
        ly = card_y + 24
        for line in lines:
            draw.text((card_x + 215, ly), line, font=font_desc, fill=COLOR_TEXT_MAIN)
            ly += 32

        card_y += 134

    # Destaque de acolhimento no rodapé
    highlight_box_y1 = card_y + 10
    highlight_box_y2 = highlight_box_y1 + 100
    draw.rounded_rectangle([card_x, highlight_box_y1, card_x + card_w, highlight_box_y2],
                           radius=16, fill=(235, 242, 237), outline=(190, 210, 198), width=1)

    font_h_title = get_font(22, weight=700)
    font_h_sub = get_font(20, weight=500)
    draw.text((card_x + 24, highlight_box_y1 + 18), "Lembre-se: Cada criança tem o seu próprio ritmo.", font=font_h_title, fill=COLOR_DEEP_GREEN)
    draw.text((card_x + 24, highlight_box_y1 + 54), "Os marcos são bússolas seguras para orientar, não motivos para comparações aflitas.", font=font_h_sub, fill=COLOR_TEXT_MUTED)

    # Assinatura
    font_author = get_font(21, weight=700)
    draw.text((80, 1240), "Sônia Torres · Fonoaudióloga (CRFa 1-17701) · Fonte: SBP / CDC", font=font_author, fill=COLOR_MEDIUM_GREEN)

    dest_path = os.path.join(FINAL_DIR, "09-slide-resumo.png")
    img.save(dest_path, "PNG")
    print("Slide 09 gerado.")

def render_slide_10():
    """
    Slide 10 — Encerramento
    Fundo bege sólido (#FAF7F2), moldura elegante em verde médio (#44634B),
    sem fotografia, assinatura institucional oficial de Sônia Torres,
    CTA forte e acolhedor para salvar e compartilhar.
    """
    img = Image.new("RGBA", (1080, 1350), COLOR_OFF_WHITE)
    draw = ImageDraw.Draw(img)

    # Moldura geométrica elegante dupla em verde médio
    draw.rounded_rectangle([55, 55, 1025, 1295], radius=28, fill=None, outline=COLOR_MEDIUM_GREEN, width=3)
    draw.rounded_rectangle([70, 70, 1010, 1280], radius=20, fill=None, outline=(215, 228, 220), width=1)

    # Ornamento de canto delicado
    for cx, cy in [(90, 90), (990, 90), (90, 1260), (990, 1260)]:
        draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=COLOR_MEDIUM_GREEN)

    # Badge topo
    font_badge = get_font(20, weight=700)
    draw_pill_badge(draw, 420, 140, "ACOLHIMENTO", font_badge,
                    bg_color=COLOR_DARK_BEIGE, text_color=COLOR_DEEP_GREEN, px=22, py=8, radius=14)

    # Pergunta reflexiva
    font_lead = get_font(46, weight=800)
    lead_text = "Ficou com alguma dúvida sobre a fala do seu filho?"
    lead_lines = wrap_text_to_width(lead_text, font_lead, max_width=860, draw=draw)
    ly = 240
    for line in lead_lines:
        bbox = draw.textbbox((0, 0), line, font=font_lead)
        lw = bbox[2] - bbox[0]
        draw.text(((1080 - lw) // 2, ly), line, font=font_lead, fill=COLOR_DEEP_GREEN)
        ly += 62

    # Texto explicativo central
    font_body = get_font(27, weight=500)
    body_text = (
        "Acompanhar de perto o desenvolvimento infantil traz paz de espírito.\n\n"
        "Se você notar que alguns marcos não estão acontecendo como esperado "
        "para a idade, uma avaliação fonoaudiológica precoce tira dúvidas, "
        "orienta a família e apoia a criança com leveza e afeto."
    )
    paragraphs = body_text.split("\n\n")
    ly += 25
    for p in paragraphs:
        p_lines = wrap_text_to_width(p, font_body, max_width=840, draw=draw)
        for pl in p_lines:
            bbox = draw.textbbox((0, 0), pl, font=font_body)
            lw = bbox[2] - bbox[0]
            draw.text(((1080 - lw) // 2, ly), pl, font=font_body, fill=COLOR_TEXT_MAIN)
            ly += 42
        ly += 22

    # Card de Contato e Assinatura Oficial Central
    card_x1 = 120
    card_x2 = 960
    card_y1 = ly + 30
    card_y2 = card_y1 + 250
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=24, fill=(240, 246, 242), outline=(195, 215, 202), width=2)

    # Assinatura
    font_name = get_font(42, weight=800)
    name_text = "Sônia Torres"
    n_bbox = draw.textbbox((0, 0), name_text, font=font_name)
    n_w = n_bbox[2] - n_bbox[0]
    draw.text(((1080 - n_w) // 2, card_y1 + 32), name_text, font=font_name, fill=COLOR_DEEP_GREEN)

    font_role = get_font(24, weight=700)
    role_text = "Fonoaudióloga · CRFa 1-17701"
    r_bbox = draw.textbbox((0, 0), role_text, font=font_role)
    r_w = r_bbox[2] - r_bbox[0]
    draw.text(((1080 - r_w) // 2, card_y1 + 88), role_text, font=font_role, fill=COLOR_MEDIUM_GREEN)

    # Linha divisória dentro do card
    draw.line([(card_x1 + 60, card_y1 + 135), (card_x2 - 60, card_y1 + 135)], fill=(205, 222, 212), width=1)

    font_sub_info = get_font(21, weight=500)
    sub_info_1 = "Avaliação e Estimulação Precoce da Linguagem Infantil"
    si1_bbox = draw.textbbox((0, 0), sub_info_1, font=font_sub_info)
    draw.text(((1080 - (si1_bbox[2] - si1_bbox[0])) // 2, card_y1 + 155), sub_info_1, font=font_sub_info, fill=COLOR_TEXT_MAIN)

    sub_info_2 = "Atendimento presencial e orientação a famílias"
    si2_bbox = draw.textbbox((0, 0), sub_info_2, font=font_sub_info)
    draw.text(((1080 - (si2_bbox[2] - si2_bbox[0])) // 2, card_y1 + 192), sub_info_2, font=font_sub_info, fill=COLOR_TEXT_MUTED)

    # CTA Pill buttons no rodapé
    cta_y = card_y2 + 45
    font_cta = get_font(22, weight=700)
    cta_text = "Salve este post para consultar sempre que precisar 🔖"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    cta_w = cta_bbox[2] - cta_bbox[0]
    draw_pill_badge(draw, (1080 - cta_w - 48) // 2, cta_y, cta_text, font_cta,
                    bg_color=COLOR_DEEP_GREEN, text_color=COLOR_OFF_WHITE, px=24, py=12, radius=18)

    # Indicador de slide
    page_text = "10 / 10"
    font_page = get_font(18, weight=700)
    p_bbox = draw.textbbox((0, 0), page_text, font=font_page)
    draw.text(((1080 - (p_bbox[2] - p_bbox[0])) // 2, 1225), page_text, font=font_page, fill=COLOR_MEDIUM_GREEN)

    dest_path = os.path.join(FINAL_DIR, "10-encerramento.png")
    img.save(dest_path, "PNG")
    print("Slide 10 gerado.")

def main():
    print("Iniciando preparação de fotos brutas...")
    prepare_raw_photos()

    print("\nRenderizando slides finais 1080x1350...")
    render_slide_01()

    # Slide 02: 0 a 6 meses
    render_content_slide(
        slide_num=2,
        raw_file_name="02-0-a-6-meses.jpg",
        age_badge="0 A 6 MESES",
        title="Balbucios e troca de olhares",
        bullets=[
            "Aos 2 meses: reage a sons altos e produz barulhinhos de vogais (ãh, êh, ôh).",
            "Aos 4 meses: vira a cabeça em direção à voz e começa a soltar gargalhadas.",
            "Aos 6 meses: já 'se reveza' fazendo sons com o adulto em tom de conversa."
        ],
        tip_text="Dica de estímulo: Responda aos barulhinhos do bebê como se fosse um diálogo real. Olho no olho!",
        is_alert=False
    )

    # Slide 03: 7 a 11 meses
    render_content_slide(
        slide_num=3,
        raw_file_name="03-7-a-11-meses.jpg",
        age_badge="7 A 11 MESES",
        title="Palminhas e repetição de sílabas",
        bullets=[
            "Perto dos 9 meses: repete sílabas com consoantes ('ba-ba-ba', 'ma-ma-ma', 'da-da-da').",
            "Bate palminhas, dá tchauzinho com as mãos e busca brinquedos escondidos.",
            "Reconhece o próprio nome e começa a entender o significado do 'não'."
        ],
        tip_text="Dica de estímulo: Brinque de 'cadê o bebê? achou!'. Fortalece a atenção compartilhada e a fala.",
        is_alert=False
    )

    # Slide 04: 1 ano
    render_content_slide(
        slide_num=4,
        raw_file_name="04-1-ano.jpg",
        age_badge="1 ANO",
        title="O gesto de apontar e primeiras palavras",
        bullets=[
            "Usa o dedo indicador para apontar o que quer ou para mostrar algo de interesse.",
            "Surge a primeira ou segunda palavra com intenção clara ('mama', 'papa', 'água', 'dá').",
            "Compreende comandos simples apoiados por gestos ('vem cá', 'dá pra mim')."
        ],
        tip_text="Dica de estímulo: Quando a criança apontar, nomeie o objeto com calma antes de entregá-lo.",
        is_alert=False
    )

    # Slide 05: 1 ano e 6 meses
    render_content_slide(
        slide_num=5,
        raw_file_name="05-1-ano-e-6-meses.jpg",
        age_badge="1 ANO E 6 MESES",
        title="Explosão de palavras e compreensão",
        bullets=[
            "Vocabulário ativo costuma ter pelo menos 10 a 20 palavras funcionais.",
            "Reconhece e aponta partes do corpo ou figuras conhecidas em livros ilustrados.",
            "Imita ativamente sons de animais, veículos e palavras simples da rotina."
        ],
        tip_text="Dica de estímulo: Evite telas. A fala da criança floresce na conversa viva do dia a dia familiar.",
        is_alert=False
    )

    # Slide 06: 2 anos
    render_content_slide(
        slide_num=6,
        raw_file_name="06-2-anos.jpg",
        age_badge="2 ANOS",
        title="Juntando duas palavras em frases",
        bullets=[
            "Combina pelo menos duas palavras com sentido ('dá água', 'bola caiu', 'papai foi').",
            "O vocabulário falado ultrapassa 50 palavras distintas no repertório diário.",
            "Quem convive no lar já compreende mais da metade de tudo o que a criança fala."
        ],
        tip_text="Dica de estímulo: Não corrija com cobrança. Devolva a frase de forma correta e amorosa.",
        is_alert=False
    )

    # Slide 07: 3 a 6 anos
    render_content_slide(
        slide_num=7,
        raw_file_name="07-3-a-6-anos.jpg",
        age_badge="3 A 6 ANOS",
        title="Frases completas, 'por quês' e histórias",
        bullets=[
            "Aos 3 anos: frases de 3 ou mais palavras, muitas perguntas ('por quê?') e conversa fluida.",
            "Aos 4 anos: relata acontecimentos do dia e a fala é entendida por pessoas de fora de casa.",
            "Aos 5 a 6 anos: conta histórias em sequência e quase todos os sons já estão dominados."
        ],
        tip_text="Dica de estímulo: Leitura diária de historinhas é o maior acelerador de vocabulário e imaginação.",
        is_alert=False
    )

    # Slide 08: Observe (sinais de alerta)
    render_content_slide(
        slide_num=8,
        raw_file_name="08-observe-alertas.jpg",
        age_badge="OBSERVE COM ATENÇÃO",
        title="Quando buscar avaliação fonoaudiológica",
        bullets=[
            "Aos 6 meses: não reage a sons, não olha nos olhos ou não balbucia nenhum som.",
            "Aos 12 meses: não aponta, não usa nenhum gesto ou não balbucia sílabas.",
            "Aos 18 meses: não fala palavras simples ou não atende a comandos rotineiros.",
            "Aos 2 anos: não junta duas palavras ou tem vocabulário muito restrito (< 50).",
            "Aos 3 anos ou mais: pessoas de fora não entendem o que a criança fala."
        ],
        tip_text="Lembrete acolhedor: Buscar ajuda cedo não é rotular; é apoiar a comunicação com tranquilidade.",
        is_alert=True
    )

    render_slide_09()
    render_slide_10()

    print("\nTodos os 10 slides foram renderizados com sucesso em 1080x1350 px!")

if __name__ == "__main__":
    main()
