"""
Script de Produção Automatizada — Destaque Instagram "Quem é" (1080 x 1920 px e Capa 1080 x 1080 px)
Cliente: Sônia Torres — Fonoaudióloga (CRFa 1-17701)
Site: sonia.fonosuite.com
Formação: Universidade Federal do Rio de Janeiro — UFRJ

Gera:
1. Story 01 — Apresentação (1080 x 1920)
2. Story 02 — Formação (1080 x 1920)
3. Story 03 — Forma de Trabalho (1080 x 1920)
4. Story 04 — Quem Atende (1080 x 1920)
5. Story 05 — Chamada Final (1080 x 1920)
6. Capa do Destaque "Quem é" (1080 x 1080 e 1080 x 1920 com centro seguro)
7. Prancha de Visão Geral (comparativo editorial em alta resolução)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# Diretórios
BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\1MATERIASIDASONIA"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(ASSETS_DIR, "destaque-quem-e")
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "PlusJakartaSans-Variable.ttf")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Paleta Cromática Editorial Oficial da Marca
COLOR_DEEP_GREEN = (29, 56, 43)        # #1D382B - Verde Petróleo Profundo (Primária)
COLOR_OLIVE = (68, 99, 75)             # #44634B - Verde Oliva Clínico (Apoio / Destaques)
COLOR_OFFWHITE = (250, 247, 242)       # #FAF7F2 - Fundo Creme Acolhedor Geral
COLOR_CARD = (244, 239, 232)           # #F4EFE8 - Bege Claro Cartões
COLOR_CARD_ALT = (236, 231, 222)       # #ECE7DE - Areia Suave
COLOR_CHARCOAL = (46, 44, 41)          # #2E2C29 - Grafite Texto Principal
COLOR_MUTED = (112, 107, 100)          # #706B64 - Texto Secundário / Apoio
COLOR_BORDER = (226, 219, 208)         # #E2DBD0 - Borda Sutil
COLOR_CORAL = (196, 84, 46)            # #C4542E - Terracota / Destaque Sutil
COLOR_WHITE = (255, 255, 255)

STORY_WIDTH = 1080
STORY_HEIGHT = 1920

# Safe zones do Instagram Stories
SAFE_TOP = 220
SAFE_BOTTOM = 1660

def get_font(size, weight=400):
    """Carrega a fonte variável Plus Jakarta Sans."""
    try:
        font = ImageFont.truetype(FONT_PATH, size)
        if hasattr(font, 'set_variation_by_name'):
            if weight >= 700:
                try: font.set_variation_by_name('Bold')
                except: pass
            elif weight >= 600:
                try: font.set_variation_by_name('SemiBold')
                except: pass
            elif weight >= 500:
                try: font.set_variation_by_name('Medium')
                except: pass
        elif hasattr(font, 'set_variation_by_axes'):
            try:
                font.set_variation_by_axes([weight])
            except:
                pass
        return font
    except Exception:
        return ImageFont.load_default()

def draw_pill(draw, xy, text, font, bg_color, text_color, border_color=None, padding_x=24, padding_y=12):
    """Desenha uma tag/pílula elegante com texto centralizado."""
    x0, y0 = xy
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + padding_x * 2
    h = th + padding_y * 2
    rect = [x0, y0, x0 + w, y0 + h]
    radius = h // 2
    draw.rounded_rectangle(rect, radius=radius, fill=bg_color, outline=border_color, width=1 if border_color else 0)
    tx = x0 + padding_x - bbox[0]
    ty = y0 + padding_y - bbox[1]
    draw.text((tx, ty), text, font=font, fill=text_color)
    return w, h

def wrap_text(text, font, max_width):
    """Quebra linhas de texto respeitando a largura máxima."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def draw_card_shadow(image, rect, radius=32, shadow_color=(0, 0, 0, 25), blur=18, offset_y=8):
    """Adiciona sombra suave e difusa a um cartão para acabamento editorial de luxo."""
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    x0, y0, x1, y1 = rect
    s_draw.rounded_rectangle([x0, y0 + offset_y, x1, y1 + offset_y], radius=radius, fill=shadow_color)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    image.paste(shadow, (0, 0), shadow)

def draw_profile_icon(draw, cx, cy, size, color):
    """Desenha um ícone minimalista e refinado de perfil/pessoa."""
    head_r = int(size * 0.23)
    head_cy = int(cy - size * 0.16)
    draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=color)
    
    shoulder_w = int(size * 0.62)
    shoulder_h = int(size * 0.38)
    shoulder_y0 = int(cy + size * 0.10)
    shoulder_y1 = shoulder_y0 + shoulder_h
    draw.chord([cx - shoulder_w // 2, shoulder_y0, cx + shoulder_w // 2, shoulder_y1], start=180, end=0, fill=color)

def draw_vector_link_icon(draw, cx, cy, size, color):
    """Desenha um ícone vetorial nítido de link (duas alças entrelaçadas)."""
    r = size // 2
    sw = max(3, size // 9)
    # Alça esquerda
    x1, y1 = cx - r // 2, cy
    draw.ellipse([x1 - r//2, y1 - r//2, x1 + r//2, y1 + r//2], outline=color, width=sw)
    # Alça direita
    x2, y2 = cx + r // 2, cy
    draw.ellipse([x2 - r//2, y2 - r//2, x2 + r//2, y2 + r//2], outline=color, width=sw)
    # Haste central
    draw.line([x1, y1, x2, y2], fill=color, width=sw)

def draw_vector_pin_dot(draw, cx, cy, radius, color):
    """Desenha um marcador circular moderno com anel externo."""
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)
    draw.ellipse([cx - radius - 3, cy - radius - 3, cx + radius + 3, cy + radius + 3], outline=color, width=1)

def generate_story_01():
    """STORY 1 — APRESENTAÇÃO
    Texto:
    Sônia Torres
    Fonoaudióloga
    Comunicação, desenvolvimento e cuidado em diferentes fases da vida.
    CRFa 1-17701
    Visual: Fotografia profissional da Sônia como elemento principal.
    """
    img = Image.new("RGB", (STORY_WIDTH, STORY_HEIGHT), COLOR_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    sonia_path = os.path.join(ASSETS_DIR, "sonia_pao_de_acucar.jpeg")
    if os.path.exists(sonia_path):
        photo = Image.open(sonia_path).convert("RGBA")
        
        # Dimensões da janela da foto: 940 x 920 px
        pw, ph = 940, 920
        px, py = 70, 240
        
        # Usar ImageOps.fit com centralização equilibrada (0.65 na largura, 0.35 na altura)
        # para mostrar com nitidez e proporção 100% autêntica o rosto da Sônia e o Pão de Açúcar
        photo_fitted = ImageOps.fit(photo, (pw, ph), centering=(0.65, 0.35), method=Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (pw, ph), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, pw, ph], radius=32, fill=255)
        
        draw_card_shadow(img, [px, py, px + pw, py + ph], radius=32, shadow_color=(29, 56, 43, 30), blur=20, offset_y=10)
        img.paste(photo_fitted, (px, py), mask)
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=32, outline=COLOR_BORDER, width=2)
        
        # Badge no canto superior esquerdo da foto
        badge_font = get_font(26, 600)
        draw_pill(draw, (px + 28, py + 28), "RIO DE JANEIRO", badge_font, (255, 255, 255, 230), COLOR_DEEP_GREEN, COLOR_BORDER, 20, 10)
    
    # Cartão Editorial Inferior para os Textos
    card_x0, card_y0 = 70, 1190
    card_w, card_h = 940, 440
    card_x1, card_y1 = card_x0 + card_w, card_y0 + card_h
    
    draw_card_shadow(img, [card_x0, card_y0, card_x1, card_y1], radius=36, shadow_color=(29, 56, 43, 20), blur=24, offset_y=12)
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=36, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
    
    # Tag superior do cartão: CRFa 1-17701
    tag_font = get_font(26, 700)
    draw_pill(draw, (card_x0 + 44, card_y0 + 40), "CRFa 1-17701", tag_font, COLOR_CARD, COLOR_DEEP_GREEN, COLOR_BORDER, 20, 10)
    
    # Nome Principal: Sônia Torres
    name_font = get_font(68, 700)
    draw.text((card_x0 + 44, card_y0 + 105), "Sônia Torres", font=name_font, fill=COLOR_DEEP_GREEN)
    
    # Subtítulo: Fonoaudióloga
    sub_font = get_font(38, 600)
    draw.text((card_x0 + 46, card_y0 + 190), "Fonoaudióloga", font=sub_font, fill=COLOR_OLIVE)
    
    # Linha divisória sutil
    draw.line([card_x0 + 44, card_y0 + 255, card_x1 - 44, card_y0 + 255], fill=COLOR_BORDER, width=1)
    
    # Mensagem: Comunicação, desenvolvimento e cuidado em diferentes fases da vida.
    body_font = get_font(34, 400)
    msg = "Comunicação, desenvolvimento e cuidado em diferentes fases da vida."
    lines = wrap_text(msg, body_font, card_w - 90)
    ly = card_y0 + 285
    for line in lines:
        draw.text((card_x0 + 44, ly), line, font=body_font, fill=COLOR_CHARCOAL)
        ly += 46
        
    output_path = os.path.join(OUTPUT_DIR, "story_01_apresentacao.png")
    img.save(output_path, "PNG", quality=100)
    print(f"Salvo: {output_path}")
    return img

def generate_story_02():
    """STORY 2 — FORMAÇÃO
    Título:
    Minha formação
    Texto:
    Sou fonoaudióloga formada pela
    Universidade Federal do Rio de Janeiro — UFRJ.
    A Fonoaudiologia me permite trabalhar com algo essencial: a comunicação humana.
    Visual: Sônia em ambiente profissional, com bastante espaço negativo e excelente legibilidade.
    """
    img = Image.new("RGB", (STORY_WIDTH, STORY_HEIGHT), COLOR_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    # Topo institucional seguro (respeitando Y=220)
    tag_font = get_font(26, 700)
    draw_pill(draw, (70, 240), "TRAJETÓRIA PROFISSIONAL", tag_font, COLOR_CARD, COLOR_OLIVE, COLOR_BORDER, 24, 12)
    
    # Título: Minha formação
    title_font = get_font(76, 700)
    draw.text((70, 320), "Minha formação", font=title_font, fill=COLOR_DEEP_GREEN)
    
    # Linha decorativa
    draw.line([70, 425, 240, 425], fill=COLOR_OLIVE, width=4)
    
    # Janela fotográfica com proporção 100% PERFEITA sem distorção
    sonia_path = os.path.join(ASSETS_DIR, "sonia_pao_de_acucar.jpeg")
    if os.path.exists(sonia_path):
        photo = Image.open(sonia_path).convert("RGBA")
        
        pw, ph = 940, 530
        px, py = 70, 465
        
        # Enquadramento proporcional com foco no rosto e no jaleco profissional com bordado
        photo_fitted = ImageOps.fit(photo, (pw, ph), centering=(0.75, 0.25), method=Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (pw, ph), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, pw, ph], radius=32, fill=255)
        
        draw_card_shadow(img, [px, py, px + pw, py + ph], radius=32, shadow_color=(29, 56, 43, 20), blur=20, offset_y=10)
        img.paste(photo_fitted, (px, py), mask)
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=32, outline=COLOR_BORDER, width=2)
        
        # Selo discreto de formação
        selo_font = get_font(24, 700)
        draw_pill(draw, (px + 28, py + ph - 64), "GRADUAÇÃO EM FONOAUDIOLOGIA", selo_font, (255, 255, 255, 230), COLOR_DEEP_GREEN, COLOR_BORDER, 20, 10)
    
    # Cartão de Destaque Institucional: UFRJ
    card_x0, card_y0 = 70, 1035
    card_w, card_h = 940, 310
    card_x1, card_y1 = card_x0 + card_w, card_y0 + card_h
    
    draw_card_shadow(img, [card_x0, card_y0, card_x1, card_y1], radius=32, shadow_color=(29, 56, 43, 16), blur=20, offset_y=8)
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=32, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
    
    # Barra lateral verde institucional
    draw.rounded_rectangle([card_x0, card_y0 + 24, card_x0 + 10, card_y1 - 24], radius=5, fill=COLOR_DEEP_GREEN)
    
    t1_font = get_font(36, 400)
    draw.text((card_x0 + 44, card_y0 + 46), "Sou fonoaudióloga formada pela", font=t1_font, fill=COLOR_CHARCOAL)
    
    ufrj_font = get_font(46, 700)
    ufrj_text = "Universidade Federal do Rio de Janeiro"
    draw.text((card_x0 + 44, card_y0 + 106), ufrj_text, font=ufrj_font, fill=COLOR_DEEP_GREEN)
    
    sigla_font = get_font(46, 700)
    draw.text((card_x0 + 44, card_y0 + 170), "— UFRJ.", font=sigla_font, fill=COLOR_OLIVE)
    
    # Cartão de Reflexão Editorial: "A Fonoaudiologia me permite..."
    ref_x0, ref_y0 = 70, 1380
    ref_w, ref_h = 940, 240
    ref_x1, ref_y1 = ref_x0 + ref_w, ref_y0 + ref_h
    
    draw_card_shadow(img, [ref_x0, ref_y0, ref_x1, ref_y1], radius=32, shadow_color=(29, 56, 43, 16), blur=20, offset_y=8)
    draw.rounded_rectangle([ref_x0, ref_y0, ref_x1, ref_y1], radius=32, fill=COLOR_CARD, outline=COLOR_BORDER, width=2)
    
    # Aspas sutis decorativas
    quote_mark_font = get_font(90, 700)
    draw.text((ref_x0 + 36, ref_y0 + 10), "“", font=quote_mark_font, fill=COLOR_OLIVE)
    
    ref_font = get_font(36, 500)
    ref_msg = "A Fonoaudiologia me permite trabalhar com algo essencial: a comunicação humana."
    ref_lines = wrap_text(ref_msg, ref_font, ref_w - 110)
    ry = ref_y0 + 64
    for line in ref_lines:
        draw.text((ref_x0 + 56, ry), line, font=ref_font, fill=COLOR_CHARCOAL)
        ry += 52
        
    output_path = os.path.join(OUTPUT_DIR, "story_02_formacao.png")
    img.save(output_path, "PNG", quality=100)
    print(f"Salvo: {output_path}")
    return img

def generate_story_03():
    """STORY 3 — FORMA DE TRABALHO
    Título:
    Cada pessoa é diferente.
    Texto:
    Por isso, o atendimento começa pela escuta, pela avaliação e pela compreensão das necessidades de cada pessoa e de sua família.
    A partir daí, o cuidado é individualizado.
    Visual: Fotografia da Sônia preparando materiais ou contexto profissional. Sem pacientes identificáveis.
    """
    img = Image.new("RGB", (STORY_WIDTH, STORY_HEIGHT), COLOR_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    tag_font = get_font(26, 700)
    draw_pill(draw, (70, 240), "MÉTODO E CUIDADO", tag_font, COLOR_CARD, COLOR_OLIVE, COLOR_BORDER, 24, 12)
    
    title_font = get_font(72, 700)
    draw.text((70, 320), "Cada pessoa é diferente.", font=title_font, fill=COLOR_DEEP_GREEN)
    
    draw.line([70, 420, 260, 420], fill=COLOR_OLIVE, width=4)
    
    maos_path = os.path.join(OUTPUT_DIR, "registro_clinico_maos.jpg")
    if os.path.exists(maos_path):
        photo = Image.open(maos_path).convert("RGBA")
        pw, ph = 940, 560
        px, py = 70, 460
        
        # Enquadramento proporcional 100% perfeito
        photo_fitted = ImageOps.fit(photo, (pw, ph), centering=(0.5, 0.4), method=Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (pw, ph), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, pw, ph], radius=32, fill=255)
        
        draw_card_shadow(img, [px, py, px + pw, py + ph], radius=32, shadow_color=(29, 56, 43, 20), blur=20, offset_y=10)
        img.paste(photo_fitted, (px, py), mask)
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=32, outline=COLOR_BORDER, width=2)
        
        caption_font = get_font(24, 600)
        draw_pill(draw, (px + 28, py + ph - 64), "ESCUTA ATENTA & AVALIAÇÃO", caption_font, (255, 255, 255, 230), COLOR_DEEP_GREEN, COLOR_BORDER, 20, 10)
    
    # Cartão com Texto de Explicação
    card_x0, card_y0 = 70, 1065
    card_w, card_h = 940, 310
    card_x1, card_y1 = card_x0 + card_w, card_y0 + card_h
    
    draw_card_shadow(img, [card_x0, card_y0, card_x1, card_y1], radius=32, shadow_color=(29, 56, 43, 16), blur=20, offset_y=8)
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=32, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
    
    body_font = get_font(38, 400)
    msg1 = "Por isso, o atendimento começa pela escuta, pela avaliação e pela compreensão das necessidades de cada pessoa e de sua família."
    lines1 = wrap_text(msg1, body_font, card_w - 90)
    ly = card_y0 + 50
    for line in lines1:
        draw.text((card_x0 + 44, ly), line, font=body_font, fill=COLOR_CHARCOAL)
        ly += 54
        
    # Cartão Destaque: A partir daí, o cuidado é individualizado.
    dest_x0, dest_y0 = 70, 1410
    dest_w, dest_h = 940, 200
    dest_x1, dest_y1 = dest_x0 + dest_w, dest_y0 + dest_h
    
    draw_card_shadow(img, [dest_x0, dest_y0, dest_x1, dest_y1], radius=32, shadow_color=(29, 56, 43, 20), blur=20, offset_y=8)
    draw.rounded_rectangle([dest_x0, dest_y0, dest_x1, dest_y1], radius=32, fill=COLOR_DEEP_GREEN)
    
    draw_vector_pin_dot(draw, dest_x0 + 54, dest_y0 + 72, 8, COLOR_OLIVE)
    
    dest_font = get_font(42, 600)
    dest_text = "A partir daí, o cuidado é individualizado."
    dest_lines = wrap_text(dest_text, dest_font, dest_w - 130)
    dy = dest_y0 + 45
    for line in dest_lines:
        draw.text((dest_x0 + 84, dy), line, font=dest_font, fill=COLOR_OFFWHITE)
        dy += 54
        
    output_path = os.path.join(OUTPUT_DIR, "story_03_forma_trabalho.png")
    img.save(output_path, "PNG", quality=100)
    print(f"Salvo: {output_path}")
    return img

def generate_story_04():
    """STORY 4 — QUEM ATENDE
    Título:
    Atendimento fonoaudiológico
    Texto principal:
    Crianças • Adultos • Idosos
    Texto complementar:
    Com atenção às necessidades de comunicação, fala, linguagem e outras demandas fonoaudiológicas.
    Visual: Representar diferentes fases da vida de maneira natural e sem estereótipos.
    """
    img = Image.new("RGB", (STORY_WIDTH, STORY_HEIGHT), COLOR_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    tag_font = get_font(26, 700)
    draw_pill(draw, (70, 240), "PÚBLICO E ATUAÇÃO", tag_font, COLOR_CARD, COLOR_OLIVE, COLOR_BORDER, 24, 12)
    
    title_font = get_font(72, 700)
    draw.text((70, 320), "Atendimento\nfonoaudiológico", font=title_font, fill=COLOR_DEEP_GREEN)
    
    draw.line([70, 500, 240, 500], fill=COLOR_OLIVE, width=4)
    
    # Três pílulas refinadas
    publico_font = get_font(36, 700)
    pills = [("Crianças", 270), ("Adultos", 260), ("Idosos", 240)]
    cur_x = 70
    p_y = 530
    for name, w_box in pills:
        draw_pill(draw, (cur_x, p_y), name, publico_font, COLOR_DEEP_GREEN, COLOR_OFFWHITE, None, 36, 18)
        cur_x += w_box + 24
        
    # Fotografia autêntica multigeracional
    post_img_path = os.path.join(BASE_DIR, "POST.png")
    if os.path.exists(post_img_path):
        photo = Image.open(post_img_path).convert("RGBA")
        pw, ph = 940, 560
        px, py = 70, 640
        
        photo_fitted = ImageOps.fit(photo, (pw, ph), centering=(0.5, 0.5), method=Image.Resampling.LANCZOS)
        mask = Image.new("L", (pw, ph), 0)
        m_draw = ImageDraw.Draw(mask)
        m_draw.rounded_rectangle([0, 0, pw, ph], radius=32, fill=255)
        
        draw_card_shadow(img, [px, py, px + pw, py + ph], radius=32, shadow_color=(29, 56, 43, 20), blur=20, offset_y=10)
        img.paste(photo_fitted, (px, py), mask)
        draw.rounded_rectangle([px, py, px + pw, py + ph], radius=32, outline=COLOR_BORDER, width=2)
        
        legenda_font = get_font(24, 600)
        draw_pill(draw, (px + 28, py + ph - 64), "DIFERENTES FASES DA VIDA", legenda_font, (255, 255, 255, 230), COLOR_DEEP_GREEN, COLOR_BORDER, 20, 10)
    
    # Cartão de Texto Complementar
    card_x0, card_y0 = 70, 1250
    card_w, card_h = 940, 360
    card_x1, card_y1 = card_x0 + card_w, card_y0 + card_h
    
    draw_card_shadow(img, [card_x0, card_y0, card_x1, card_y1], radius=32, shadow_color=(29, 56, 43, 16), blur=20, offset_y=8)
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=32, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
    
    card_title_font = get_font(28, 700)
    draw.text((card_x0 + 44, card_y0 + 45), "ÁREAS DE ATENÇÃO", font=card_title_font, fill=COLOR_OLIVE)
    
    draw.line([card_x0 + 44, card_y0 + 90, card_x1 - 44, card_y0 + 90], fill=COLOR_BORDER, width=1)
    
    body_font = get_font(38, 400)
    msg = "Com atenção às necessidades de comunicação, fala, linguagem e outras demandas fonoaudiológicas."
    lines = wrap_text(msg, body_font, card_w - 90)
    ly = card_y0 + 125
    for line in lines:
        draw.text((card_x0 + 44, ly), line, font=body_font, fill=COLOR_CHARCOAL)
        ly += 56
        
    output_path = os.path.join(OUTPUT_DIR, "story_04_quem_atende.png")
    img.save(output_path, "PNG", quality=100)
    print(f"Salvo: {output_path}")
    return img

def generate_story_05():
    """STORY 5 — CHAMADA FINAL
    Título:
    Quer saber como posso ajudar?
    Texto:
    Conheça os outros destaques ou entre em contato comigo.
    Sônia Torres
    Fonoaudióloga | CRFa 1-17701
    sonia.fonosuite.com
    Visual:
    Tela simples, elegante e com hierarquia clara. Deixar uma área apropriada para inserir posteriormente o sticker de link do Instagram.
    """
    img = Image.new("RGB", (STORY_WIDTH, STORY_HEIGHT), COLOR_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    # Tag superior
    tag_font = get_font(26, 700)
    draw_pill(draw, (70, 240), "PRÓXIMO PASSO", tag_font, COLOR_CARD, COLOR_OLIVE, COLOR_BORDER, 24, 12)
    
    # Título: Quer saber como posso ajudar?
    title_font = get_font(74, 700)
    title_text = "Quer saber como\nposso ajudar?"
    draw.text((70, 320), title_text, font=title_font, fill=COLOR_DEEP_GREEN)
    
    # Linha decorativa
    draw.line([70, 520, 240, 520], fill=COLOR_OLIVE, width=4)
    
    # Subtítulo: Conheça os outros destaques ou entre em contato comigo.
    sub_font = get_font(42, 400)
    sub_msg = "Conheça os outros destaques ou entre em contato comigo."
    sub_lines = wrap_text(sub_msg, sub_font, 920)
    sy = 560
    for line in sub_lines:
        draw.text((70, sy), line, font=sub_font, fill=COLOR_CHARCOAL)
        sy += 60
        
    # ÁREA DEDICADA PARA O STICKER DE LINK DO INSTAGRAM
    # Com ícones vetoriais desenhados à mão (zero emojis com erro de renderização)
    sticker_x0, sticker_y0 = 70, 750
    sticker_w, sticker_h = 940, 360
    sticker_x1, sticker_y1 = sticker_x0 + sticker_w, sticker_y0 + sticker_h
    
    draw_card_shadow(img, [sticker_x0, sticker_y0, sticker_x1, sticker_y1], radius=36, shadow_color=(29, 56, 43, 20), blur=24, offset_y=10)
    draw.rounded_rectangle([sticker_x0, sticker_y0, sticker_x1, sticker_y1], radius=36, fill=COLOR_CARD, outline=COLOR_OLIVE, width=2)
    
    # Indicador de sticker
    st_tag_font = get_font(24, 700)
    draw_pill(draw, (sticker_x0 + 44, sticker_y0 + 36), "STICKER DE LINK DO INSTAGRAM", st_tag_font, COLOR_WHITE, COLOR_DEEP_GREEN, COLOR_BORDER, 20, 10)
    
    # Área interna do slot
    slot_x0, slot_y0 = sticker_x0 + 44, sticker_y0 + 95
    slot_w, slot_h = sticker_w - 88, 150
    slot_x1, slot_y1 = slot_x0 + slot_w, slot_y0 + slot_h
    
    draw.rounded_rectangle([slot_x0, slot_y0, slot_x1, slot_y1], radius=24, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
    
    # Ícone vetorial nítido de link
    draw_vector_link_icon(draw, slot_x0 + 60, slot_y0 + 55, 36, COLOR_DEEP_GREEN)
    
    # URL oficial
    url_font = get_font(44, 700)
    cta_hint_font = get_font(26, 500)
    draw.text((slot_x0 + 105, slot_y0 + 34), "sonia.fonosuite.com", font=url_font, fill=COLOR_DEEP_GREEN)
    draw.text((slot_x0 + 44, slot_y0 + 100), "Toque no sticker para acessar informações e agendamentos", font=cta_hint_font, fill=COLOR_MUTED)
    
    # Marcador sutil de instrução de publicação
    draw_vector_pin_dot(draw, sticker_x0 + 54, sticker_y0 + 308, 6, COLOR_OLIVE)
    hint_font = get_font(26, 500)
    draw.text((sticker_x0 + 74, sticker_y0 + 295), "Posicione aqui o sticker de link nativo do Instagram", font=hint_font, fill=COLOR_OLIVE)
    
    # Cartão de Identificação Institucional / Assinatura
    card_x0, card_y0 = 70, 1160
    card_w, card_h = 940, 440
    card_x1, card_y1 = card_x0 + card_w, card_y0 + card_h
    
    draw_card_shadow(img, [card_x0, card_y0, card_x1, card_y1], radius=36, shadow_color=(29, 56, 43, 24), blur=24, offset_y=12)
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=36, fill=COLOR_DEEP_GREEN)
    
    # Ícone de perfil no topo do cartão
    draw_profile_icon(draw, card_x0 + 80, card_y0 + 95, 76, COLOR_OFFWHITE)
    
    # Nome
    name_font = get_font(64, 700)
    draw.text((card_x0 + 145, card_y0 + 60), "Sônia Torres", font=name_font, fill=COLOR_OFFWHITE)
    
    # Cargo e Registro
    cred_font = get_font(36, 500)
    draw.text((card_x0 + 50, card_y0 + 175), "Fonoaudióloga | CRFa 1-17701", font=cred_font, fill=COLOR_CARD)
    
    # Linha divisória
    draw.line([card_x0 + 50, card_y0 + 245, card_x1 - 50, card_y0 + 245], fill=COLOR_OLIVE, width=2)
    
    # Endereço web em destaque
    site_label_font = get_font(24, 600)
    draw.text((card_x0 + 50, card_y0 + 275), "ENDEREÇO OFICIAL", font=site_label_font, fill=COLOR_CARD_ALT)
    
    site_font = get_font(48, 700)
    draw.text((card_x0 + 50, card_y0 + 325), "sonia.fonosuite.com", font=site_font, fill=COLOR_OFFWHITE)
    
    output_path = os.path.join(OUTPUT_DIR, "story_05_chamada_final.png")
    img.save(output_path, "PNG", quality=100)
    print(f"Salvo: {output_path}")
    return img

def generate_capa_destaque():
    """CAPA DO DESTAQUE "Quem é"
    Requisitos:
    - 1080 x 1080 px (e 1080 x 1920)
    - Texto: Quem é
    - Ícone minimalista de perfil/pessoa
    - Fundo verde-escuro (#1D382B)
    - Elemento em creme (#FAF7F2) ou branco
    - Área central segura para recorte circular do Instagram
    """
    capa_size = 1080
    img = Image.new("RGB", (capa_size, capa_size), COLOR_DEEP_GREEN)
    draw = ImageDraw.Draw(img)
    
    cx = capa_size // 2
    cy = capa_size // 2
    
    # Anel sutil de corte seguro (diâmetro 800 px)
    guide_r = 400
    draw.ellipse([cx - guide_r, cy - guide_r, cx + guide_r, cy + guide_r], outline=(36, 68, 52), width=3)
    
    # Anel interno sutil (diâmetro 680 px)
    inner_guide_r = 340
    draw.ellipse([cx - inner_guide_r, cy - inner_guide_r, cx + inner_guide_r, cy + inner_guide_r], outline=(44, 82, 63), width=2)
    
    # Ícone minimalista de perfil/pessoa no centro
    icon_cy = cy - 70
    icon_size = 320
    draw_profile_icon(draw, cx, icon_cy, icon_size, COLOR_OFFWHITE)
    
    # Texto "Quem é"
    texto = "Quem é"
    text_font = get_font(92, 700)
    bbox = text_font.getbbox(texto)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    tx = cx - tw // 2 - bbox[0]
    ty = cy + 140
    draw.text((tx, ty), texto, font=text_font, fill=COLOR_OFFWHITE)
    
    output_capa_sq = os.path.join(OUTPUT_DIR, "capa_destaque_quem_e.png")
    img.save(output_capa_sq, "PNG", quality=100)
    print(f"Salvo: {output_capa_sq}")
    
    # Versão Story 1080 x 1920
    story_capa = Image.new("RGB", (STORY_WIDTH, STORY_HEIGHT), COLOR_DEEP_GREEN)
    offset_y = (STORY_HEIGHT - capa_size) // 2
    story_capa.paste(img, (0, offset_y))
    
    output_capa_story = os.path.join(OUTPUT_DIR, "capa_destaque_quem_e_story.png")
    story_capa.save(output_capa_story, "PNG", quality=100)
    print(f"Salvo: {output_capa_story}")
    
    return img, story_capa

def generate_overview_board():
    """Gera prancha de alta resolução comparativa."""
    files = [
        ("Story 01: Apresentação", os.path.join(OUTPUT_DIR, "story_01_apresentacao.png")),
        ("Story 02: Formação", os.path.join(OUTPUT_DIR, "story_02_formacao.png")),
        ("Story 03: Forma de Trabalho", os.path.join(OUTPUT_DIR, "story_03_forma_trabalho.png")),
        ("Story 04: Quem Atende", os.path.join(OUTPUT_DIR, "story_04_quem_atende.png")),
        ("Story 05: Chamada Final", os.path.join(OUTPUT_DIR, "story_05_chamada_final.png")),
        ("Capa: 'Quem é'", os.path.join(OUTPUT_DIR, "capa_destaque_quem_e_story.png")),
    ]
    
    scale = 0.4
    item_w = int(STORY_WIDTH * scale)
    item_h = int(STORY_HEIGHT * scale)
    gap = 40
    pad_x = 60
    pad_y = 120
    
    total_w = pad_x * 2 + len(files) * item_w + (len(files) - 1) * gap
    total_h = pad_y * 2 + item_h + 80
    
    board = Image.new("RGB", (total_w, total_h), (242, 239, 233))
    b_draw = ImageDraw.Draw(board)
    
    header_font = get_font(52, 700)
    b_draw.text((pad_x, 40), "Destaque Instagram 'Quem é' — Sônia Torres (Fonoaudióloga • CRFa 1-17701)", font=header_font, fill=COLOR_DEEP_GREEN)
    
    sub_header_font = get_font(28, 500)
    b_draw.text((pad_x, 100), "Conjunto Completo de 5 Stories (1080x1920 px) + Capa de Destaque Circular | sonia.fonosuite.com", font=sub_header_font, fill=COLOR_OLIVE)
    
    for idx, (label, fpath) in enumerate(files):
        if os.path.exists(fpath):
            thumb = Image.open(fpath).resize((item_w, item_h), Image.Resampling.LANCZOS)
            x = pad_x + idx * (item_w + gap)
            y = pad_y + 40
            
            b_draw.rectangle([x - 3, y - 3, x + item_w + 3, y + item_h + 3], outline=COLOR_BORDER, width=2)
            board.paste(thumb, (x, y))
            
            label_font = get_font(26, 600)
            b_draw.text((x, y + item_h + 20), label, font=label_font, fill=COLOR_CHARCOAL)
            
    board_path = os.path.join(OUTPUT_DIR, "prancha_visao_geral.png")
    board.save(board_path, "PNG", quality=95)
    print(f"Prancha gerada: {board_path}")
    return board

if __name__ == "__main__":
    print("Regenerando Destaque 'Quem é' com proporções e vetores perfeitos...")
    generate_story_01()
    generate_story_02()
    generate_story_03()
    generate_story_04()
    generate_story_05()
    generate_capa_destaque()
    generate_overview_board()
    print("Concluído com sucesso!")
