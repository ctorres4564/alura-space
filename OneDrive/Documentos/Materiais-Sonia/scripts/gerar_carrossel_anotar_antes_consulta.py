# -*- coding: utf-8 -*-
"""
Script de Produção Automatizada — Carrossel Instagram 4:5 (1080 x 1350 px)
Carrossel: "O que anotar antes da consulta"
Cliente: Sônia Torres — Fonoaudióloga (CRFa 1-17701)
Linha: Infantil / Família / Observação da Comunicação

Gera:
1. Cópia das fotografias brutas em: avulsos/carrossel-lista-anotar-antes-da-consulta/raw-photos/
2. Slides finais (01 a 09 em PNG) em: avulsos/carrossel-lista-anotar-antes-da-consulta/slides-finais/
3. Grade de visualização comparativa: avulsos/carrossel-lista-anotar-antes-da-consulta/preview-grade.jpg
"""

import os
import shutil
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# Caminhos principais do workspace
WORKSPACE = Path(r"c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia")
CARROSSEL_DIR = WORKSPACE / "avulsos" / "carrossel-lista-anotar-antes-da-consulta"
RAW_DIR = CARROSSEL_DIR / "raw-photos"
FINAL_DIR = CARROSSEL_DIR / "slides-finais"
FONT_PATH = WORKSPACE / "assets" / "fonts" / "PlusJakartaSans-Variable.ttf"

RAW_DIR.mkdir(parents=True, exist_ok=True)
FINAL_DIR.mkdir(parents=True, exist_ok=True)

# Dimensões 4:5 padrão Instagram feed
W, H = 1080, 1350

# Paleta oficial da identidade visual
COLOR_DEEP_GREEN = (29, 56, 43)        # #1D382B - Verde Petróleo Profundo
COLOR_CREAM = (250, 247, 242)          # #FAF7F2 - Off-White leitura
COLOR_BEIGE = (234, 228, 216)          # #EAE4D8 - Bege escuro cartões/badges
COLOR_BORDER = (226, 219, 208)         # #E2DBD0 - Borda sutil
COLOR_OLIVE = (68, 99, 75)             # #44634B - Verde Oliva de apoio
COLOR_TEXT_DARK = (46, 44, 41)         # #2E2C29 - Cinza grafite texto
COLOR_MUTED = (105, 100, 93)           # #69645D - Texto secundário
COLOR_LIGHT_CARD = (255, 255, 255)     # #FFFFFF - Card puro
COLOR_WHITE = (255, 255, 255)
COLOR_GOLD = (201, 164, 76)            # #C9A44C - Dourado sutil de destaque

# Mapeamento das imagens de alta resolução geradas
BRAIN_DIR = Path(r"C:\Users\Gamer\.gemini\antigravity-ide\brain\ba4cc574-fef7-48dd-be38-d38c8f7301a6")
SOURCE_PHOTOS = {
    "01-capa.jpg": BRAIN_DIR / "anotar_01_capa_1791486463693.jpg",
    "03-atencao.jpg": BRAIN_DIR / "anotar_03_atencao_1791486482737.jpg",
    "04-resposta-nome.jpg": BRAIN_DIR / "anotar_04_resposta_nome_1791486510558.jpg",
    "05-formas-pedir.jpg": BRAIN_DIR / "anotar_05_formas_pedir_1791486535514.jpg",
    "06-brincadeira.jpg": BRAIN_DIR / "anotar_06_brincadeira_1791486566771.jpg",
    "07-sensorial.jpg": BRAIN_DIR / "anotar_07_sensorial_1791486598375.jpg",
    "09-encerramento.jpg": BRAIN_DIR / "anotar_09_encerramento_1791486635963.jpg",
}

# Cópia das fotos para raw-photos
for fname, src_path in SOURCE_PHOTOS.items():
    dest_path = RAW_DIR / fname
    if src_path.exists():
        shutil.copy2(src_path, dest_path)
        print(f"[OK] Foto copiada: {fname}")
    else:
        print(f"[AVISO] Origem nao encontrada: {src_path}")


def get_font(size, weight=400):
    try:
        font = ImageFont.truetype(str(FONT_PATH), size)
        if hasattr(font, 'set_variation_by_axes'):
            font.set_variation_by_axes([weight])
        return font
    except Exception:
        # Fallback Windows
        if weight >= 700 and os.path.exists(r"C:\Windows\Fonts\segoeuib.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", size)
        elif weight >= 600 and os.path.exists(r"C:\Windows\Fonts\seguisb.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\seguisb.ttf", size)
        elif os.path.exists(r"C:\Windows\Fonts\segoeui.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", size)
        return ImageFont.load_default()


def cover_crop(img, target_w, target_h):
    scale = max(target_w / img.width, target_h / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - target_w) // 2
    top = (nh - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def wrap_text(draw, text, font, max_width):
    lines = []
    paragraphs = text.split("\n")
    for para in paragraphs:
        if not para.strip():
            lines.append("")
            continue
        words = para.split(" ")
        current = ""
        for word in words:
            test = word if not current else f"{current} {word}"
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def draw_rounded_card(im, x, y, w, h, radius, fill_color, border_color=None, border_width=1):
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill_color, outline=border_color, width=border_width)
    im.alpha_composite(overlay)


def draw_badge(draw, text, x, y, bg_color, text_color, font_size=22, padding_x=22, padding_y=10):
    font = get_font(font_size, 700)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bw = tw + padding_x * 2
    bh = th + padding_y * 2 + 4
    radius = bh // 2
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=radius, fill=bg_color)
    tx = x + padding_x
    ty = y + padding_y - bbox[1]
    draw.text((tx, ty), text, fill=text_color, font=font)
    return bw, bh


def draw_header_nav(draw, current_slide, total_slides=9, tag_text="COMUNICAÇÃO INFANTIL", is_dark=False):
    font_tag = get_font(21, 700)
    font_ind = get_font(21, 600)
    
    tag_color = COLOR_BEIGE if is_dark else COLOR_OLIVE
    ind_color = (200, 215, 205) if is_dark else COLOR_MUTED
    
    # Tag à esquerda
    draw.text((70, 75), tag_text.upper(), fill=tag_color, font=font_tag)
    
    # Indicador de slide à direita
    ind_str = f"{current_slide:02d} / {total_slides:02d}"
    bbox = draw.textbbox((0, 0), ind_str, font=font_ind)
    draw.text((W - 70 - (bbox[2] - bbox[0]), 75), ind_str, fill=ind_color, font=font_ind)


def draw_footer_brand(draw, is_dark=False, action_note=None):
    font_brand = get_font(20, 600)
    font_action = get_font(20, 600)
    
    brand_color = (210, 225, 215) if is_dark else COLOR_MUTED
    action_color = COLOR_GOLD if is_dark else COLOR_DEEP_GREEN
    
    brand_text = "Sônia Torres · Fonoaudióloga · CRFa 1-17701"
    draw.text((70, H - 85), brand_text, fill=brand_color, font=font_brand)
    
    if action_note:
        bbox = draw.textbbox((0, 0), action_note, font=font_action)
        draw.text((W - 70 - (bbox[2] - bbox[0]), H - 85), action_note, fill=action_color, font=font_action)


# ==========================================
# RENDERIZADORES INDIVIDUAIS DOS 9 SLIDES
# ==========================================

def render_slide_01():
    """Slide 1 — Capa com fotografia documental e tipografia editorial sofisticada"""
    photo_file = RAW_DIR / "01-capa.jpg"
    base_photo = Image.open(photo_file).convert("RGB")
    im = cover_crop(base_photo, W, H).convert("RGBA")
    
    # Camada de gradiente elegante no topo e base para garantir legibilidade impecável
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_over = ImageDraw.Draw(overlay)
    
    # Degradê sutil superior
    for y in range(460):
        alpha = int(210 * (1 - y / 460) ** 1.3)
        d_over.line([(0, y), (W, y)], fill=(250, 247, 242, alpha))
        
    # Card elegante flutuante para ancorar o título
    card_w, card_h = W - 120, 480
    card_x, card_y = 60, 110
    d_over.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=28,
        fill=(250, 247, 242, 242),
        outline=COLOR_BORDER,
        width=2
    )
    
    im.alpha_composite(overlay)
    draw = ImageDraw.Draw(im)
    
    # Badge do topo do card
    draw_badge(draw, "OBSERVAÇÃO CLÍNICA", card_x + 45, card_y + 45, COLOR_BEIGE, COLOR_DEEP_GREEN, font_size=20)
    
    # Indicador de slide
    font_ind = get_font(21, 600)
    draw.text((card_x + card_w - 110, card_y + 48), "01 / 09", fill=COLOR_MUTED, font=font_ind)
    
    # Título Principal da Capa
    font_title = get_font(52, 800)
    title_text = "O que anotar antes\nda consulta"
    draw.text((card_x + 45, card_y + 115), title_text, fill=COLOR_DEEP_GREEN, font=font_title, spacing=14)
    
    # Subtítulo explicativo
    font_sub = get_font(27, 500)
    sub_text = "Sobre a comunicação de crianças dentro\ndo espectro autista."
    draw.text((card_x + 45, card_y + 270), sub_text, fill=COLOR_TEXT_DARK, font=font_sub, spacing=10)
    
    # Selo de utilidade no card
    draw_badge(draw, "📌 Salve para levar na consulta", card_x + 45, card_y + 390, COLOR_DEEP_GREEN, COLOR_CREAM, font_size=22, padding_x=24, padding_y=12)
    
    # Faixa inferior com crédito da Dra. Sônia e chamada de arraste
    pill_w, pill_h = W - 140, 84
    pill_x, pill_y = 70, H - 140
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=24, fill=(29, 56, 43, 235))
    
    font_brand = get_font(22, 600)
    font_swipe = get_font(22, 700)
    draw.text((pill_x + 35, pill_y + 26), "Sônia Torres · Fonoaudióloga", fill=COLOR_CREAM, font=font_brand)
    
    swipe_text = "Arraste para o lado 👉"
    bbox = draw.textbbox((0, 0), swipe_text, font=font_swipe)
    draw.text((pill_x + pill_w - (bbox[2] - bbox[0]) - 35, pill_y + 26), swipe_text, fill=(255, 230, 160), font=font_swipe)
    
    return im.convert("RGB")


def render_slide_02():
    """Slide 2 — Contexto e Alinhamento Ético (Sem foto, design editorial e acolhedor)"""
    im = Image.new("RGBA", (W, H), COLOR_CREAM)
    draw = ImageDraw.Draw(im)
    
    draw_header_nav(draw, 2, 9, tag_text="PREPARO PARA AVALIAÇÃO")
    
    # Card Central Editorial com moldura dupla
    cx, cy = 70, 150
    cw, ch = W - 140, H - 300
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=32, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
    
    # Tag de destaque no interior do card
    draw_badge(draw, "POR QUE REGISTRAR?", cx + 55, cy + 60, COLOR_BEIGE, COLOR_DEEP_GREEN, font_size=22)
    
    # Citação de impacto com aspas editoriais
    font_quote_mark = get_font(84, 800)
    draw.text((cx + 55, cy + 130), "“", fill=COLOR_OLIVE, font=font_quote_mark)
    
    font_main = get_font(42, 700)
    main_text = "Anotar o dia a dia ajuda quem avalia a entender a comunicação da criança no ambiente real dela."
    lines_main = wrap_text(draw, main_text, font_main, cw - 110)
    
    curr_y = cy + 225
    for line in lines_main:
        draw.text((cx + 55, curr_y), line, fill=COLOR_DEEP_GREEN, font=font_main)
        curr_y += 62
        
    # Linha divisória fina e elegante
    curr_y += 35
    draw.line([(cx + 55, curr_y), (cx + cw - 55, curr_y)], fill=COLOR_BORDER, width=1)
    
    # Bloco explicativo sobre a ausência de diagnóstico/autoteste
    curr_y += 45
    box_w = cw - 110
    box_h = 240
    draw.rounded_rectangle([cx + 55, curr_y, cx + 55 + box_w, curr_y + box_h], radius=20, fill=(244, 239, 232), outline=COLOR_BORDER, width=1)
    
    font_note_title = get_font(26, 700)
    draw.text((cx + 85, curr_y + 35), "⚠️ Importante lembrar:", fill=COLOR_DEEP_GREEN, font=font_note_title)
    
    font_note_body = get_font(25, 400)
    note_text = (
        "Esta lista não é um teste, não soma pontos e não serve para "
        "diagnóstico. Quem avalia observa o contexto completo da criança, "
        "e suas anotações trazem a realidade da sua casa para a consulta."
    )
    lines_note = wrap_text(draw, note_text, font_note_body, box_w - 60)
    ny = curr_y + 85
    for line in lines_note:
        draw.text((cx + 85, ny), line, fill=COLOR_TEXT_DARK, font=font_note_body)
        ny += 40
        
    # Rodapé institucional
    draw_footer_brand(draw, is_dark=False, action_note="Deslize para ver os 5 pontos →")
    return im.convert("RGB")


def render_content_slide(slide_num, total_slides, area_num, area_title, prompt_question, photo_filename, observation_tip=None):
    """Renderiza slides das áreas 1 a 5 com fotografia documental de alta resolução e card editorial"""
    im = Image.new("RGBA", (W, H), COLOR_CREAM)
    draw = ImageDraw.Draw(im)
    
    draw_header_nav(draw, slide_num, total_slides, tag_text=f"ÁREA {area_num} DE 5")
    
    # Card com a Fotografia Documental
    # Dimensões da foto em formato harmonioso (1080 - 140 = 940 de largura, 560 de altura)
    photo_w = W - 140
    photo_h = 570
    px, py = 70, 140
    
    photo_file = RAW_DIR / photo_filename
    if photo_file.exists():
        raw_img = Image.open(photo_file).convert("RGB")
        cropped_photo = cover_crop(raw_img, photo_w, photo_h)
        
        # Aplicar cantos arredondados na imagem
        mask = Image.new("L", (photo_w, photo_h), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, photo_w, photo_h], radius=28, fill=255)
        
        im.paste(cropped_photo, (px, py), mask)
        
        # Borda sutil sobre a foto
        draw.rounded_rectangle([px, py, px + photo_w, py + photo_h], radius=28, outline=COLOR_BORDER, width=2)
    
    # Card Inferior de Texto e Pergunta
    card_y = py + photo_h + 30
    card_h = H - card_y - 140
    draw.rounded_rectangle([px, card_y, px + photo_w, card_y + card_h], radius=28, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
    
    # Tag interna da área
    draw_badge(draw, f"ÁREA {area_num}", px + 45, card_y + 40, COLOR_BEIGE, COLOR_DEEP_GREEN, font_size=20)
    
    # Título da Área
    font_area_title = get_font(36, 800)
    draw.text((px + 45, card_y + 98), area_title, fill=COLOR_DEEP_GREEN, font=font_area_title)
    
    # Linha divisória suave
    draw.line([(px + 45, card_y + 158), (px + photo_w - 45, card_y + 158)], fill=COLOR_BORDER, width=1)
    
    # Pergunta reflexiva para os pais
    font_question = get_font(28, 500)
    lines_q = wrap_text(draw, prompt_question, font_question, photo_w - 90)
    
    qy = card_y + 185
    for line in lines_q:
        draw.text((px + 45, qy), line, fill=COLOR_TEXT_DARK, font=font_question)
        qy += 44
        
    # Dica prática opcional de observação
    if observation_tip:
        font_tip = get_font(22, 600)
        draw.text((px + 45, card_y + card_h - 55), observation_tip, fill=COLOR_OLIVE, font=font_tip)
        
    draw_footer_brand(draw, is_dark=False, action_note="Deslize →")
    return im.convert("RGB")


def render_slide_08():
    """Slide 8 — Roteiro Resumo (Alto contraste para print e consulta rápida no celular)"""
    im = Image.new("RGBA", (W, H), COLOR_DEEP_GREEN)
    draw = ImageDraw.Draw(im)
    
    draw_header_nav(draw, 8, 9, tag_text="GUIA DE BOLSO", is_dark=True)
    
    # Card central escuro elegante
    cx, cy = 65, 140
    cw, ch = W - 130, H - 280
    draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=32, fill=(35, 68, 52), outline=(52, 98, 76), width=2)
    
    # Badge do topo do card
    draw_badge(draw, "FEITO PARA PRINTAR", cx + 45, cy + 45, (52, 98, 76), COLOR_CREAM, font_size=20)
    
    # Título do Roteiro
    font_title = get_font(42, 800)
    draw.text((cx + 45, cy + 105), "Roteiro de Anotação", fill=COLOR_CREAM, font=font_title)
    
    font_sub = get_font(23, 400)
    draw.text((cx + 45, cy + 165), "Guarde esta lista para levar para a sala de atendimento:", fill=(200, 220, 210), font=font_sub)
    
    # 5 Itens estruturados com ícones e destaque
    items = [
        ("1. Atenção compartilhada", "Olha quando você aponta ou mostra algo com interesse?"),
        ("2. Resposta ao nome", "Em quais situações responde e em quais não parece ouvir?"),
        ("3. Formas de pedir", "Pede com gesto, palavra, som ou puxando você até o objeto?"),
        ("4. Brincadeira e imitação", "Imita gestos/sons? Como explora brinquedos e pessoas?"),
        ("5. Sensibilidades e rotina", "O que acalma e o que incomoda (sons, toques, luzes)?"),
    ]
    
    iy = cy + 225
    for idx, (head, desc) in enumerate(items, 1):
        # Caixa de item
        box_item_h = 92
        draw.rounded_rectangle([cx + 40, iy, cx + cw - 40, iy + box_item_h], radius=16, fill=(29, 56, 43), outline=(48, 88, 68), width=1)
        
        # Marcador numérico
        draw.rounded_rectangle([cx + 55, iy + 20, cx + 105, iy + 70], radius=12, fill=COLOR_OLIVE)
        font_num = get_font(24, 700)
        draw.text((cx + 72, iy + 28), str(idx), fill=COLOR_CREAM, font=font_num)
        
        # Textos do item
        font_head = get_font(25, 700)
        draw.text((cx + 125, iy + 16), head, fill=COLOR_CREAM, font=font_head)
        
        font_desc = get_font(21, 400)
        draw.text((cx + 125, iy + 52), desc, fill=(210, 225, 218), font=font_desc)
        
        iy += 106
        
    # Box de instrução final: O que anotar para cada item
    box_note_y = iy + 15
    draw.rounded_rectangle([cx + 40, box_note_y, cx + cw - 40, box_note_y + 110], radius=18, fill=COLOR_CREAM)
    
    font_rule_title = get_font(22, 800)
    draw.text((cx + 65, box_note_y + 22), "📝 Para cada anotação, registre sempre:", fill=COLOR_DEEP_GREEN, font=font_rule_title)
    
    font_rule_desc = get_font(23, 600)
    draw.text((cx + 65, box_note_y + 58), "Quando aconteceu  •  Com quem estava  •  Em qual lugar", fill=COLOR_OLIVE, font=font_rule_desc)
    
    draw_footer_brand(draw, is_dark=True, action_note="Tire print deste slide 📸")
    return im.convert("RGB")


def render_slide_09():
    """Slide 9 — Encerramento, Acolhimento e Assinatura com foto documental de mãos e caderno"""
    photo_file = RAW_DIR / "09-encerramento.jpg"
    base_photo = Image.open(photo_file).convert("RGB")
    im = cover_crop(base_photo, W, H).convert("RGBA")
    
    # Overlay com gradiente do meio para baixo para contraste perfeito
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_over = ImageDraw.Draw(overlay)
    
    # Gradiente na parte superior suave
    for y in range(250):
        alpha = int(180 * (1 - y / 250) ** 1.2)
        d_over.line([(0, y), (W, y)], fill=(250, 247, 242, alpha))
        
    # Card elegante na parte inferior
    card_w, card_h = W - 120, 620
    card_x, card_y = 60, H - 690
    d_over.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=30,
        fill=(250, 247, 242, 246),
        outline=COLOR_BORDER,
        width=2
    )
    
    im.alpha_composite(overlay)
    draw = ImageDraw.Draw(im)
    
    draw_header_nav(draw, 9, 9, tag_text="ENCERRAMENTO")
    
    # Badge do Card
    draw_badge(draw, "LEVE PARA A CONSULTA", card_x + 45, card_y + 45, COLOR_BEIGE, COLOR_DEEP_GREEN, font_size=20)
    
    # Texto principal de acolhimento
    font_main = get_font(31, 700)
    main_text = (
        "Quem avalia observa o conjunto, não um item isolado.\n"
        "Suas anotações e a sua percepção diária são partes "
        "fundamentais desse processo."
    )
    lines_main = wrap_text(draw, main_text, font_main, card_w - 90)
    my = card_y + 115
    for line in lines_main:
        draw.text((card_x + 45, my), line, fill=COLOR_DEEP_GREEN, font=font_main)
        my += 48
        
    # Linha divisória
    my += 20
    draw.line([(card_x + 45, my), (card_x + card_w - 45, my)], fill=COLOR_BORDER, width=1)
    
    # Chamada para ação
    my += 28
    font_cta = get_font(25, 600)
    cta_text = "Salve este post para consultar antes da sua próxima consulta."
    lines_cta = wrap_text(draw, cta_text, font_cta, card_w - 90)
    for line in lines_cta:
        draw.text((card_x + 45, my), line, fill=COLOR_TEXT_DARK, font=font_cta)
        my += 38
        
    # Assinatura Profissional com CRFa
    my += 25
    draw.rounded_rectangle([card_x + 45, my, card_x + card_w - 45, my + 105], radius=18, fill=COLOR_DEEP_GREEN)
    
    font_name = get_font(26, 700)
    draw.text((card_x + 75, my + 20), "Sônia Torres · Fonoaudióloga", fill=COLOR_CREAM, font=font_name)
    
    font_crf = get_font(21, 500)
    draw.text((card_x + 75, my + 58), "CRFa 1-17701  •  Atendimento infantil e neurofuncional", fill=(210, 225, 218), font=font_crf)
    
    # Referência técnica discreta na base
    font_ref = get_font(18, 400)
    ref_text = "Referência técnica: Manual de Orientação TEA (Sociedade Brasileira de Pediatria, 2019)"
    draw.text((card_x + 55, card_y + card_h - 40), ref_text, fill=COLOR_MUTED, font=font_ref)
    
    return im.convert("RGB")


# ==========================================
# GERAÇÃO DA GRADE DE VISUALIZAÇÃO (PREVIEW)
# ==========================================

def render_preview_grid(slides):
    """Gera uma prancha de contato 3x3 de alta qualidade com todos os slides"""
    cols, rows = 3, 3
    thumb_w, thumb_h = 360, 450
    gap = 24
    pad = 36
    
    grid_w = cols * thumb_w + (cols - 1) * gap + pad * 2
    grid_h = rows * thumb_h + (rows - 1) * gap + pad * 2
    
    grid_img = Image.new("RGB", (grid_w, grid_h), (234, 228, 216))
    draw = ImageDraw.Draw(grid_img)
    
    for idx, slide in enumerate(slides):
        col = idx % cols
        row = idx // cols
        
        gx = pad + col * (thumb_w + gap)
        gy = pad + row * (thumb_h + gap)
        
        thumb = slide.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        grid_img.paste(thumb, (gx, gy))
        draw.rectangle([gx, gy, gx + thumb_w, gy + thumb_h], outline=(180, 172, 160), width=2)
        
    return grid_img


# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================

def main():
    print("Iniciando renderizacao dos 9 slides do carrossel...")
    
    slides_rendered = []
    
    # 01 - Capa
    print("Renderizando Slide 01 (Capa)...")
    s1 = render_slide_01()
    s1.save(FINAL_DIR / "01-capa.png", format="PNG", quality=95)
    slides_rendered.append(s1)
    
    # 02 - Contexto
    print("Renderizando Slide 02 (Contexto)...")
    s2 = render_slide_02()
    s2.save(FINAL_DIR / "02-contexto.png", format="PNG", quality=95)
    slides_rendered.append(s2)
    
    # 03 - Área 1: Atenção compartilhada
    print("Renderizando Slide 03 (Área 1: Atenção Compartilhada)...")
    s3 = render_content_slide(
        slide_num=3,
        total_slides=9,
        area_num=1,
        area_title="Atenção compartilhada",
        prompt_question="Ele olha quando você aponta ou mostra algo? Tenta mostrar coisas para você, ou olha para o seu rosto quando algo acontece?",
        photo_filename="03-atencao.jpg",
        observation_tip="💡 Dica: observe se há troca de olhares ao apontar objetos."
    )
    s3.save(FINAL_DIR / "03-area-1-atencao-compartilhada.png", format="PNG", quality=95)
    slides_rendered.append(s3)
    
    # 04 - Área 2: Resposta ao nome
    print("Renderizando Slide 04 (Área 2: Resposta ao Nome)...")
    s4 = render_content_slide(
        slide_num=4,
        total_slides=9,
        area_num=2,
        area_title="Resposta ao nome",
        prompt_question="Como ele responde quando você o chama? Em que situações costuma responder e em quais parece não ouvir?",
        photo_filename="04-resposta-nome.jpg",
        observation_tip="💡 Dica: anote se responde quando entretido com algo de que gosta."
    )
    s4.save(FINAL_DIR / "04-area-2-resposta-ao-nome.png", format="PNG", quality=95)
    slides_rendered.append(s4)
    
    # 05 - Área 3: Formas de pedir
    print("Renderizando Slide 05 (Área 3: Formas de Pedir)...")
    s5 = render_content_slide(
        slide_num=5,
        total_slides=9,
        area_num=3,
        area_title="Formas de pedir",
        prompt_question="Ele pede o que quer usando gestos, sons, palavras, apontando, puxando sua mão ou levando você até o que deseja?",
        photo_filename="05-formas-pedir.jpg",
        observation_tip="💡 Dica: registre a maneira como expressa cada necessidade."
    )
    s5.save(FINAL_DIR / "05-area-3-formas-de-pedir.png", format="PNG", quality=95)
    slides_rendered.append(s5)
    
    # 06 - Área 4: Brincadeira e imitação
    print("Renderizando Slide 06 (Área 4: Brincadeira e Imitação)...")
    s6 = render_content_slide(
        slide_num=6,
        total_slides=9,
        area_num=4,
        area_title="Brincadeira e imitação",
        prompt_question="Ele imita sons, gestos ou ações simples? Como brinca com os brinquedos no chão e quando interage com você?",
        photo_filename="06-brincadeira.jpg",
        observation_tip="💡 Dica: anote se empilha, enfileira ou faz de conta."
    )
    s6.save(FINAL_DIR / "06-area-4-brincadeira-e-imitacao.png", format="PNG", quality=95)
    slides_rendered.append(s6)
    
    # 07 - Área 5: Contexto sensorial
    print("Renderizando Slide 07 (Área 5: Contexto Sensorial)...")
    s7 = render_content_slide(
        slide_num=7,
        total_slides=9,
        area_num=5,
        area_title="Contexto sensorial",
        prompt_question="O que acalma ou incomoda: sons altos, luzes fortes, certos toques ou mudanças de rotina? Anote a situação, não um rótulo.",
        photo_filename="07-sensorial.jpg",
        observation_tip="💡 Dica: descreva a cena exata em que o incômodo ocorreu."
    )
    s7.save(FINAL_DIR / "07-area-5-contexto-sensorial.png", format="PNG", quality=95)
    slides_rendered.append(s7)
    
    # 08 - Roteiro de anotação (Resumo)
    print("Renderizando Slide 08 (Roteiro Resumo)...")
    s8 = render_slide_08()
    s8.save(FINAL_DIR / "08-roteiro-de-anotacao.png", format="PNG", quality=95)
    slides_rendered.append(s8)
    
    # 09 - Encerramento
    print("Renderizando Slide 09 (Encerramento)...")
    s9 = render_slide_09()
    s9.save(FINAL_DIR / "09-encerramento.png", format="PNG", quality=95)
    slides_rendered.append(s9)
    
    # Grade de visualização
    print("Gerando grade de visualizacao comparativa (preview-grade.jpg)...")
    grid = render_preview_grid(slides_rendered)
    grid.save(CARROSSEL_DIR / "preview-grade.jpg", format="JPEG", quality=92)
    
    print("\n[SUCESSO] Todos os 9 slides e a prancha de preview foram gerados com sucesso!")
    print(f"Arquivos salvos em: {FINAL_DIR}")


if __name__ == "__main__":
    main()
