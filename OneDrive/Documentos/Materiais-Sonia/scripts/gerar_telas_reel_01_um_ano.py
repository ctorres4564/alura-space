"""
Script para processamento, composição gráfica e renderização das 5 telas do Reel 01:
"Meu filho tem 1 ano e ainda não fala nenhuma palavra. Devo me preocupar?"
Fonoaudióloga Sônia Torres · CRFa 1-17701

Gera:
1. Fotografias originais salvas em raw-photos/
2. Versões limpas (sem texto) em 1080 x 1920 px em fotografias-sem-texto/
3. Versões finais com tipografia profissional na Safe Zone do Instagram Reel em telas-finais/
4. Prancha de visão geral comparativa com as 5 telas lado a lado
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia"
REEL_DIR = os.path.join(BASE_DIR, "reels", "reel-01-um-ano-sem-palavras")
RAW_DIR = os.path.join(REEL_DIR, "raw-photos")
CLEAN_DIR = os.path.join(REEL_DIR, "fotografias-sem-texto")
FINAL_DIR = os.path.join(REEL_DIR, "telas-finais")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

# Imagens geradas
IMAGE_SOURCES = [
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\f91edc96-c2ea-45c2-bb3d-bd9246ffca0e\reel01_gancho_1790290924058.jpg",
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\f91edc96-c2ea-45c2-bb3d-bd9246ffca0e\reel01_validacao_1790290942559.jpg",
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\f91edc96-c2ea-45c2-bb3d-bd9246ffca0e\reel01_esperar_1790290963172.jpg",
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\f91edc96-c2ea-45c2-bb3d-bd9246ffca0e\reel01_sinais_1790290986679.jpg",
    r"C:\Users\Gamer\.gemini\antigravity-ide\brain\f91edc96-c2ea-45c2-bb3d-bd9246ffca0e\reel01_fechamento_1790291017967.jpg",
]

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920

# Carregar fontes
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

def resize_and_crop(img, target_w, target_h):
    """Redimensiona e corta imagem centralizada para preencher exatamente o target."""
    w, h = img.size
    aspect = w / h
    target_aspect = target_w / target_h
    
    if aspect > target_aspect:
        new_w = int(h * target_aspect)
        left = (w - new_w) // 2
        img_cropped = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_aspect)
        top = (h - new_h) // 2
        img_cropped = img.crop((0, top, w, top + new_h))
        
    return img_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

def draw_pill_badge(draw, text, y, font, bg_color=(234, 228, 216), text_color=(29, 56, 43), border_color=(68, 99, 75)):
    """Desenha badge em formato de pílula centralizada com borda sutil."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    pad_x = 34
    pad_y = 16
    
    bw = tw + pad_x * 2
    bh = th + pad_y * 2
    bx = (TARGET_WIDTH - bw) // 2
    
    draw.rounded_rectangle([bx, y, bx + bw, y + bh], radius=bh//2, fill=bg_color, outline=border_color, width=2)
    tx = bx + pad_x
    ty = y + pad_y - 2
    draw.text((tx, ty), text, font=font, fill=text_color)
    return y + bh

def draw_card(overlay_draw, rect, fill_rgba, outline_rgba, radius=24, border_width=2):
    """Desenha um card translúcido no overlay."""
    overlay_draw.rounded_rectangle(rect, radius=radius, fill=fill_rgba, outline=outline_rgba, width=border_width)

def render_screens():
    screens_data = [
        {
            "id": 1,
            "raw_filename": "01-gancho.jpg",
            "clean_filename": "01-gancho-sem-texto.png",
            "final_filename": "01-gancho.png",
            "src_idx": 0,
            "badge": "DESENVOLVIMENTO DA FALA · 12 MESES",
            "card_top": 280,
            "card_height": 530,
            "title_lines": [
                "Meu filho tem 1 ano",
                "e ainda não fala",
                "nenhuma palavra."
            ],
            "highlight": "Devo me preocupar?",
            "sub_lines": [
                "Entenda o que é esperado nessa fase e quais sinais",
                "realmente merecem atenção da família."
            ],
            "tag": "Sônia Torres · Fonoaudióloga · CRFa 1-17701"
        },
        {
            "id": 2,
            "raw_filename": "02-validacao.jpg",
            "clean_filename": "02-validacao-sem-texto.png",
            "final_filename": "02-validacao.png",
            "src_idx": 1,
            "badge": "DÚVIDA FREQUENTE NO CONSULTÓRIO",
            "card_top": 280,
            "card_height": 550,
            "title_lines": [
                "Essa é uma das dúvidas",
                "mais comuns que recebo."
            ],
            "highlight": "E faz todo sentido você se perguntar isso.",
            "sub_lines": [
                "Quando comparamos com outras crianças, a angústia",
                "aumenta. Mas a comunicação começa muito antes",
                "da fala com frases prontas."
            ],
            "tag": "@torresdafono"
        },
        {
            "id": 3,
            "raw_filename": "03-o-que-esperar.jpg",
            "clean_filename": "03-o-que-esperar-sem-texto.png",
            "final_filename": "03-o-que-esperar.png",
            "src_idx": 2,
            "badge": "O QUE OBSERVAR AOS 12 MESES",
            "card_top": 270,
            "card_height": 620,
            "title_lines": [
                "Aos 12 meses, a fala",
                "já se manifesta em gestos:"
            ],
            "highlight": None,
            "checklist": [
                "Acena 'tchau' com as mãos e bate palminhas",
                "Aponta com o dedo para mostrar ou pedir algo",
                "Reconhece o próprio nome e atende quando chamada",
                "Compreende comandos simples do dia a dia (ex: 'não')",
                "Balbucia com entonação expressiva de conversa"
            ],
            "tag": "Fonte: Sociedade Brasileira de Pediatria (SBP)"
        },
        {
            "id": 4,
            "raw_filename": "04-sinais-alerta.jpg",
            "clean_filename": "04-sinais-alerta-sem-texto.png",
            "final_filename": "04-sinais-alerta.png",
            "src_idx": 3,
            "badge": "QUANDO CONVERSAR COM A FONO",
            "card_top": 270,
            "card_height": 640,
            "title_lines": [
                "Sinais que justificam",
                "uma avaliação precoce:"
            ],
            "highlight": None,
            "checklist": [
                "Aos 12 meses: não usa gestos sociais (tchau, apontar)",
                "Aos 12 meses: não parece ouvir ou reagir à voz dos pais",
                "Aos 15 meses: não balbucia nem tenta palavras simples",
                "Aos 18 meses: não fala ao menos 6 palavras com sentido"
            ],
            "footnote": "Avaliar cedo não é rotular: é acolher e estimular no momento certo.",
            "tag": "Fonte: Caderneta da Criança (Ministério da Saúde)"
        },
        {
            "id": 5,
            "raw_filename": "05-fechamento.jpg",
            "clean_filename": "05-fechamento-sem-texto.png",
            "final_filename": "05-fechamento.png",
            "src_idx": 4,
            "badge": "ORIENTAÇÃO E CUIDADO",
            "card_top": 280,
            "card_height": 580,
            "title_lines": [
                "Acompanhar de perto",
                "é a melhor forma de cuidar."
            ],
            "highlight": "Cada conquista no tempo certo.",
            "sub_lines": [
                "Salve esse vídeo para acompanhar os próximos meses",
                "ou compartilhe com uma família que precisa saber disso."
            ],
            "signature": {
                "name": "Sônia Torres",
                "title": "Fonoaudióloga · CRFa 1-17701",
                "insta": "@torresdafono",
                "ref": "SBP / Caderneta da Criança (Ministério da Saúde)"
            }
        }
    ]

    rendered_images = []

    for item in screens_data:
        src_path = IMAGE_SOURCES[item["src_idx"]]
        raw_dest = os.path.join(RAW_DIR, item["raw_filename"])
        clean_dest = os.path.join(CLEAN_DIR, item["clean_filename"])
        final_dest = os.path.join(FINAL_DIR, item["final_filename"])
        
        # 1. Copiar imagem pura para raw-photos
        shutil.copyfile(src_path, raw_dest)
        
        # 2. Carregar e redimensionar 1080x1920
        with Image.open(src_path) as orig:
            img_resized = resize_and_crop(orig, TARGET_WIDTH, TARGET_HEIGHT)
            
        # Salvar versão limpa sem texto
        img_resized.save(clean_dest, "PNG", quality=95)
        
        # 3. Composição visual da tela final
        base = img_resized.convert("RGBA")
        overlay = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
        ol_draw = ImageDraw.Draw(overlay)
        
        # Leve escurecimento superior e inferior para enquadramento cinematográfico seguro
        for y in range(400):
            ratio = 1.0 - (y / 400.0)
            a = int(140 * (ratio ** 1.4))
            ol_draw.line([(0, y), (TARGET_WIDTH, y)], fill=(15, 25, 20, a))
            
        for y in range(TARGET_HEIGHT - 350, TARGET_HEIGHT):
            ratio = (y - (TARGET_HEIGHT - 350)) / 350.0
            a = int(170 * (ratio ** 1.3))
            ol_draw.line([(0, y), (TARGET_WIDTH, y)], fill=(15, 25, 20, a))
            
        # Desenhar Card Principal de Leitura com Alto Contraste
        cx1 = 80
        cx2 = TARGET_WIDTH - 80
        cy1 = item["card_top"]
        cy2 = cy1 + item["card_height"]
        
        # Fundo do card em Verde Petróleo Profundo (#13241B) translúcido com acabamento editorial
        card_fill = (19, 36, 27, 228)
        card_border = (84, 122, 95, 180)
        draw_card(ol_draw, [cx1, cy1, cx2, cy2], card_fill, card_border, radius=28, border_width=2)
        
        # Combinar base e overlay translúcido antes de escrever textos nítidos
        composite = Image.alpha_composite(base, overlay)
        draw = ImageDraw.Draw(composite)
        
        # Badge Superior
        font_badge = get_font(FONT_BOLD_PATH, 24)
        draw_pill_badge(draw, item["badge"], cy1 + 34, font_badge, 
                        bg_color=(240, 235, 224), text_color=(25, 48, 36), border_color=(90, 130, 102))
        
        # Título Principal
        font_title = get_font(FONT_BOLD_PATH, 46)
        ty = cy1 + 106
        for line in item["title_lines"]:
            bbox = draw.textbbox((0, 0), line, font=font_title)
            lw = bbox[2] - bbox[0]
            lx = (TARGET_WIDTH - lw) // 2
            # Sombra suave de segurança
            draw.text((lx + 1, ty + 2), line, font=font_title, fill=(5, 10, 8, 200))
            draw.text((lx, ty), line, font=font_title, fill=(255, 255, 255))
            ty += 56
            
        # Destaque em Terracota / Salmão suave
        if item.get("highlight"):
            ty += 10
            font_hl = get_font(FONT_BOLD_PATH, 34)
            hl = item["highlight"]
            bbox = draw.textbbox((0, 0), hl, font=font_hl)
            lw = bbox[2] - bbox[0]
            lx = (TARGET_WIDTH - lw) // 2
            draw.text((lx + 1, ty + 2), hl, font=font_hl, fill=(10, 15, 12, 200))
            draw.text((lx, ty), hl, font=font_hl, fill=(245, 168, 130))
            ty += 46

        # Linhas de Subtítulo / Contexto
        if item.get("sub_lines"):
            ty += 14
            font_sub = get_font(FONT_REGULAR_PATH, 28)
            for sline in item["sub_lines"]:
                bbox = draw.textbbox((0, 0), sline, font=font_sub)
                lw = bbox[2] - bbox[0]
                lx = (TARGET_WIDTH - lw) // 2
                draw.text((lx, ty), sline, font=font_sub, fill=(225, 232, 226))
                ty += 38

        # Checklist com marcadores
        if item.get("checklist"):
            ty += 16
            font_chk = get_font(FONT_SEMIBOLD_PATH, 27)
            dot_color = (235, 164, 125)  # Terracota acolhedor
            for point in item["checklist"]:
                px = cx1 + 45
                # Marcador em círculo
                draw.ellipse([px, ty + 10, px + 12, ty + 22], fill=dot_color)
                # Texto do marcador
                draw.text((px + 28, ty + 2), point, font=font_chk, fill=(240, 244, 240))
                ty += 44

        # Nota de rodapé dentro do card (Slide 4)
        if item.get("footnote"):
            ty += 16
            font_fn = get_font(FONT_BOLD_PATH, 25)
            fn_text = item["footnote"]
            bbox = draw.textbbox((0, 0), fn_text, font=font_fn)
            lw = bbox[2] - bbox[0]
            lx = (TARGET_WIDTH - lw) // 2
            draw.text((lx, ty), fn_text, font=font_fn, fill=(245, 200, 150))

        # Assinatura institucional (Slide 5)
        if item.get("signature"):
            ty += 20
            sig = item["signature"]
            font_sig_name = get_font(FONT_BOLD_PATH, 32)
            font_sig_role = get_font(FONT_SEMIBOLD_PATH, 26)
            font_sig_ref = get_font(FONT_REGULAR_PATH, 22)
            
            # Linha divisória fina
            div_y = ty
            draw.line([(cx1 + 80, div_y), (cx2 - 80, div_y)], fill=(80, 115, 92, 160), width=1)
            ty += 24
            
            # Nome e CRFa
            bbox_name = draw.textbbox((0, 0), sig["name"], font=font_sig_name)
            draw.text(((TARGET_WIDTH - (bbox_name[2] - bbox_name[0])) // 2, ty), sig["name"], font=font_sig_name, fill=(255, 255, 255))
            ty += 42
            
            role_text = f"{sig['title']} · {sig['insta']}"
            bbox_role = draw.textbbox((0, 0), role_text, font=font_sig_role)
            draw.text(((TARGET_WIDTH - (bbox_role[2] - bbox_role[0])) // 2, ty), role_text, font=font_sig_role, fill=(225, 235, 228))
            ty += 38
            
            ref_text = f"Fonte: {sig['ref']}"
            bbox_ref = draw.textbbox((0, 0), ref_text, font=font_sig_ref)
            draw.text(((TARGET_WIDTH - (bbox_ref[2] - bbox_ref[0])) // 2, ty), ref_text, font=font_sig_ref, fill=(185, 200, 190))

        # Tag de identificação no rodapé do card (Slide 1 a 4)
        elif item.get("tag"):
            font_tag = get_font(FONT_REGULAR_PATH, 22)
            tag_text = item["tag"]
            bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
            lx = (TARGET_WIDTH - (bbox[2] - bbox[0])) // 2
            draw.text((lx, cy2 - 40), tag_text, font=font_tag, fill=(180, 205, 190))

        # Indicador de tela (Ex: 1/5, 2/5...) no rodapé protegido
        screen_idx_text = f"{item['id']} / 5"
        font_idx = get_font(FONT_BOLD_PATH, 24)
        bbox_idx = draw.textbbox((0, 0), screen_idx_text, font=font_idx)
        draw.text(((TARGET_WIDTH - (bbox_idx[2] - bbox_idx[0])) // 2, TARGET_HEIGHT - 180), 
                  screen_idx_text, font=font_idx, fill=(240, 245, 240, 210))

        # Salvar tela final
        final_img = composite.convert("RGB")
        final_img.save(final_dest, "PNG", quality=95)
        rendered_images.append(final_img)
        print(f"Salvo: {final_dest}")

    # Gerar Prancha Panorâmica Geral com as 5 Telas Lado a Lado
    print("Gerando prancha de visão geral comparativa...")
    thumb_w = 400
    thumb_h = int(thumb_w * (TARGET_HEIGHT / TARGET_WIDTH))  # 711 px
    spacing = 30
    board_padding = 60
    
    total_w = (thumb_w * 5) + (spacing * 4) + (board_padding * 2)
    header_h = 160
    footer_h = 100
    total_h = thumb_h + header_h + footer_h + (board_padding * 2)
    
    board = Image.new("RGB", (total_w, total_h), (245, 242, 235))
    b_draw = ImageDraw.Draw(board)
    
    # Header da prancha
    f_header_title = get_font(FONT_BOLD_PATH, 48)
    f_header_sub = get_font(FONT_REGULAR_PATH, 30)
    
    b_title = "Reel 01 — Meu filho tem 1 ano e ainda não fala nenhuma palavra. Devo me preocupar?"
    b_sub = "Sônia Torres · Fonoaudióloga · CRFa 1-17701 · Visão Geral das 5 Telas (9:16 · 1080 x 1920 px)"
    
    b_draw.text((board_padding, board_padding), b_title, font=f_header_title, fill=(25, 48, 36))
    b_draw.text((board_padding, board_padding + 64), b_sub, font=f_header_sub, fill=(68, 99, 75))
    
    # Inserir thumbnails
    cur_x = board_padding
    thumb_y = board_padding + header_h
    
    for idx, screen_img in enumerate(rendered_images):
        t_img = screen_img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        # Borda sutil de moldura
        b_draw.rectangle([cur_x - 3, thumb_y - 3, cur_x + thumb_w + 3, thumb_y + thumb_h + 3], 
                         outline=(210, 200, 185), width=3)
        board.paste(t_img, (cur_x, thumb_y))
        
        # Legenda inferior de cada tela
        f_lbl = get_font(FONT_BOLD_PATH, 24)
        lbl_text = f"Tela 0{idx+1}"
        b_draw.text((cur_x + 10, thumb_y + thumb_h + 16), lbl_text, font=f_lbl, fill=(30, 50, 40))
        
        cur_x += thumb_w + spacing

    board_dest = os.path.join(FINAL_DIR, "prancha-visao-geral.png")
    board.save(board_dest, "PNG", quality=95)
    print(f"Prancha salva com sucesso em: {board_dest}")

if __name__ == "__main__":
    render_screens()
