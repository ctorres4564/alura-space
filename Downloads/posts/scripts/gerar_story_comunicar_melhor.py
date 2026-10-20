import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# -------------------------------------------------------------------------
# CONSTANTES DE DESIGN E DIMENSÕES (Instagram Story 9:16)
# -------------------------------------------------------------------------
WIDTH = 1080
HEIGHT = 1920

# Paleta de Cores Institucional (@torresdafono)
COLOR_CREME_BG = (244, 237, 228)           # #F4EDE4
COLOR_DARK_TEXT = (42, 36, 33)             # #2A2421 Marrom café editorial
COLOR_WHITE = (255, 255, 255)
COLOR_TERRACOTA = (194, 125, 96)           # #C27D60 Terracota principal da marca
COLOR_TERRACOTA_HOVER = (176, 110, 83)
COLOR_GOLD_ACCENT = (220, 184, 138)        # Dourado acolhedor / Champagne
COLOR_CARD_BG = (26, 20, 18, 218)          # Fundo semi-opaco translúcido café premium
COLOR_CARD_BORDER = (220, 184, 138, 140)   # Borda fina champagne translúcida

# Tipografia
FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_SERIF_REG = "C:/Windows/Fonts/georgia.ttf"
FONT_SERIF_ITALIC = "C:/Windows/Fonts/georgiai.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_SANS_REG = "C:/Windows/Fonts/segoui.ttf" if os.path.exists("C:/Windows/Fonts/segoui.ttf") else "C:/Windows/Fonts/segoeui.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def render_story():
    # 1. Carregar a foto real de alta qualidade
    photo_path = "assets/sonia_torres_real.jpg"
    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Foto não encontrada em: {photo_path}")
    
    raw_photo = Image.open(photo_path).convert("RGBA")
    
    # 2. Composição do Canvas e Enquadramento da Personagem
    # Queremos dar espaço no topo (y=200 a y=560) para a assinatura institucional e o gancho
    # sem cobrir o rosto, olhos ou sorriso da Dra. Sônia Torres!
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), (28, 23, 20, 255))
    
    # Redimensionamento harmônico da foto
    # A foto original tem proporção 682x1024.
    # Vamos escalar para largura de 1160px para melhor presença e centralização
    target_photo_w = 1160
    scale_factor = target_photo_w / raw_photo.width
    target_photo_h = int(raw_photo.height * scale_factor) # ~1740px
    photo_resized = raw_photo.resize((target_photo_w, target_photo_h), Image.Resampling.LANCZOS)
    
    # Posicionar a foto no terço médio-inferior
    # Offset x para centralizar a Dra. Sônia e o ambiente
    photo_x = (WIDTH - target_photo_w) // 2 + 10
    photo_y = 440  # Permite que a cabeça comece em torno de y = 440 + (1740*0.14) = 680px!
    
    # Extensão harmoniosa do topo do consultório:
    # A parte superior da foto tem a estante de madeira e parede clara.
    # Vamos pegar a fatia superior e estendê-la com gradiente e blur atmosférico suave
    top_slice = photo_resized.crop((0, 0, target_photo_w, 60))
    top_extended = top_slice.resize((WIDTH, photo_y + 120), Image.Resampling.BILINEAR)
    top_extended = top_extended.filter(ImageFilter.GaussianBlur(18))
    
    canvas.paste(top_extended, (0, 0))
    canvas.paste(photo_resized, (photo_x, photo_y), photo_resized)
    
    # 3. Tratamento de Cor & Overlays Translúcidos (Contraste AAA)
    # Overlay gradiente superior escuro/café para destacar o gancho sem poluição
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    # Gradiente do topo (0 a 650px) para garantir contraste perfeito no texto
    for y in range(0, 680):
        # Transição suave de opacidade
        if y < 380:
            alpha = int(220)
        else:
            prog = (y - 380) / 300.0
            alpha = int(220 * ((1.0 - prog) ** 1.5))
        draw_ov.line([(0, y), (WIDTH, y)], fill=(18, 14, 12, alpha))
        
    # Gradiente da base (1450 a 1920px) para aconchegar a CTA e rodapé
    for y in range(1400, HEIGHT):
        prog = (y - 1400) / 520.0
        alpha = int(200 * (prog ** 1.3))
        draw_ov.line([(0, y), (WIDTH, y)], fill=(16, 12, 11, alpha))
    
    # Tom quente sofisticado unificador (warm tint)
    warm_layer = Image.new("RGBA", (WIDTH, HEIGHT), (42, 28, 20, 28))
    overlay = Image.alpha_composite(overlay, warm_layer)
    
    story = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(story)
    
    # -------------------------------------------------------------------------
    # 4. ASSINATURA SUPERIOR DISCRETA E ELEGANTE (Safe Zone do Instagram)
    # "Sônia Torres | Fonoaudióloga • CRFª 1-17701" e "@torresdafono"
    # -------------------------------------------------------------------------
    y_brand = 220
    tag_box = (70, y_brand - 12, WIDTH - 70, y_brand + 48)
    
    # Cápsula translúcida com acabamento refinado
    cap_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    cap_draw = ImageDraw.Draw(cap_layer)
    cap_draw.rounded_rectangle(tag_box, radius=24, fill=(24, 18, 16, 175), outline=(220, 184, 138, 90), width=1)
    story = Image.alpha_composite(story, cap_layer)
    draw = ImageDraw.Draw(story)
    
    font_brand_name = get_font(FONT_SANS_BOLD, 22)
    font_brand_crf = get_font(FONT_SANS_REG, 21)
    
    name_str = "SÔNIA TORRES"
    crf_str = " | FONOAUDIÓLOGA  •  CRFª 1-17701"
    handle_str = "@TORRESDAFONO"
    
    draw.text((95, y_brand), name_str, font=font_brand_name, fill=(248, 243, 237))
    bbox_n = draw.textbbox((95, y_brand), name_str, font=font_brand_name)
    draw.text((bbox_n[2], y_brand), crf_str, font=font_brand_crf, fill=COLOR_GOLD_ACCENT)
    
    bbox_h = draw.textbbox((0, 0), handle_str, font=font_brand_name)
    h_w = bbox_h[2] - bbox_h[0]
    draw.text((WIDTH - 95 - h_w, y_brand), handle_str, font=font_brand_name, fill=(248, 243, 237))
    
    # -------------------------------------------------------------------------
    # 5. TEXTO SUPERIOR (GANCHO PRINCIPAL)
    # "Um primeiro passo para se comunicar melhor"
    # Fonte serifada editorial elegante, cor clara/branca, impacto instantâneo
    # -------------------------------------------------------------------------
    font_hook_reg = get_font(FONT_SERIF_BOLD, 58)
    font_hook_ita = get_font(FONT_SERIF_ITALIC, 58)
    
    hook_part1 = "Um primeiro passo"
    hook_part2 = "para se comunicar melhor"
    
    # Linha 1
    bbox_1 = draw.textbbox((0, 0), hook_part1, font=font_hook_reg)
    w_1 = bbox_1[2] - bbox_1[0]
    x_1 = (WIDTH - w_1) // 2
    y_1 = 330
    
    # Sombra difusa projetada
    draw.text((x_1 + 2, y_1 + 3), hook_part1, font=font_hook_reg, fill=(0, 0, 0, 200))
    draw.text((x_1, y_1), hook_part1, font=font_hook_reg, fill=COLOR_WHITE)
    
    # Linha 2 em itálico dourado terracota para máxima elegância editorial
    bbox_2 = draw.textbbox((0, 0), hook_part2, font=font_hook_ita)
    w_2 = bbox_2[2] - bbox_2[0]
    x_2 = (WIDTH - w_2) // 2
    y_2 = 412
    
    draw.text((x_2 + 2, y_2 + 3), hook_part2, font=font_hook_ita, fill=(0, 0, 0, 200))
    draw.text((x_2, y_2), hook_part2, font=font_hook_ita, fill=COLOR_GOLD_ACCENT)
    
    # -------------------------------------------------------------------------
    # 6. TEXTO CENTRAL DENTRO DE BLOCO TRANSLÚCIDO (CAIXA SEMI-OPACA)
    # "Atendimento fonoaudiológico para crianças, adultos e idosos,
    #  em consultório ou em domicílio no Rio de Janeiro."
    # -------------------------------------------------------------------------
    card_w = 930
    card_x1 = (WIDTH - card_w) // 2
    card_x2 = card_x1 + card_w
    card_y1 = 1170
    card_y2 = 1470
    
    # Sombra suave do bloco translúcido
    card_sh = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    csh_draw = ImageDraw.Draw(card_sh)
    csh_draw.rounded_rectangle((card_x1, card_y1 + 12, card_x2, card_y2 + 24), radius=32, fill=(0, 0, 0, 110))
    card_sh = card_sh.filter(ImageFilter.GaussianBlur(16))
    story = Image.alpha_composite(story, card_sh)
    
    # Bloco com fundo semi-opaco translúcido
    card_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card_layer)
    c_draw.rounded_rectangle(
        (card_x1, card_y1, card_x2, card_y2),
        radius=30,
        fill=COLOR_CARD_BG,
        outline=COLOR_CARD_BORDER,
        width=2
    )
    
    # Detalhe visual de cabeçalho do card
    header_badge = "CUIDADO ESPECIALIZADO & ACOLHEDOR"
    font_badge = get_font(FONT_SANS_BOLD, 20)
    bbox_b = c_draw.textbbox((0, 0), header_badge, font=font_badge)
    b_w = bbox_b[2] - bbox_b[0]
    b_x = (WIDTH - b_w) // 2
    c_draw.text((b_x, card_y1 + 34), header_badge, font=font_badge, fill=COLOR_GOLD_ACCENT)
    
    # Divisor suave
    div_y = card_y1 + 72
    c_draw.line([(card_x1 + 180, div_y), (card_x2 - 180, div_y)], fill=(220, 184, 138, 90), width=1)
    
    story = Image.alpha_composite(story, card_layer)
    draw = ImageDraw.Draw(story)
    
    # Texto Central (com ortografia corrigida: "domicílio")
    font_body = get_font(FONT_SERIF_REG, 34)
    body_text = "Atendimento fonoaudiológico para crianças, adultos e idosos, em consultório ou em domicílio no Rio de Janeiro."
    
    wrapped_lines = wrap_text(body_text, font_body, card_w - 90, draw)
    
    cur_y = card_y1 + 100
    for line in wrapped_lines:
        bbox_l = draw.textbbox((0, 0), line, font=font_body)
        l_w = bbox_l[2] - bbox_l[0]
        l_x = (WIDTH - l_w) // 2
        draw.text((l_x, cur_y), line, font=font_body, fill=(248, 244, 239))
        cur_y += 50

    # -------------------------------------------------------------------------
    # 7. TEXTO INFERIOR (CTA): "Conheça as opções"
    # Botão terracota de alta conversão
    # -------------------------------------------------------------------------
    btn_w = 600
    btn_h = 94
    btn_x1 = (WIDTH - btn_w) // 2
    btn_x2 = btn_x1 + btn_w
    btn_y1 = 1530
    btn_y2 = btn_y1 + btn_h
    
    # Sombra do botão
    btn_sh = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bsh_draw = ImageDraw.Draw(btn_sh)
    bsh_draw.rounded_rectangle((btn_x1, btn_y1 + 8, btn_x2, btn_y2 + 18), radius=47, fill=(0, 0, 0, 120))
    btn_sh = btn_sh.filter(ImageFilter.GaussianBlur(12))
    story = Image.alpha_composite(story, btn_sh)
    
    # Botão Terracota
    btn_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(btn_layer)
    b_draw.rounded_rectangle(
        (btn_x1, btn_y1, btn_x2, btn_y2),
        radius=47,
        fill=COLOR_TERRACOTA + (255,),
        outline=(255, 255, 255, 110),
        width=2
    )
    story = Image.alpha_composite(story, btn_layer)
    draw = ImageDraw.Draw(story)
    
    cta_label = "Conheça as opções"
    font_cta = get_font(FONT_SANS_BOLD, 32)
    bbox_c = draw.textbbox((0, 0), cta_label, font=font_cta)
    c_w = bbox_c[2] - bbox_c[0]
    c_h = bbox_c[3] - bbox_c[1]
    
    cta_x = (WIDTH - c_w - 38) // 2
    cta_y = btn_y1 + (btn_h - c_h) // 2 - 3
    draw.text((cta_x, cta_y), cta_label, font=font_cta, fill=COLOR_WHITE)
    
    # Ícone sutil chevron >
    arr_x = cta_x + c_w + 22
    arr_y = btn_y1 + btn_h // 2
    draw.line([(arr_x, arr_y - 12), (arr_x + 12, arr_y), (arr_x, arr_y + 12)], fill=COLOR_WHITE, width=4)

    # -------------------------------------------------------------------------
    # 8. ASSINATURA INSTITUCIONAL DE RODAPÉ
    # -------------------------------------------------------------------------
    footer_text = "DRA. SÔNIA TORRES • FONOAUDIOLOGIA CLÍNICA"
    font_foo = get_font(FONT_SANS_BOLD, 20)
    bbox_f = draw.textbbox((0, 0), footer_text, font=font_foo)
    f_w = bbox_f[2] - bbox_f[0]
    draw.text(((WIDTH - f_w) // 2, 1675), footer_text, font=font_foo, fill=(220, 184, 138, 210))

    # -------------------------------------------------------------------------
    # GRAVAÇÃO DOS ARQUIVOS FINAIS
    # -------------------------------------------------------------------------
    final_img = story.convert("RGB")
    
    target_main = "um-primeiro-passo-para-se-comunicar-melhor.jpg"
    final_img.save(target_main, "JPEG", quality=98, subsampling=0)
    print(f"[OK] Story principal atualizado com sucesso: {target_main}")
    
    os.makedirs("posts_finais", exist_ok=True)
    target_backup = "posts_finais/story_um_primeiro_passo_para_se_comunicar_melhor.jpg"
    final_img.save(target_backup, "JPEG", quality=98, subsampling=0)
    print(f"[OK] Cópia em alta resolução salva em: {target_backup}")

if __name__ == "__main__":
    render_story()
