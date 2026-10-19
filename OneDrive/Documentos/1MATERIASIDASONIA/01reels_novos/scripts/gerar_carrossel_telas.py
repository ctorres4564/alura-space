# -*- coding: utf-8 -*-
"""
Script de Renderização dos Slides de Carrossel Instagram (1080x1350)
Tema: "Deixo o celular para ele ficar quieto" (Telas na Primeira Infância)
Profissional: Dra. Sônia Torres · Fonoaudióloga · CRFa 1-17701
Formato: 4:5 vertical (feed do Instagram)
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "publicacao", "carrossel-telas")
ASSETS_DIR = os.path.join(BASE_DIR, "publicacao", "telas-objecao", "imagens")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Dimensões (Instagram Portrait 4:5)
W, H = 1080, 1350

# Paleta de Cores Institucional Sônia Torres
BG_DARK = (28, 16, 52)         # #1C1034 Roxo profundo
BG_CARD = (40, 24, 72)         # #281848 Roxo intermediário para cartões
ACCENT_LILAC = (168, 130, 245) # #A882F5 Lilás de realce
ACCENT_GOLD = (248, 186, 54)   # #F8BA36 Dourado quente
TEXT_WHITE = (255, 255, 255)
TEXT_MUTED = (200, 190, 220)
TEXT_GRAY = (140, 130, 160)
BOX_BG = (48, 30, 84)

# Carregamento de fontes com fallbacks
poppins_path = os.path.join(FONTS_DIR, "Poppins-Bold.ttf")
segoe_path = "C:/Windows/Fonts/segoeui.ttf"
segoe_bold_path = "C:/Windows/Fonts/segoeuib.ttf"
arial_bold_path = "C:/Windows/Fonts/arialbd.ttf"
arial_path = "C:/Windows/Fonts/arial.ttf"

def get_font(path, size, fallback="arial.ttf"):
    try:
        return ImageFont.truetype(path, size)
    except:
        try:
            return ImageFont.truetype(fallback, size)
        except:
            return ImageFont.load_default()

font_title_hero = get_font(poppins_path, 58, arial_bold_path)
font_title = get_font(poppins_path, 46, arial_bold_path)
font_subtitle = get_font(segoe_bold_path, 32, arial_bold_path)
font_body_bold = get_font(segoe_bold_path, 28, arial_bold_path)
font_body = get_font(segoe_path, 26, arial_path)
font_tag = get_font(poppins_path, 22, arial_bold_path)
font_footer = get_font(segoe_path, 22, arial_path)

def draw_header(draw, slide_num, total_slides=7, tag="DESENVOLVIMENTO INFANTIL · TELAS"):
    """Renderiza a tag superior de categoria e o número da página."""
    tag_w = draw.textlength(tag, font=font_tag)
    draw.rounded_rectangle([70, 55, 70 + tag_w + 32, 98], radius=12, fill=(60, 36, 105))
    draw.text((86, 64), tag, font=font_tag, fill=ACCENT_GOLD)
    
    pag_text = f"{slide_num}/{total_slides}"
    pag_w = draw.textlength(pag_text, font=font_tag)
    draw.text((W - 70 - pag_w, 64), pag_text, font=font_tag, fill=TEXT_MUTED)

def draw_footer(draw, is_last=False):
    """Renderiza o rodapé institucional e o indicador de arraste."""
    author_text = "Sônia Torres | Fonoaudióloga · CRFa 1-17701"
    draw.text((70, H - 75), author_text, font=font_footer, fill=TEXT_MUTED)
    
    if not is_last:
        cta_text = "Arraste ➔"
        cta_w = draw.textlength(cta_text, font=font_tag)
        draw.text((W - 70 - cta_w, H - 78), cta_text, font=font_tag, fill=ACCENT_LILAC)

def wrap_text(text, font, max_width, draw):
    """Quebra texto respeitando largura máxima."""
    lines = []
    paragraphs = text.split("\n")
    for p in paragraphs:
        if not p.strip():
            lines.append("")
            continue
        words = p.split(" ")
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            if draw.textlength(test_line, font=font) <= max_width:
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

def create_base_canvas():
    """Gera o fundo com gradiente sutil roxo institucional."""
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        alpha = y / H
        r = int(BG_DARK[0] * (1 - alpha * 0.3) + 18 * alpha)
        g = int(BG_DARK[1] * (1 - alpha * 0.3) + 10 * alpha)
        b = int(BG_DARK[2] * (1 - alpha * 0.3) + 36 * alpha)
        draw.line([(0, y), (W, y)], fill=(r, g, b), width=4)
    return img, draw

def crop_and_fit_image(img_path, target_w, target_h, focus_y_ratio=0.48):
    """
    Recorta e redimensiona a imagem vertical 9:16 para a janela horizontal/retangular
    com controle fino de enquadramento vertical (focus_y_ratio), garantindo que
    as mãos e os objetos centrais nunca sejam cortados.
    """
    if not os.path.exists(img_path):
        return None
    
    src = Image.open(img_path).convert("RGB")
    src_w, src_h = src.size
    
    # Redimensiona para cobrir totalmente a largura alvo
    scale = target_w / src_w
    scaled_w = target_w
    scaled_h = int(src_h * scale)
    
    # Se a altura escalada for menor que o target_h, escala pela altura
    if scaled_h < target_h:
        scale = target_h / src_h
        scaled_h = target_h
        scaled_w = int(src_w * scale)
        
    resized = src.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
    
    # Cálculo do corte vertical com base no foco de interesse
    center_y = int(scaled_h * focus_y_ratio)
    top = center_y - (target_h // 2)
    
    # Previne ultrapassar limites
    if top < 0:
        top = 0
    if top + target_h > scaled_h:
        top = scaled_h - target_h
        
    left = (scaled_w - target_w) // 2
    cropped = resized.crop((left, top, left + target_w, top + target_h))
    
    # Aplica máscara de cantos arredondados elegante
    mask = Image.new("L", (target_w, target_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, target_w, target_h], radius=22, fill=255)
    
    # Borda sutil de 1px ao redor da imagem para acabamento refinado
    border_overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(border_overlay)
    bdraw.rounded_rectangle([0, 0, target_w - 1, target_h - 1], radius=22, outline=(255, 255, 255, 40), width=1)
    
    final_img = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    final_img.paste(cropped, (0, 0), mask)
    final_img = Image.alpha_composite(final_img, border_overlay)
    
    return final_img

# ==================== SLIDE 1: CAPA COM GANCHO FORTE ====================
def render_slide_1():
    img, draw = create_base_canvas()
    draw_header(draw, 1, 7, "DESENVOLVIMENTO INFANTIL · TELAS")
    
    # Imagem Quadro 1: Mãozinha da criança alcançando celular e mão do adulto intervindo
    # Enquadramento calibrado: focus_y_ratio=0.44 para manter o visor e o toque de mãos no centro
    q1_path = os.path.join(ASSETS_DIR, "quadro1_limpo.png")
    photo = crop_and_fit_image(q1_path, target_w=W - 140, target_h=500, focus_y_ratio=0.44)
    if photo:
        img.paste(photo, (70, 130), photo)
        
    # Título Principal (Capa)
    title = "“Deixo o celular para\nele ficar quieto...”"
    y_pos = 665
    for line in title.split("\n"):
        draw.text((70, y_pos), line, font=font_title_hero, fill=TEXT_WHITE)
        y_pos += 72
        
    # Card reflexivo acolhedor
    y_card = y_pos + 20
    draw.rounded_rectangle([70, y_card, W - 70, y_card + 340], radius=18, fill=BOX_BG)
    
    sub_title = "Quem nunca sentiu esse impulso?"
    draw.text((100, y_card + 28), sub_title, font=font_subtitle, fill=ACCENT_GOLD)
    
    body = (
        "O cansaço da rotina é real e ninguém educa no vazio.\n\n"
        "Mas o que a neurociência e a fonoaudiologia mostram "
        "sobre o que acontece no cérebro infantil quando substituímos a troca humana por telas?"
    )
    by = y_card + 80
    for line in wrap_text(body, font_body, W - 200, draw):
        draw.text((100, by), line, font=font_body, fill=TEXT_MUTED)
        by += 38
        
    draw_footer(draw)
    out_p = os.path.join(OUTPUT_DIR, "slide_01_capa.png")
    img.save(out_p, "PNG")
    print(f"Slide 1 gerado: {out_p}")

# ==================== SLIDE 2: O CANSAÇO REAL E A CULPA ====================
def render_slide_2():
    img, draw = create_base_canvas()
    draw_header(draw, 2, 7)
    
    title = "Ninguém educa no vazio:\no cansaço familiar é real."
    y = 140
    for line in title.split("\n"):
        draw.text((70, y), line, font=font_title, fill=ACCENT_GOLD)
        y += 62
        
    y += 20
    # Cartão 1: Empatia e Realidade
    draw.rounded_rectangle([70, y, W - 70, y + 360], radius=20, fill=BG_CARD)
    draw.text((100, y + 30), "A rotina não é um comercial de TV", font=font_subtitle, fill=TEXT_WHITE)
    
    body1 = (
        "Muitas vezes, o celular não entra por negligência, mas por necessidade de sobrevivência:\n\n"
        "• Fazer o jantar sem a panela queimar.\n"
        "• Responder a uma urgência do trabalho.\n"
        "• Conseguir 10 minutos para respirar em um dia exaustivo."
    )
    by1 = y + 80
    for bl in wrap_text(body1, font_body, W - 200, draw):
        draw.text((100, by1), bl, font=font_body, fill=TEXT_MUTED)
        by1 += 38
        
    # Cartão 2: Sem Julgamento
    y += 400
    draw.rounded_rectangle([70, y, W - 70, y + 430], radius=20, fill=BOX_BG)
    draw.text((100, y + 35), "Sem culpa. Com consciência.", font=font_subtitle, fill=ACCENT_LILAC)
    
    body2 = (
        "A fonoaudiologia não está aqui para apontar o dedo ou cobrar perfeição inatingível.\n\n"
        "O nosso papel é apresentar as evidências clínicas para que você entenda as necessidades do desenvolvimento e faça escolhas conscientes no dia a dia."
    )
    by2 = y + 90
    for bl in wrap_text(body2, font_body_bold, W - 200, draw):
        draw.text((100, by2), bl, font=font_body_bold, fill=TEXT_WHITE)
        by2 += 42
        
    draw_footer(draw)
    out_p = os.path.join(OUTPUT_DIR, "slide_02_acolhimento.png")
    img.save(out_p, "PNG")
    print(f"Slide 2 gerado: {out_p}")

# ==================== SLIDE 3: ATÉ OS 2 ANOS (ZERO TELA) ====================
def render_slide_3():
    img, draw = create_base_canvas()
    draw_header(draw, 3, 7)
    
    # Imagem Quadro 2: Blocos de madeira e dedinhos da criança
    # Enquadramento calibrado: focus_y_ratio=0.48 para centralizar a torre e as mãos
    q2_path = os.path.join(ASSETS_DIR, "quadro2_limpo.png")
    photo = crop_and_fit_image(q2_path, target_w=W - 140, target_h=430, focus_y_ratio=0.48)
    if photo:
        img.paste(photo, (70, 130), photo)
        
    title = "Até os 2 anos:\na recomendação é ZERO tela."
    y = 590
    for line in title.split("\n"):
        draw.text((70, y), line, font=font_title, fill=TEXT_WHITE)
        y += 58
        
    # Card Explicativo
    y += 20
    draw.rounded_rectangle([70, y, W - 70, y + 430], radius=18, fill=BG_CARD)
    draw.text((100, y + 26), "Por que o mundo real é insubstituível?", font=font_subtitle, fill=ACCENT_GOLD)
    
    items = (
        "• Conexões neurais em salto: O cérebro do bebê aprende pela tridimensionalidade do ambiente físico.\n\n"
        "• Estímulo multissensorial: A criança precisa pegar, sentir peso, textura e temperatura dos objetos reais.\n\n"
        "• Como a fala nasce: O bebê aprende a falar olhando o movimento da boca humana, os olhos e a entonação da sua voz."
    )
    by = y + 78
    for bl in wrap_text(items, font_body, W - 200, draw):
        draw.text((100, by), bl, font=font_body, fill=TEXT_MUTED)
        by += 35
        
    # Fonte oficial
    draw.text((100, y + 380), "Orientação: Sociedade Brasileira de Pediatria (SBP, 2022)", font=font_footer, fill=ACCENT_LILAC)
    
    draw_footer(draw)
    out_p = os.path.join(OUTPUT_DIR, "slide_03_ate_2_anos.png")
    img.save(out_p, "PNG")
    print(f"Slide 3 gerado: {out_p}")

# ==================== SLIDE 4: DE 2 A 5 ANOS (LIMITE PRÁTICO) ====================
def render_slide_4():
    img, draw = create_base_canvas()
    draw_header(draw, 4, 7)
    
    # Imagem Quadro 3: Massinha de modelar, mãos e ampulheta ao fundo
    # Enquadramento calibrado: focus_y_ratio=0.46 para capturar ampulheta e massinha
    q3_path = os.path.join(ASSETS_DIR, "quadro3_limpo.png")
    photo = crop_and_fit_image(q3_path, target_w=W - 140, target_h=430, focus_y_ratio=0.46)
    if photo:
        img.paste(photo, (70, 130), photo)
        
    title = "De 2 a 5 anos:\naté 1 hora por dia."
    y = 590
    for line in title.split("\n"):
        draw.text((70, y), line, font=font_title, fill=TEXT_WHITE)
        y += 58
        
    # Card Explicativo
    y += 20
    draw.rounded_rectangle([70, y, W - 70, y + 430], radius=18, fill=BOX_BG)
    draw.text((100, y + 26), "Uma referência prática, não uma punição", font=font_subtitle, fill=ACCENT_LILAC)
    
    items = (
        "• Não encare como regra punitiva: Esse limite serve como bússola de equilíbrio para a rotina familiar.\n\n"
        "• Qualidade acima de tudo: Escolha programas calmos, educativos e com narrativa compreensível. Evite vídeos frenéticos e hipnóticos.\n\n"
        "• Mediação ativa: O adulto precisa estar junto, comentando, perguntando e dando sentido ao que é assistido."
    )
    by = y + 78
    for bl in wrap_text(items, font_body, W - 200, draw):
        draw.text((100, by), bl, font=font_body, fill=TEXT_MUTED)
        by += 35
        
    draw.text((100, y + 380), "Referência de rotina sugerida por especialistas pediátricos", font=font_footer, fill=ACCENT_GOLD)
    
    draw_footer(draw)
    out_p = os.path.join(OUTPUT_DIR, "slide_04_de_2_a_5_anos.png")
    img.save(out_p, "PNG")
    print(f"Slide 4 gerado: {out_p}")

# ==================== SLIDE 5: A CIÊNCIA SEM ALARMISMO ====================
def render_slide_5():
    img, draw = create_base_canvas()
    draw_header(draw, 5, 7, "CIÊNCIA & DESENVOLVIMENTO")
    
    # Imagem Quadro 4: Flat lay com cartões ilustrados infantis
    # Enquadramento calibrado: focus_y_ratio=0.45 para capturar os cartões e as mãos apontando juntas
    q4_path = os.path.join(ASSETS_DIR, "quadro4_limpo.png")
    photo = crop_and_fit_image(q4_path, target_w=W - 140, target_h=400, focus_y_ratio=0.45)
    if photo:
        img.paste(photo, (70, 130), photo)
        
    title = "O que as pesquisas mostram?\n(Sem mitos e sem pânico)"
    y = 560
    for line in title.split("\n"):
        draw.text((70, y), line, font=font_title, fill=ACCENT_GOLD)
        y += 58
        
    # Card Analítico do Estudo
    y += 15
    draw.rounded_rectangle([70, y, W - 70, y + 475], radius=18, fill=BG_CARD)
    draw.text((100, y + 26), "Estudo Madigan et al., 2019 (JAMA Pediatrics)", font=font_subtitle, fill=TEXT_WHITE)
    
    body = (
        "Uma relevante pesquisa acompanhou 2.441 crianças e observou que mais tempo de tela se associou a escores um pouco menores no desenvolvimento global.\n\n"
        "⚠️ Mas atenção ao rigor científico:\n"
        "• A associação estatística observada é MODESTA.\n"
        "• O estudo NÃO comprova que a tela seja a causa direta ou isolada do atraso.\n"
        "• O alerta não é para gerar culpa, mas para valorizar a interação que constrói a linguagem."
    )
    by = y + 78
    for bl in wrap_text(body, font_body, W - 200, draw):
        # Destaque de cor para avisos
        fill_color = ACCENT_GOLD if "⚠️" in bl or "MODESTA" in bl else TEXT_MUTED
        draw.text((100, by), bl, font=font_body, fill=fill_color)
        by += 34
        
    draw_footer(draw)
    out_p = os.path.join(OUTPUT_DIR, "slide_05_estudo_cientifico.png")
    img.save(out_p, "PNG")
    print(f"Slide 5 gerado: {out_p}")

# ==================== SLIDE 6: O QUE CONSTRÓI A FALA ====================
def render_slide_6():
    img, draw = create_base_canvas()
    draw_header(draw, 6, 7, "DESENVOLVIMENTO DA LINGUAGEM")
    
    # Imagem Quadro 5: Dedinho da criança no livro ilustrado e acolhimento do adulto
    # Enquadramento calibrado: focus_y_ratio=0.46 para foco macro no toque das mãos e na página
    q5_path = os.path.join(ASSETS_DIR, "quadro5_limpo.png")
    photo = crop_and_fit_image(q5_path, target_w=W - 140, target_h=430, focus_y_ratio=0.46)
    if photo:
        img.paste(photo, (70, 130), photo)
        
    title = "O que desenvolve a fala\né a presença humana viva."
    y = 590
    for line in title.split("\n"):
        draw.text((70, y), line, font=font_title, fill=TEXT_WHITE)
        y += 58
        
    # Card Conceitual
    y += 20
    draw.rounded_rectangle([70, y, W - 70, y + 430], radius=18, fill=BOX_BG)
    draw.text((100, y + 26), "O valor da Atenção Conjunta (Joint Attention)", font=font_subtitle, fill=ACCENT_LILAC)
    
    items = (
        "• Aplicativo nenhum substitui o olhar recíproco: Telas reproduzem sons, mas não respondem aos gestos únicos do seu filho.\n\n"
        "• A linguagem nasce no afeto: A pergunta curiosa sobre o brinquedo, a risada compartilhada e a pausa para esperar a criança responder.\n\n"
        "• Conversar e olhar juntos ainda faz toda a diferença para o cérebro infantil."
    )
    by = y + 78
    for bl in wrap_text(items, font_body, W - 200, draw):
        draw.text((100, by), bl, font=font_body, fill=TEXT_MUTED)
        by += 35
        
    draw_footer(draw)
    out_p = os.path.join(OUTPUT_DIR, "slide_06_atencao_conjunta.png")
    img.save(out_p, "PNG")
    print(f"Slide 6 gerado: {out_p}")

# ==================== SLIDE 7: CTA / CONVITE AO DEBATE ====================
def render_slide_7():
    img, draw = create_base_canvas()
    draw_header(draw, 7, 7, "CONVITE AO DEBATE")
    
    # Card Elegante Central em Off-White (idêntico ao fechamento do vídeo)
    card_w = 940
    card_h = 410
    card_x = (W - card_w) // 2
    card_y = 135
    
    # Sombra do card
    draw.rounded_rectangle(
        [card_x - 4, card_y + 8, card_x + card_w + 4, card_y + card_h + 16],
        radius=28,
        fill=(0, 0, 0, 80)
    )
    
    # Fundo do card off-white
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=26,
        fill=(250, 248, 245)
    )
    
    # Textos do card interno
    t1_lines = ["FALTA DE LIMITES OU", "DIFICULDADE DE COMUNICAÇÃO?"]
    curr_y = card_y + 48
    for line in t1_lines:
        bbox = font_title.getbbox(line)
        lw = bbox[2] - bbox[0]
        draw.text(((W - lw) // 2, curr_y), line, font=font_title, fill=(20, 20, 20))
        curr_y += 50
        
    curr_y += 14
    t2 = "O QUE VOCÊ PENSA?"
    bbox2 = font_subtitle.getbbox(t2)
    w2 = bbox2[2] - bbox2[0]
    draw.text(((W - w2) // 2, curr_y), t2, font=font_subtitle, fill=(115, 62, 147))
    
    curr_y += 65
    t3 = "Sônia Torres | Fonoaudióloga"
    bbox3 = font_body_bold.getbbox(t3)
    w3 = bbox3[2] - bbox3[0]
    draw.text(((W - w3) // 2, curr_y), t3, font=font_body_bold, fill=(40, 40, 40))
    
    curr_y += 36
    t4 = "sonia.fonosuite.com"
    bbox4 = font_body.getbbox(t4)
    w4 = bbox4[2] - bbox4[0]
    draw.text(((W - w4) // 2, curr_y), t4, font=font_body, fill=(110, 110, 110))
    
    # Bloco inferior de interação (ajustado para acomodar texto e ações sem colisão)
    box_y = 575
    box_h = 600
    draw.rounded_rectangle([70, box_y, W - 70, box_y + box_h], radius=20, fill=BG_CARD)
    draw.text((100, box_y + 28), "Vamos conversar nos comentários?", font=font_subtitle, fill=ACCENT_GOLD)
    
    cta_body = (
        "Como funciona a rotina de telas na sua casa?\n\n"
        "Você já notou alguma diferença no comportamento, na agitação ou na comunicação da criança após períodos mais longos em frente ao celular ou TV?"
    )
    cby = box_y + 78
    for cl in wrap_text(cta_body, font_body, W - 200, draw):
        draw.text((100, cby), cl, font=font_body, fill=TEXT_WHITE)
        cby += 36
        
    # Ações de engajamento posicionadas DINAMICAMENTE após o texto (sem sobreposição)
    act_y = cby + 26
    actions = [
        "💬 Deixe sua experiência nos comentários abaixo",
        "↗️ Envie para mães, pais e educadores que precisam ler isso",
        "🔖 Salve este post para consultar sempre que tiver dúvidas"
    ]
    for act in actions:
        # Fundo arredondado sutil para destacar cada ação
        act_bbox = font_body.getbbox(act)
        draw.rounded_rectangle([95, act_y - 6, W - 95, act_y + 36], radius=10, fill=BOX_BG)
        draw.text((115, act_y), act, font=font_body, fill=ACCENT_LILAC)
        act_y += 50
        
    # Assinatura de rodapé com selo de fechamento
    draw_footer(draw, is_last=True)
    out_p = os.path.join(OUTPUT_DIR, "slide_07_debate_cta.png")
    img.save(out_p, "PNG")
    print(f"Slide 7 gerado: {out_p}")

def main():
    print("=" * 60)
    print("RENDERIZADOR DE CARROSSEL - DRA. SÔNIA TORRES")
    print("Tema: 'Deixo o celular para ele ficar quieto' (Telas)")
    print(f"Destino: {OUTPUT_DIR}")
    print("=" * 60)
    
    render_slide_1()
    render_slide_2()
    render_slide_3()
    render_slide_4()
    render_slide_5()
    render_slide_6()
    render_slide_7()
    
    print("\nTodos os 7 slides foram renderizados com sucesso em 1080x1350!")

if __name__ == "__main__":
    main()
