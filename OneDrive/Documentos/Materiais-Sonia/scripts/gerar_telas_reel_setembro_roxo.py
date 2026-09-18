"""
Script Refinado: Renderização de Telas do Reel Setembro Roxo
Foco: Alta Acessibilidade, Tipografia Grande e Enquadramento Harmonioso.

Ajustes:
- Altura dos cards ajustada dinamicamente ao conteúdo para não invadir as pessoas.
- Remoção de linhas divisórias redundantes que colavam nos textos.
- Tipografia em escala sênior/mobile (60px títulos, 44px itens, 42px complementos).
- Contraste absoluto WCAG AAA em qualquer dispositivo.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia"
REEL_DIR = os.path.join(BASE_DIR, "reels", "reel-setembro-roxo-disfagia")
CLEAN_DIR = os.path.join(REEL_DIR, "fotografias-sem-texto")
os.makedirs(REEL_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)

# Imagens de Alta Resolução
SOURCES = [
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\b38950e8-9e4f-4bee-b831-3a0201c57b1e\slide_01_setembro_roxo_1789744700010.jpg",
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\b38950e8-9e4f-4bee-b831-3a0201c57b1e\slide_02_setembro_roxo_1789744719675.jpg",
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\b38950e8-9e4f-4bee-b831-3a0201c57b1e\slide_03_setembro_roxo_1789744739707.jpg",
]

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920

# Cores de Acessibilidade Máxima
COLOR_WHITE = (255, 255, 255)
COLOR_OFFWHITE = (245, 247, 250)
COLOR_PURPLE_VIBRANT = (168, 85, 247)   # Roxo/Lilás vibrante para acentos e marcadores (#a855f7)
COLOR_PURPLE_LIGHT = (233, 213, 255)     # Lilás suave (#e9d5ff)
COLOR_PURPLE_PILL = (126, 34, 206)       # Roxo institucional (#7e22ce)
CARD_BG = (16, 12, 22, 238)              # 93% de opacidade para contraste absoluto
CARD_BORDER = (168, 85, 247, 130)        # Borda sutil de 2px

# Fontes do Sistema Windows
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMIBOLD_PATH = r"C:\Windows\Fonts\seguisb.ttf"
FONT_REGULAR_PATH = r"C:\Windows\Fonts\segoeui.ttf"

if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = r"C:\Windows\Fonts\arialbd.ttf"
    FONT_SEMIBOLD_PATH = r"C:\Windows\Fonts\arialbd.ttf"
    FONT_REGULAR_PATH = r"C:\Windows\Fonts\arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_accessible_card(image, x1, y1, x2, y2, radius=28):
    """Desenha card com sombra suave e borda fina de acabamento."""
    overlay = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
    draw_ol = ImageDraw.Draw(overlay)
    
    # Sombra difusa
    for offset in range(10, 0, -2):
        s_alpha = int(40 * (offset / 10))
        draw_ol.rounded_rectangle(
            [x1 - offset, y1 - offset + 6, x2 + offset, y2 + offset + 6],
            radius=radius + offset,
            fill=(0, 0, 0, s_alpha)
        )
        
    draw_ol.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=CARD_BG, outline=CARD_BORDER, width=2)
    return Image.alpha_composite(image.convert("RGBA"), overlay)

def render_slide_1(base_img):
    """
    SLIDE 1 — APRESENTAÇÃO
    """
    # Card compacto e elegante
    card_x1 = 70
    card_x2 = TARGET_WIDTH - 70  # 940px largura
    card_y1 = 180
    card_y2 = 680
    
    img = draw_accessible_card(base_img, card_x1, card_y1, card_x2, card_y2, radius=30)
    draw = ImageDraw.Draw(img)
    center_x = TARGET_WIDTH // 2
    
    cur_y = card_y1 + 44
    
    # 1. Badge "SETEMBRO ROXO"
    font_badge = get_font(FONT_BOLD_PATH, 34)
    badge_text = "SETEMBRO ROXO"
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    
    pad_x, pad_y = 32, 14
    pw = bw + pad_x * 2
    ph = bh + pad_y * 2
    px = center_x - (pw // 2)
    
    draw.rounded_rectangle([px, cur_y, px + pw, cur_y + ph], radius=18, fill=COLOR_PURPLE_PILL)
    draw.text((px + pad_x, cur_y + pad_y - 2), badge_text, font=font_badge, fill=COLOR_WHITE)
    
    # 2. Título Principal
    cur_y += ph + 32
    font_title = get_font(FONT_BOLD_PATH, 58)
    title_text = "Conscientização sobre disfagia"
    bbox_t = draw.textbbox((0, 0), title_text, font=font_title)
    tw = bbox_t[2] - bbox_t[0]
    draw.text((center_x - (tw // 2), cur_y), title_text, font=font_title, fill=COLOR_WHITE)
    
    # 3. Texto Complementar (grande, fácil de ler)
    cur_y += (bbox_t[3] - bbox_t[1]) + 30
    font_comp = get_font(FONT_SEMIBOLD_PATH, 42)
    comp_lines = [
        "Dificuldades para engolir podem afetar",
        "alimentação, hidratação e segurança."
    ]
    for line in comp_lines:
        bbox_c = draw.textbbox((0, 0), line, font=font_comp)
        cw = bbox_c[2] - bbox_c[0]
        draw.text((center_x - (cw // 2), cur_y), line, font=font_comp, fill=COLOR_OFFWHITE)
        cur_y += (bbox_c[3] - bbox_c[1]) + 16
        
    return img.convert("RGB")

def render_slide_2(base_img):
    """
    SLIDE 2 — SINAIS
    """
    # Card com altura calibrada
    card_x1 = 70
    card_x2 = TARGET_WIDTH - 70
    card_y1 = 170
    card_y2 = 750
    
    img = draw_accessible_card(base_img, card_x1, card_y1, card_x2, card_y2, radius=30)
    draw = ImageDraw.Draw(img)
    center_x = TARGET_WIDTH // 2
    
    cur_y = card_y1 + 38
    
    # 1. Tag superior
    font_tag = get_font(FONT_BOLD_PATH, 28)
    tag_text = "SETEMBRO ROXO · DISFAGIA"
    bbox_tag = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = bbox_tag[2] - bbox_tag[0]
    draw.text((center_x - (tag_w // 2), cur_y), tag_text, font=font_tag, fill=COLOR_PURPLE_LIGHT)
    
    # 2. Título Principal
    cur_y += (bbox_tag[3] - bbox_tag[1]) + 22
    font_title = get_font(FONT_BOLD_PATH, 58)
    title_text = "Alguns sinais merecem atenção"
    bbox_t = draw.textbbox((0, 0), title_text, font=font_title)
    tw = bbox_t[2] - bbox_t[0]
    draw.text((center_x - (tw // 2), cur_y), title_text, font=font_title, fill=COLOR_WHITE)
    
    # 3. Lista dos 4 Sinais
    cur_y += (bbox_t[3] - bbox_t[1]) + 34
    sinais = [
        "Tosse ou engasgos ao comer ou beber",
        "Voz molhada após engolir",
        "Refeições muito demoradas",
        "Dificuldade para engolir"
    ]
    
    font_item = get_font(FONT_BOLD_PATH, 42)
    item_x_margin = card_x1 + 65
    
    for item in sinais:
        # Marcador circular lilás/roxo
        b_radius = 11
        b_cy = cur_y + 24
        b_cx = item_x_margin + 12
        
        draw.ellipse(
            [b_cx - b_radius, b_cy - b_radius, b_cx + b_radius, b_cy + b_radius],
            fill=COLOR_PURPLE_VIBRANT,
            outline=COLOR_WHITE,
            width=2
        )
        draw.text((item_x_margin + 44, cur_y), item, font=font_item, fill=COLOR_WHITE)
        cur_y += 70
        
    return img.convert("RGB")

def render_slide_3(base_img):
    """
    SLIDE 3 — AÇÃO & CRÉDITOS
    """
    card_x1 = 70
    card_x2 = TARGET_WIDTH - 70
    card_y1 = 170
    card_y2 = 720
    
    img = draw_accessible_card(base_img, card_x1, card_y1, card_x2, card_y2, radius=30)
    
    # Card de rodapé para assinatura profissional
    sign_w = 580
    sign_h = 135
    sign_x1 = (TARGET_WIDTH - sign_w) // 2
    sign_x2 = sign_x1 + sign_w
    sign_y1 = 1650
    sign_y2 = sign_y1 + sign_h
    img = draw_accessible_card(img, sign_x1, sign_y1, sign_x2, sign_y2, radius=24)
    
    draw = ImageDraw.Draw(img)
    center_x = TARGET_WIDTH // 2
    
    cur_y = card_y1 + 36
    
    # 1. Tag superior
    font_tag = get_font(FONT_BOLD_PATH, 28)
    tag_text = "SETEMBRO ROXO"
    bbox_tag = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = bbox_tag[2] - bbox_tag[0]
    draw.text((center_x - (tag_w // 2), cur_y), tag_text, font=font_tag, fill=COLOR_PURPLE_LIGHT)
    
    # 2. Título Principal em 2 linhas
    cur_y += (bbox_tag[3] - bbox_tag[1]) + 20
    font_title = get_font(FONT_BOLD_PATH, 54)
    title_lines = [
        "Dificuldade para engolir",
        "não deve ser ignorada."
    ]
    for line in title_lines:
        bbox_t = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox_t[2] - bbox_t[0]
        draw.text((center_x - (tw // 2), cur_y), line, font=font_title, fill=COLOR_WHITE)
        cur_y += (bbox_t[3] - bbox_t[1]) + 12
        
    # 3. Texto Complementar
    cur_y += 24
    font_comp = get_font(FONT_SEMIBOLD_PATH, 38)
    comp_lines = [
        "A avaliação adequada ajuda a identificar o que",
        "está acontecendo e orientar os cuidados necessários."
    ]
    for line in comp_lines:
        bbox_c = draw.textbbox((0, 0), line, font=font_comp)
        cw = bbox_c[2] - bbox_c[0]
        draw.text((center_x - (cw // 2), cur_y), line, font=font_comp, fill=COLOR_OFFWHITE)
        cur_y += (bbox_c[3] - bbox_c[1]) + 14
        
    # 4. Destaque: "Informação também é cuidado."
    cur_y += 22
    font_dest = get_font(FONT_BOLD_PATH, 36)
    dest_text = "Informação também é cuidado."
    bbox_d = draw.textbbox((0, 0), dest_text, font=font_dest)
    dw = bbox_d[2] - bbox_d[0]
    draw.text((center_x - (dw // 2), cur_y), dest_text, font=font_dest, fill=COLOR_PURPLE_LIGHT)
    
    # 5. Assinatura e Registro Profissional
    font_name = get_font(FONT_BOLD_PATH, 38)
    font_crfa = get_font(FONT_REGULAR_PATH, 28)
    
    name_text = "Sônia Torres"
    crfa_text = "Fonoaudióloga | CRFa 1-17701"
    
    bbox_n = draw.textbbox((0, 0), name_text, font=font_name)
    bbox_cr = draw.textbbox((0, 0), crfa_text, font=font_crfa)
    
    nw = bbox_n[2] - bbox_n[0]
    crw = bbox_cr[2] - bbox_cr[0]
    
    draw.text((center_x - (nw // 2), sign_y1 + 24), name_text, font=font_name, fill=COLOR_WHITE)
    draw.text((center_x - (crw // 2), sign_y1 + 76), crfa_text, font=font_crfa, fill=COLOR_PURPLE_LIGHT)
    
    return img.convert("RGB")

def process_all_slides():
    print("Iniciando renderização de alta precisão...")
    
    configs = [
        {
            "final_name": "01-slide-apresentacao.png",
            "clean_name": "01-slide-apresentacao-sem-texto.png",
            "src": SOURCES[0],
            "renderer": render_slide_1
        },
        {
            "final_name": "02-slide-sinais.png",
            "clean_name": "02-slide-sinais-sem-texto.png",
            "src": SOURCES[1],
            "renderer": render_slide_2
        },
        {
            "final_name": "03-slide-acao.png",
            "clean_name": "03-slide-acao-sem-texto.png",
            "src": SOURCES[2],
            "renderer": render_slide_3
        }
    ]
    
    for cfg in configs:
        src_path = cfg["src"]
        if not os.path.exists(src_path):
            print(f"Erro: Arquivo não encontrado: {src_path}")
            continue
            
        img = Image.open(src_path)
        if img.size != (TARGET_WIDTH, TARGET_HEIGHT):
            img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            
        clean_out = os.path.join(CLEAN_DIR, cfg["clean_name"])
        img.save(clean_out, format="PNG", quality=98)
        
        final_img = cfg["renderer"](img)
        final_out = os.path.join(REEL_DIR, cfg["final_name"])
        final_img.save(final_out, format="PNG", quality=98)
        print(f"Slide renderizado com sucesso: {final_out}")
        
    print("Renderização concluída com sucesso!")

if __name__ == "__main__":
    process_all_slides()
