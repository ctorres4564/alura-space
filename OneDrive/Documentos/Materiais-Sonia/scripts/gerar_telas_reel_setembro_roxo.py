"""
Script para processamento e composição gráfica dos 3 slides do Reel:
Campanha Setembro Roxo — Conscientização sobre Disfagia
Fonoaudióloga Sônia Torres (CRFa 1-17701)

Gera:
1. Fotografias limpas (sem texto) em 1080 x 1920 px (9:16) para uso flexível
2. Telas finais diagramadas rigorosamente dentro da Safe Zone do Instagram Reel
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia"
REEL_DIR = os.path.join(BASE_DIR, "reels", "reel-setembro-roxo-disfagia")
CLEAN_DIR = os.path.join(REEL_DIR, "fotografias-sem-texto")
os.makedirs(REEL_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)

# Imagens geradas via IA (Alta Resolução Documental)
SOURCES = [
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\b38950e8-9e4f-4bee-b831-3a0201c57b1e\slide_01_setembro_roxo_1789744700010.jpg",
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\b38950e8-9e4f-4bee-b831-3a0201c57b1e\slide_02_setembro_roxo_1789744719675.jpg",
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\b38950e8-9e4f-4bee-b831-3a0201c57b1e\slide_03_setembro_roxo_1789744739707.jpg",
]

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920

# Paleta de Cores Sofisticada
PURPLE_PRIMARY = (112, 44, 142)      # Roxo Setembro Roxo elegante / sóbrio
PURPLE_ACCENT = (142, 68, 173)       # Roxo vivo para detalhes
PURPLE_LIGHT = (244, 238, 250)       # Creme lilás suave para fundos de tags
PURPLE_TEXT = (88, 28, 118)          # Roxo profundo para texto de tag
WHITE = (255, 255, 255)
CREAM = (248, 246, 242)              # Bege/Creme quente
OFF_WHITE = (235, 233, 230)
DARK_TEXT = (28, 28, 30)             # Grafite profundo para legibilidade em cards
MUTED_TEXT = (95, 95, 100)
CARD_BG = (255, 255, 255, 235)       # Branco translúcido sofisticado
CARD_BORDER = (225, 220, 232, 200)

# Fontes do Sistema Windows
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMIBOLD_PATH = r"C:\Windows\Fonts\segoeuisl.ttf"
FONT_REGULAR_PATH = r"C:\Windows\Fonts\segoeui.ttf"

if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = r"C:\Windows\Fonts\arialbd.ttf"
    FONT_REGULAR_PATH = r"C:\Windows\Fonts\arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def apply_top_protection_gradient(image, height=780, max_alpha=180):
    """
    Aplica um gradiente escurecido suave e natural no terço superior,
    garantindo contraste absoluto para a tipografia sem descaracterizar a foto.
    """
    overlay = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
    draw_ol = ImageDraw.Draw(overlay)
    
    for y in range(height):
        ratio = 1.0 - (y / height)
        alpha = int(max_alpha * (ratio ** 1.35))
        draw_ol.line([(0, y), (TARGET_WIDTH, y)], fill=(15, 15, 18, alpha))
        
    return Image.alpha_composite(image.convert("RGBA"), overlay)

def draw_text_with_shadow(draw, text, x, y, font, fill=WHITE, shadow_color=(0, 0, 0, 160), shadow_offset=(0, 2)):
    ox, oy = shadow_offset
    draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)

def render_slide_1(base_img):
    """
    SLIDE 1 — APRESENTAÇÃO
    Texto Principal: 'SETEMBRO ROXO'
    Abaixo: 'Conscientização sobre disfagia'
    Texto Complementar: 'Dificuldades para engolir podem afetar alimentação, hidratação e segurança.'
    """
    img = apply_top_protection_gradient(base_img, height=750, max_alpha=175)
    draw = ImageDraw.Draw(img)
    
    # Safe zone: X centralizado com margem segura de 100px (largura útil = 880px)
    # Posição Y começando em 250px (bem abaixo do topo do Reel)
    start_y = 260
    
    # 1. Badge "SETEMBRO ROXO" em pill com roxo nobre
    font_badge = get_font(FONT_BOLD_PATH, 28)
    badge_text = "SETEMBRO ROXO"
    bbox_b = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    
    pad_x = 24
    pad_y = 12
    badge_w = bw + pad_x * 2
    badge_h = bh + pad_y * 2
    bx = (TARGET_WIDTH - badge_w) // 2
    by = start_y
    
    # Fundo do badge roxo da campanha
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=16, fill=PURPLE_PRIMARY)
    draw.text((bx + pad_x, by + pad_y - 2), badge_text, font=font_badge, fill=WHITE)
    
    # 2. Subtítulo: "Conscientização sobre disfagia"
    font_sub = get_font(FONT_BOLD_PATH, 44)
    sub_text = "Conscientização sobre disfagia"
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw = bbox_sub[2] - bbox_sub[0]
    sx = (TARGET_WIDTH - sw) // 2
    sy = by + badge_h + 30
    draw_text_with_shadow(draw, sub_text, sx, sy, font_sub, fill=WHITE)
    
    # Linha decorativa roxa minimalista
    line_w = 80
    lx = (TARGET_WIDTH - line_w) // 2
    ly = sy + (bbox_sub[3] - bbox_sub[1]) + 24
    draw.line([(lx, ly), (lx + line_w, ly)], fill=PURPLE_ACCENT, width=4)
    
    # 3. Texto Complementar com quebra harmoniosa
    font_comp = get_font(FONT_REGULAR_PATH, 34)
    comp_lines = [
        "Dificuldades para engolir podem afetar",
        "alimentação, hidratação e segurança."
    ]
    
    cy = ly + 26
    for line in comp_lines:
        bbox_c = draw.textbbox((0, 0), line, font=font_comp)
        cw = bbox_c[2] - bbox_c[0]
        cx = (TARGET_WIDTH - cw) // 2
        draw_text_with_shadow(draw, line, cx, cy, font_comp, fill=CREAM, shadow_offset=(0, 2))
        cy += (bbox_c[3] - bbox_c[1]) + 14
        
    return img.convert("RGB")

def render_slide_2(base_img):
    """
    SLIDE 2 — SINAIS
    Título: 'Alguns sinais merecem atenção'
    4 Itens:
    - Tosse ou engasgos ao comer ou beber
    - Voz molhada após engolir
    - Refeições muito demoradas
    - Dificuldade para engolir
    """
    img = apply_top_protection_gradient(base_img, height=880, max_alpha=190)
    draw = ImageDraw.Draw(img)
    
    start_y = 240
    
    # Tag identificadora discreta
    font_tag = get_font(FONT_BOLD_PATH, 22)
    tag_text = "SETEMBRO ROXO · DISFAGIA"
    bbox_t = draw.textbbox((0, 0), tag_text, font=font_tag)
    tw = bbox_t[2] - bbox_t[0]
    draw_text_with_shadow(draw, tag_text, (TARGET_WIDTH - tw) // 2, start_y, font_tag, fill=(215, 185, 235))
    
    # Título Principal
    font_title = get_font(FONT_BOLD_PATH, 46)
    title_text = "Alguns sinais merecem atenção"
    bbox_title = draw.textbbox((0, 0), title_text, font=font_title)
    ti_w = bbox_title[2] - bbox_title[0]
    ti_x = (TARGET_WIDTH - ti_w) // 2
    ti_y = start_y + 40
    draw_text_with_shadow(draw, title_text, ti_x, ti_y, font_title, fill=WHITE)
    
    # Linha divisora sutil
    line_w = 60
    lx = (TARGET_WIDTH - line_w) // 2
    ly = ti_y + (bbox_title[3] - bbox_title[1]) + 24
    draw.line([(lx, ly), (lx + line_w, ly)], fill=PURPLE_ACCENT, width=3)
    
    # Itens / Sinais em lista vertical limpa com marcadores roxos sofisticados
    sinais = [
        "Tosse ou engasgos ao comer ou beber",
        "Voz molhada após engolir",
        "Refeições muito demoradas",
        "Dificuldade para engolir"
    ]
    
    font_item = get_font(FONT_BOLD_PATH, 34)
    item_y = ly + 36
    margin_left = 130  # Seguro contra margens de corte do Reels
    
    for item in sinais:
        # Pílula/bullet roxo elegante
        bullet_radius = 8
        bullet_cy = item_y + 20
        bullet_cx = margin_left + 10
        draw.ellipse(
            [bullet_cx - bullet_radius, bullet_cy - bullet_radius, bullet_cx + bullet_radius, bullet_cy + bullet_radius],
            fill=PURPLE_ACCENT,
            outline=WHITE,
            width=2
        )
        
        # Texto do sinal
        draw_text_with_shadow(draw, item, margin_left + 38, item_y, font_item, fill=CREAM, shadow_offset=(0, 2))
        item_y += 62
        
    return img.convert("RGB")

def render_slide_3(base_img):
    """
    SLIDE 3 — AÇÃO & CRÉDITOS
    Título Principal: 'Dificuldade para engolir não deve ser ignorada.'
    Texto Complementar: 'A avaliação adequada ajuda a identificar o que está acontecendo e orientar os cuidados necessários.'
    Em menor destaque: 'Informação também é cuidado.'
    Rodapé:
    Sônia Torres
    Fonoaudióloga | CRFa 1-17701
    """
    # Aplicar gradiente superior para o texto e sutil proteção inferior para a assinatura segura
    img = apply_top_protection_gradient(base_img, height=840, max_alpha=185)
    
    # Proteção de rodapé muito suave apenas para garantia do CRFa
    overlay_bot = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
    draw_bot = ImageDraw.Draw(overlay_bot)
    bot_start = 1600
    for y in range(bot_start, TARGET_HEIGHT):
        ratio = (y - bot_start) / (TARGET_HEIGHT - bot_start)
        alpha = int(140 * ratio)
        draw_bot.line([(0, y), (TARGET_WIDTH, y)], fill=(15, 15, 18, alpha))
    img = Image.alpha_composite(img, overlay_bot)
    
    draw = ImageDraw.Draw(img)
    
    start_y = 240
    
    # Badge superior sutil
    font_tag = get_font(FONT_BOLD_PATH, 22)
    tag_text = "SETEMBRO ROXO"
    bbox_t = draw.textbbox((0, 0), tag_text, font=font_tag)
    tw = bbox_t[2] - bbox_t[0]
    draw_text_with_shadow(draw, tag_text, (TARGET_WIDTH - tw) // 2, start_y, font_tag, fill=(215, 185, 235))
    
    # Título Principal (2 linhas bem calibradas)
    font_title = get_font(FONT_BOLD_PATH, 44)
    title_lines = [
        "Dificuldade para engolir",
        "não deve ser ignorada."
    ]
    
    ty = start_y + 40
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        lw = bbox[2] - bbox[0]
        lx = (TARGET_WIDTH - lw) // 2
        draw_text_with_shadow(draw, line, lx, ty, font_title, fill=WHITE)
        ty += (bbox[3] - bbox[1]) + 12
        
    # Linha roxa central
    line_w = 70
    lx = (TARGET_WIDTH - line_w) // 2
    ly = ty + 18
    draw.line([(lx, ly), (lx + line_w, ly)], fill=PURPLE_ACCENT, width=4)
    
    # Texto Complementar
    font_comp = get_font(FONT_REGULAR_PATH, 32)
    comp_lines = [
        "A avaliação adequada ajuda a identificar o que",
        "está acontecendo e orientar os cuidados necessários."
    ]
    
    cy = ly + 28
    for line in comp_lines:
        bbox_c = draw.textbbox((0, 0), line, font=font_comp)
        cw = bbox_c[2] - bbox_c[0]
        cx = (TARGET_WIDTH - cw) // 2
        draw_text_with_shadow(draw, line, cx, cy, font_comp, fill=CREAM)
        cy += (bbox_c[3] - bbox_c[1]) + 12
        
    # Destaque adicional em menor ênfase: "Informação também é cuidado."
    font_dest = get_font(FONT_BOLD_PATH, 28)
    dest_text = "Informação também é cuidado."
    bbox_d = draw.textbbox((0, 0), dest_text, font=font_dest)
    dw = bbox_d[2] - bbox_d[0]
    dx = (TARGET_WIDTH - dw) // 2
    dy = cy + 18
    draw_text_with_shadow(draw, dest_text, dx, dy, font_dest, fill=(228, 205, 245))
    
    # --- ASSINATURA / CRÉDITOS NO RODAPÉ SEGURO ---
    # Safe zone inferior: Posicionado em torno de Y = 1680px (acima dos 240px finais que o Instagram usa para legenda e áudio)
    sign_y = 1690
    font_name = get_font(FONT_BOLD_PATH, 30)
    font_crfa = get_font(FONT_REGULAR_PATH, 24)
    
    name_text = "Sônia Torres"
    crfa_text = "Fonoaudióloga | CRFa 1-17701"
    
    bbox_n = draw.textbbox((0, 0), name_text, font=font_name)
    bbox_cr = draw.textbbox((0, 0), crfa_text, font=font_crfa)
    
    nw = bbox_n[2] - bbox_n[0]
    crw = bbox_cr[2] - bbox_cr[0]
    
    draw_text_with_shadow(draw, name_text, (TARGET_WIDTH - nw) // 2, sign_y, font_name, fill=WHITE)
    draw_text_with_shadow(draw, crfa_text, (TARGET_WIDTH - crw) // 2, sign_y + (bbox_n[3] - bbox_n[1]) + 8, font_crfa, fill=CREAM)
    
    return img.convert("RGB")

def process_all_slides():
    print("Iniciando processamento dos 3 slides do Reel de Setembro Roxo...")
    
    configs = [
        {
            "num": "01",
            "clean_name": "01-slide-apresentacao-sem-texto.png",
            "final_name": "01-slide-apresentacao.png",
            "src": SOURCES[0],
            "renderer": render_slide_1
        },
        {
            "num": "02",
            "clean_name": "02-slide-sinais-sem-texto.png",
            "final_name": "02-slide-sinais.png",
            "src": SOURCES[1],
            "renderer": render_slide_2
        },
        {
            "num": "03",
            "clean_name": "03-slide-acao-sem-texto.png",
            "final_name": "03-slide-acao.png",
            "src": SOURCES[2],
            "renderer": render_slide_3
        }
    ]
    
    for cfg in configs:
        src_path = cfg["src"]
        if not os.path.exists(src_path):
            print(f"Erro: Arquivo de origem não encontrado: {src_path}")
            continue
            
        img = Image.open(src_path)
        
        # Garantir proporção 1080 x 1920
        if img.size != (TARGET_WIDTH, TARGET_HEIGHT):
            img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            
        # 1. Salvar versão limpa sem texto
        clean_out = os.path.join(CLEAN_DIR, cfg["clean_name"])
        img.save(clean_out, format="PNG", quality=98)
        print(f"Versão limpa salva: {clean_out}")
        
        # 2. Renderizar versão diagramada com texto e safe zone
        final_img = cfg["renderer"](img)
        final_out = os.path.join(REEL_DIR, cfg["final_name"])
        final_img.save(final_out, format="PNG", quality=98)
        print(f"Slide final renderizado: {final_out}")
        
    print("Todos os slides foram processados com sucesso!")

if __name__ == "__main__":
    process_all_slides()
