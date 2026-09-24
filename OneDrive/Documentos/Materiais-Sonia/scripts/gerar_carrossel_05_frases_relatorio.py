"""
Script de Produção Automatizada — Carrossel Instagram 4:5 (1080 x 1350 px)
Carrossel: "5 frases de um relatório fonoaudiológico que precisam ser bem explicadas"
Cliente: Sônia Torres — Fonoaudióloga (CRFa 1-17701 | @torresdafono)
Direção de Arte: Editorial brasileiro contemporâneo, acolhedor e clínico, com diversidade autêntica.

Gera:
1. Cópias das fotos brutas em: carrosseis/carrossel-05-frases-relatorio/raw-photos/
2. Slides finais em: carrosseis/carrossel-05-frases-relatorio/slides-finais/ (01 a 07 em PNG 1080x1350)
3. Prancha de visualização comparativa: carrosseis/carrossel-05-frases-relatorio/slides-finais/prancha-visao-geral.png
"""

import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# Diretórios
BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia"
RAW_DIR = os.path.join(BASE_DIR, "carrosseis", "carrossel-05-frases-relatorio", "raw-photos")
FINAL_DIR = os.path.join(BASE_DIR, "carrosseis", "carrossel-05-frases-relatorio", "slides-finais")
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "PlusJakartaSans-Variable.ttf")
BRAIN_DIR = r"C:\Users\Gamer\.gemini\antigravity-ide\brain\0fb4ba9f-15fc-4f5b-a5ab-f2cbc9333f96"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

# Mapeamento das imagens geradas
RAW_IMAGES_SOURCE = [
    ("01-capa.jpg", os.path.join(BRAIN_DIR, "capa_fono_brasileira_negra_1790238573340.jpg")),
    ("02-frase-01.jpg", os.path.join(BRAIN_DIR, "registro_clinico_maos_pardas_1790238610546.jpg")),
    ("03-frase-02.jpg", os.path.join(BRAIN_DIR, "interacao_crianca_negra_livro_1790238650562.jpg")),
    ("04-frase-03.jpg", os.path.join(BRAIN_DIR, "observacao_crianca_parda_brinquedo_1790238694411.jpg")),
    ("05-frase-04.jpg", os.path.join(BRAIN_DIR, "materiais_clinicos_frutas_brasil_1790238743083.jpg")),
    ("06-frase-05.jpg", os.path.join(BRAIN_DIR, "dialogo_fono_mae_brasileira_1790238795265.jpg")),
    ("07-fechamento.jpg", os.path.join(BRAIN_DIR, "consultorio_fono_brasil_respiro_1790238853169.jpg")),
]

# Copiar fotos para a pasta oficial do carrossel
for filename, src in RAW_IMAGES_SOURCE:
    dest = os.path.join(RAW_DIR, filename)
    if os.path.exists(src):
        shutil.copy2(src, dest)
        print(f"Copiada foto: {filename}")
    else:
        print(f"AVISO: Arquivo de origem não encontrado: {src}")

# Paleta Cromática Editorial
COLOR_BG_OFFWHITE = (250, 247, 242)      # #FAF7F2 - Fundo geral acolhedor
COLOR_BG_CARD = (244, 239, 232)          # #F4EFE8 - Fundo de cartões sutis
COLOR_DEEP_GREEN = (29, 56, 43)          # #1D382B - Verde Petróleo Profundo
COLOR_OLIVE = (68, 99, 75)               # #44634B - Verde Oliva Clínico
COLOR_CORAL = (196, 84, 46)              # #C4542E - Terracota / Coral Destaque
COLOR_CHARCOAL = (46, 44, 41)            # #2E2C29 - Grafite Texto
COLOR_MUTED_GRAY = (112, 107, 100)       # #706B64 - Texto secundário/apoio
COLOR_BORDER_LIGHT = (226, 219, 208)     # #E2DBD0 - Linha sutil divisória
COLOR_WHITE = (255, 255, 255)

WIDTH = 1080
HEIGHT = 1350

# Carregador de fontes com fallback
def get_font(size, weight=400):
    try:
        font = ImageFont.truetype(FONT_PATH, size)
        if hasattr(font, 'set_variation_by_axes'):
            font.set_variation_by_axes([weight])
        return font
    except Exception:
        # Fallback Windows fonts
        if weight >= 700 and os.path.exists(r"C:\Windows\Fonts\segoeuib.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", size)
        elif weight >= 600 and os.path.exists(r"C:\Windows\Fonts\seguisb.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\seguisb.ttf", size)
        elif os.path.exists(r"C:\Windows\Fonts\segoeui.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", size)
        return ImageFont.load_default()

# Utilitário: Quebra de texto inteligente por largura máxima
def wrap_text(text, font, max_width, draw):
    lines = []
    paragraphs = text.split('\n')
    for p in paragraphs:
        if not p.strip():
            lines.append("")
            continue
        words = p.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(' '.join(current_line))
    return lines

# Utilitário: Desenhar Badge em Cápsula
def draw_badge(draw, text, x, y, bg_color=COLOR_CORAL, text_color=COLOR_WHITE, font_size=24, padding_x=22, padding_y=10):
    font = get_font(font_size, 700)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    bw = tw + padding_x * 2
    bh = th + padding_y * 2 + 4
    
    # Desenhar retângulo arredondado (pílula)
    radius = bh // 2
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=radius, fill=bg_color)
    
    # Centralizar texto
    tx = x + padding_x
    ty = y + padding_y - (bbox[1])
    draw.text((tx, ty), text, fill=text_color, font=font)
    return bw, bh

# Utilitário: Desenhar Cabeçalho Superior Padrão (Safe Area Y: 90 a 160)
def draw_header(draw, slide_num, total=7, category="RELATÓRIO FONOAUDIOLÓGICO"):
    font_cat = get_font(20, 700)
    font_meta = get_font(20, 600)
    
    # Categoria à esquerda
    draw.text((90, 95), category.upper(), fill=COLOR_OLIVE, font=font_cat)
    
    # Paginação à direita
    page_text = f"{slide_num:02d} / {total:02d}"
    bbox = draw.textbbox((0, 0), page_text, font=font_meta)
    pw = bbox[2] - bbox[0]
    draw.text((WIDTH - 90 - pw, 95), page_text, fill=COLOR_MUTED_GRAY, font=font_meta)
    
    # Linha divisória sutil
    draw.line([(90, 132), (WIDTH - 90, 132)], fill=COLOR_BORDER_LIGHT, width=1)

# Utilitário: Desenhar Rodapé Padrão (Safe Area Y: 1240 a 1280)
def draw_footer(draw, is_cover=False, is_closing=False):
    font_brand = get_font(20, 600)
    font_crfa = get_font(18, 500)
    
    # Linha divisória sutil
    draw.line([(90, 1230), (WIDTH - 90, 1230)], fill=COLOR_BORDER_LIGHT, width=1)
    
    # Identificação profissional
    draw.text((90, 1250), "Sônia Torres", fill=COLOR_DEEP_GREEN, font=font_brand)
    bbox_name = draw.textbbox((0, 0), "Sônia Torres", font=font_brand)
    nw = bbox_name[2] - bbox_name[0]
    draw.text((90 + nw + 12, 1252), "•  Fonoaudióloga  |  CRFa 1-17701", fill=COLOR_MUTED_GRAY, font=font_crfa)
    
    if is_cover:
        cta_text = "Arraste para o lado  →"
        font_cta = get_font(20, 700)
        bbox_cta = draw.textbbox((0, 0), cta_text, font=font_cta)
        cw = bbox_cta[2] - bbox_cta[0]
        draw.text((WIDTH - 90 - cw, 1250), cta_text, fill=COLOR_CORAL, font=font_cta)
    elif not is_closing:
        handle = "@torresdafono"
        bbox_h = draw.textbbox((0, 0), handle, font=font_brand)
        hw = bbox_h[2] - bbox_h[0]
        draw.text((WIDTH - 90 - hw, 1250), handle, fill=COLOR_OLIVE, font=font_brand)

# Utilitário: Recortar e Inserir Imagem Arredondada com Sombra Suave
def insert_image_with_radius(base_img, img_path, box, radius=24, add_shadow=True):
    if not os.path.exists(img_path):
        return
    x, y, w, h = box
    raw = Image.open(img_path).convert("RGB")
    
    # Crop centralizado proporcional
    raw_fitted = ImageOps.fit(raw, (w, h), Image.Resampling.LANCZOS)
    
    # Criar máscara arredondada
    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    
    # Sombra sutil
    if add_shadow:
        shadow_w = w + 20
        shadow_h = h + 20
        shadow = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.rounded_rectangle([10, 14, 10 + w, 14 + h], radius=radius, fill=(0, 0, 0, 32))
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        base_img.paste(shadow, (x - 10, y - 6), shadow)
    
    # Colar imagem recortada com máscara
    base_img.paste(raw_fitted, (x, y), mask)

# ==============================================================================
# RENDERIZAÇÃO DOS SLIDES
# ==============================================================================

def render_slide_01_capa():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, 1, 7, "SÉRIE RELATÓRIOS CLÍNICOS")
    
    # Badge
    draw_badge(draw, "RELATÓRIO FONOAUDIOLÓGICO", 90, 165, bg_color=COLOR_CORAL, font_size=22)
    
    # Título Principal
    font_title = get_font(58, 800)
    title_text = "5 frases de um relatório\nfonoaudiológico que\nprecisam ser bem explicadas"
    lines = title_text.split('\n')
    
    curr_y = 240
    for line in lines:
        if "5 frases" in line:
            # Destacar "5 frases" em terracota
            words = line.split(" de um relatório")
            draw.text((90, curr_y), words[0], fill=COLOR_CORAL, font=font_title)
            bbox = draw.textbbox((0, 0), words[0], font=font_title)
            w5 = bbox[2] - bbox[0]
            draw.text((90 + w5, curr_y), " de um relatório", fill=COLOR_DEEP_GREEN, font=font_title)
        else:
            draw.text((90, curr_y), line, fill=COLOR_DEEP_GREEN, font=font_title)
        curr_y += 72
        
    # Subtítulo
    curr_y += 12
    font_sub = get_font(32, 500)
    sub_text = "Porque uma conclusão sozinha pode dizer muito pouco."
    draw.text((90, curr_y), sub_text, fill=COLOR_MUTED_GRAY, font=font_sub)
    
    # Imagem de Capa (Fonoaudióloga Negra em consultório brasileiro)
    # Box de Y: 560 a 1200 (altura: 640px, largura: 900px)
    foto_path = os.path.join(RAW_DIR, "01-capa.jpg")
    insert_image_with_radius(img, foto_path, (90, 555, 900, 645), radius=28)
    
    draw_footer(draw, is_cover=True)
    
    out_path = os.path.join(FINAL_DIR, "01-capa.png")
    img.save(out_path, "PNG", quality=100)
    print(f"Gerado: {out_path}")


def render_slide_02_frase_01():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, 2, 7)
    
    # Badge
    draw_badge(draw, "FRASE 01", 90, 165, bg_color=COLOR_DEEP_GREEN, font_size=22)
    
    # Frase em Destaque (Aspas / Citação clínica)
    font_quote = get_font(46, 700)
    quote_text = '“Está dentro do esperado\npara a idade.”'
    lines = quote_text.split('\n')
    curr_y = 230
    for l in lines:
        draw.text((90, curr_y), l, fill=COLOR_DEEP_GREEN, font=font_quote)
        curr_y += 58
        
    # Chamada / Pergunta em destaque
    curr_y += 10
    font_call = get_font(36, 800)
    draw.text((90, curr_y), "Esperado em quê?", fill=COLOR_CORAL, font=font_call)
    
    # Bloco de texto explicativo
    curr_y += 54
    font_body = get_font(29, 500)
    body_lines = [
        "Compreensão? Vocabulário? Construção de frases? Interação?",
        "",
        "Um relatório precisa deixar claro quais habilidades foram",
        "observadas e o que fundamenta essa conclusão."
    ]
    for bl in body_lines:
        draw.text((90, curr_y), bl, fill=COLOR_CHARCOAL, font=font_body)
        curr_y += 40
        
    # Foto editorial (Mãos morenas e prancheta com anotações e blocos)
    foto_path = os.path.join(RAW_DIR, "02-frase-01.jpg")
    insert_image_with_radius(img, foto_path, (90, 640, 900, 560), radius=26)
    
    draw_footer(draw)
    
    out_path = os.path.join(FINAL_DIR, "02-frase-01.png")
    img.save(out_path, "PNG", quality=100)
    print(f"Gerado: {out_path}")


def render_slide_03_frase_02():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, 3, 7)
    
    # Badge
    draw_badge(draw, "FRASE 02", 90, 165, bg_color=COLOR_DEEP_GREEN, font_size=22)
    
    # Frase em Destaque
    font_quote = get_font(46, 700)
    quote_text = '“Apresenta atraso de linguagem.”'
    draw.text((90, 230), quote_text, fill=COLOR_DEEP_GREEN, font=font_quote)
    
    # Chamada
    curr_y = 296
    font_call = get_font(36, 800)
    draw.text((90, curr_y), "Essa frase, sozinha, diz pouco.", fill=COLOR_CORAL, font=font_call)
    
    # Texto explicativo
    curr_y += 56
    font_body = get_font(29, 500)
    body_lines = [
        "É fundamental explicar quais aspectos da linguagem",
        "apresentaram dificuldades (expressão, compreensão, fala)",
        "e quais observações sustentam essa interpretação."
    ]
    for bl in body_lines:
        draw.text((90, curr_y), bl, fill=COLOR_CHARCOAL, font=font_body)
        curr_y += 40
        
    # Foto editorial (Interação acolhedora com criança negra e livro em português)
    foto_path = os.path.join(RAW_DIR, "03-frase-02.jpg")
    insert_image_with_radius(img, foto_path, (90, 590, 900, 610), radius=26)
    
    draw_footer(draw)
    
    out_path = os.path.join(FINAL_DIR, "03-frase-02.png")
    img.save(out_path, "PNG", quality=100)
    print(f"Gerado: {out_path}")


def render_slide_04_frase_03():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, 4, 7)
    
    # Badge
    draw_badge(draw, "FRASE 03", 90, 165, bg_color=COLOR_DEEP_GREEN, font_size=22)
    
    # Frase em Destaque
    font_quote = get_font(44, 700)
    quote_text = '“Não colaborou durante a avaliação.”'
    draw.text((90, 226), quote_text, fill=COLOR_DEEP_GREEN, font=font_quote)
    
    # Chamada
    curr_y = 288
    font_call = get_font(35, 800)
    draw.text((90, curr_y), "O que realmente aconteceu?", fill=COLOR_CORAL, font=font_call)
    
    # Tópicos explicativos em lista clara
    curr_y += 50
    font_item = get_font(27, 600)
    bullets = [
        "• Recusou atividades específicas?",
        "• Teve dificuldade para compreender os comandos?",
        "• Permaneceu pouco tempo na tarefa?",
        "• Precisou de ajuda constante para engajar?"
    ]
    for b in bullets:
        draw.text((90, curr_y), b, fill=COLOR_CHARCOAL, font=font_item)
        curr_y += 38
        
    # Conclusão do slide
    curr_y += 12
    font_note = get_font(26, 500)
    note_lines = [
        "Descrever o comportamento observado informa muito mais",
        "à família do que simplesmente rotular como 'não colaborou'."
    ]
    for nl in note_lines:
        draw.text((90, curr_y), nl, fill=COLOR_MUTED_GRAY, font=font_note)
        curr_y += 34
        
    # Foto editorial (Criança parda no seu tempo com brinquedo de madeira e fono observando)
    foto_path = os.path.join(RAW_DIR, "04-frase-03.jpg")
    insert_image_with_radius(img, foto_path, (90, 680, 900, 520), radius=26)
    
    draw_footer(draw)
    
    out_path = os.path.join(FINAL_DIR, "04-frase-03.png")
    img.save(out_path, "PNG", quality=100)
    print(f"Gerado: {out_path}")


def render_slide_05_frase_04():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, 5, 7)
    
    # Badge
    draw_badge(draw, "FRASE 04", 90, 165, bg_color=COLOR_DEEP_GREEN, font_size=22)
    
    # Frase em Destaque
    font_quote = get_font(42, 700)
    quote_text = '“Teve resultado abaixo do esperado no protocolo.”'
    draw.text((90, 226), quote_text, fill=COLOR_DEEP_GREEN, font=font_quote)
    
    # Chamada
    curr_y = 286
    font_call = get_font(34, 800)
    draw.text((90, curr_y), "A pontuação é apenas uma parte da avaliação.", fill=COLOR_CORAL, font=font_call)
    
    # Texto explicativo
    curr_y += 52
    font_body = get_font(28, 500)
    body_lines = [
        "Mais do que um número final, importa compreender",
        "como a criança respondeu, quais foram seus caminhos,",
        "seus acertos e as condições em que realizou as atividades."
    ]
    for bl in body_lines:
        draw.text((90, curr_y), bl, fill=COLOR_CHARCOAL, font=font_body)
        curr_y += 38
        
    # Foto editorial (Macro de fichas de frutas tropicais em português e anotações clínicas)
    foto_path = os.path.join(RAW_DIR, "05-frase-04.jpg")
    insert_image_with_radius(img, foto_path, (90, 580, 900, 620), radius=26)
    
    draw_footer(draw)
    
    out_path = os.path.join(FINAL_DIR, "05-frase-04.png")
    img.save(out_path, "PNG", quality=100)
    print(f"Gerado: {out_path}")


def render_slide_06_frase_05():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, 6, 7)
    
    # Badge
    draw_badge(draw, "FRASE 05", 90, 165, bg_color=COLOR_DEEP_GREEN, font_size=22)
    
    # Frase em Destaque
    font_quote = get_font(44, 700)
    quote_text = '“Precisa de acompanhamento fonoaudiológico.”'
    draw.text((90, 226), quote_text, fill=COLOR_DEEP_GREEN, font=font_quote)
    
    # Chamada
    curr_y = 286
    font_call = get_font(35, 800)
    draw.text((90, curr_y), "A família precisa entender por quê.", fill=COLOR_CORAL, font=font_call)
    
    # Texto explicativo
    curr_y += 52
    font_body = get_font(28, 500)
    body_lines = [
        "O relatório deve relacionar a indicação aos achados observados,",
        "às habilidades que precisam ser desenvolvidas e aos objetivos",
        "claros de cada etapa do acompanhamento."
    ]
    for bl in body_lines:
        draw.text((90, curr_y), bl, fill=COLOR_CHARCOAL, font=font_body)
        curr_y += 38
        
    # Foto editorial (Diálogo empático entre fonoaudióloga e mãe brasileira)
    foto_path = os.path.join(RAW_DIR, "06-frase-05.jpg")
    insert_image_with_radius(img, foto_path, (90, 575, 900, 625), radius=26)
    
    draw_footer(draw)
    
    out_path = os.path.join(FINAL_DIR, "06-frase-05.png")
    img.save(out_path, "PNG", quality=100)
    print(f"Gerado: {out_path}")


def render_slide_07_fechamento():
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_OFFWHITE)
    draw = ImageDraw.Draw(img)
    
    draw_header(draw, 7, 7, "SÍNTESE & ORIENTAÇÃO")
    
    # Badge
    draw_badge(draw, "PARA GUARDAR", 90, 165, bg_color=COLOR_CORAL, font_size=22)
    
    # Título
    font_title = get_font(48, 800)
    t_lines = [
        "Um relatório não deve",
        "apenas dar uma conclusão."
    ]
    curr_y = 230
    for tl in t_lines:
        draw.text((90, curr_y), tl, fill=COLOR_DEEP_GREEN, font=font_title)
        curr_y += 62
        
    # Destaque de Complemento
    curr_y += 10
    font_sub = get_font(36, 700)
    sub_lines = [
        "Ele precisa ajudar a compreender",
        "o que foi observado."
    ]
    for sl in sub_lines:
        draw.text((90, curr_y), sl, fill=COLOR_OLIVE, font=font_sub)
        curr_y += 48
        
    # Citação Emocional / Autoridade
    curr_y += 18
    font_cite = get_font(30, 600)
    draw.text((90, curr_y), "“Clareza também faz parte do cuidado.”", fill=COLOR_CORAL, font=font_cite)
    
    # Foto com respiro do consultório brasileiro (Estante de livros e vaso jiboia)
    foto_path = os.path.join(RAW_DIR, "07-fechamento.jpg")
    insert_image_with_radius(img, foto_path, (90, 545, 900, 480), radius=26)
    
    # Bloco de Assinatura e Chamada para Ação (Y: 1045 a 1215)
    card_box = [90, 1045, 990, 1215]
    draw.rounded_rectangle(card_box, radius=20, fill=COLOR_BG_CARD, outline=COLOR_BORDER_LIGHT, width=1)
    
    font_name = get_font(34, 800)
    font_role = get_font(24, 600)
    font_cta = get_font(24, 700)
    
    draw.text((125, 1070), "Sônia Torres", fill=COLOR_DEEP_GREEN, font=font_name)
    draw.text((125, 1115), "Fonoaudióloga  |  CRFa 1-17701", fill=COLOR_CHARCOAL, font=font_role)
    draw.text((125, 1152), "@torresdafono", fill=COLOR_OLIVE, font=font_role)
    
    cta_badge_text = "SALVE ESTE POST"
    draw_badge(draw, cta_badge_text, 680, 1105, bg_color=COLOR_CORAL, text_color=COLOR_WHITE, font_size=20, padding_x=22, padding_y=12)
    
    draw_footer(draw, is_closing=True)
    
    out_path = os.path.join(FINAL_DIR, "07-fechamento.png")
    img.save(out_path, "PNG", quality=100)
    print(f"Gerado: {out_path}")


def render_prancha_visao_geral():
    """Gera uma prancha horizontal com os 7 slides lado a lado em alta definição para conferência."""
    slide_files = [
        "01-capa.png",
        "02-frase-01.png",
        "03-frase-02.png",
        "04-frase-03.png",
        "05-frase-04.png",
        "06-frase-05.png",
        "07-fechamento.png"
    ]
    
    # Cada thumbnail com 432 x 540 px (escala 0.4)
    thumb_w = 432
    thumb_h = 540
    gap = 36
    padding = 60
    
    total_w = padding * 2 + (thumb_w * 7) + (gap * 6)
    total_h = padding * 2 + thumb_h + 160
    
    prancha = Image.new("RGB", (total_w, total_h), (242, 238, 230))
    p_draw = ImageDraw.Draw(prancha)
    
    # Cabeçalho da prancha
    font_p_title = get_font(44, 800)
    font_p_meta = get_font(24, 600)
    
    p_draw.text((padding, 45), "CARROSSEL INSTAGRAM — VISÃO GERAL DE CONSISTÊNCIA VISUAL", fill=COLOR_DEEP_GREEN, font=font_p_title)
    p_draw.text((padding, 100), "Sônia Torres • Fonoaudióloga (CRFa 1-17701) | @torresdafono  •  Formato: 1080x1350 px (4:5)", fill=COLOR_OLIVE, font=font_p_meta)
    
    curr_x = padding
    curr_y = 170
    
    for i, sf in enumerate(slide_files, 1):
        s_path = os.path.join(FINAL_DIR, sf)
        if os.path.exists(s_path):
            slide_img = Image.open(s_path).convert("RGB")
            slide_resized = slide_img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            
            # Sombra para destacar cada prancha
            shadow = Image.new("RGBA", (thumb_w + 16, thumb_h + 16), (0, 0, 0, 0))
            s_d = ImageDraw.Draw(shadow)
            s_d.rounded_rectangle([8, 10, thumb_w + 8, thumb_h + 10], radius=12, fill=(0, 0, 0, 45))
            shadow = shadow.filter(ImageFilter.GaussianBlur(8))
            prancha.paste(shadow, (curr_x - 8, curr_y - 8), shadow)
            
            # Colar slide
            prancha.paste(slide_resized, (curr_x, curr_y))
            
            # Legenda inferior
            font_cap = get_font(20, 700)
            caption = f"Slide {i:02d}"
            p_draw.text((curr_x + 10, curr_y + thumb_h + 16), caption, fill=COLOR_DEEP_GREEN, font=font_cap)
            
            curr_x += thumb_w + gap
            
    out_prancha = os.path.join(FINAL_DIR, "prancha-visao-geral.png")
    prancha.save(out_prancha, "PNG", quality=95)
    print(f"Gerada prancha: {out_prancha}")


if __name__ == "__main__":
    print("Iniciando renderização editorial dos 7 slides...")
    render_slide_01_capa()
    render_slide_02_frase_01()
    render_slide_03_frase_02()
    render_slide_04_frase_03()
    render_slide_05_frase_04()
    render_slide_06_frase_05()
    render_slide_07_fechamento()
    render_prancha_visao_geral()
    print("Sucesso! Todos os 7 slides e a prancha de visão geral foram criados.")
