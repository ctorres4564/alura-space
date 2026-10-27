from PIL import Image, ImageDraw, ImageFont
import os

def create_cover():
    print("Gerando capa vertical oficial 1080x1920...")
    img_path = "assets/images/retrato_mulher.jpg"
    base_img = Image.open(img_path).convert("RGBA")
    
    # Redimensiona mantendo proporção e centralizando em 1080x1920
    target_w, target_h = 1080, 1920
    
    # Crop centralizado 1080x1920
    base_img = base_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Criar camada de gradiente escuro superior e inferior para destaque de texto e contraste cinematográfico
    gradient = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_grad = ImageDraw.Draw(gradient)
    
    # Gradiente escuro no topo e na base
    for y in range(target_h):
        if y < 700:
            # Topo escurecido para o título
            alpha = int(220 * (1.0 - y / 700.0) ** 1.3)
        elif y > 1400:
            # Base escurecida para subtítulo e safe area
            alpha = int(230 * ((y - 1400.0) / 520.0) ** 1.2)
        else:
            alpha = 40  # leve vinheta central
        draw_grad.line([(0, y), (target_w, y)], fill=(8, 10, 14, alpha))
        
    combined = Image.alpha_composite(base_img, gradient)
    draw = ImageDraw.Draw(combined)
    
    # Fontes
    # Tentando fontes do sistema Windows (Arial, Impact, Trebuchet MS, Segoe UI)
    def get_font(size, bold=True):
        font_paths = [
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/impact.ttf",
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    return ImageFont.truetype(fp, size)
                except:
                    pass
        return ImageFont.load_default()

    font_top = get_font(42, bold=True)
    font_main = get_font(84, bold=True)
    font_liberdade = get_font(98, bold=True)
    font_sub = get_font(36, bold=False)
    
    # 1. Kicker superior
    kicker = "DOCUMENTÁRIO POLÍTICO"
    k_bbox = draw.textbbox((0, 0), kicker, font=font_top)
    k_w = k_bbox[2] - k_bbox[0]
    draw.text(((target_w - k_w) // 2, 220), kicker, font=font_top, fill=(200, 200, 210, 240))
    
    # Linha divisória sutil
    draw.line([(target_w // 2 - 80, 280), (target_w // 2 + 80, 280)], fill=(217, 30, 54, 255), width=4)
    
    # 2. Título principal em caixa alta
    # "QUEM TEM MEDO DA"
    # "LIBERDADE" (em vermelho vivo / destaque)
    # "DAS MULHERES?"
    t1 = "QUEM TEM MEDO DA"
    t2 = "LIBERDADE"
    t3 = "DAS MULHERES?"
    
    # Linha 1
    bbox1 = draw.textbbox((0, 0), t1, font=font_main)
    w1 = bbox1[2] - bbox1[0]
    y1 = 320
    # Sombra
    draw.text(((target_w - w1) // 2 + 3, y1 + 3), t1, font=font_main, fill=(0, 0, 0, 255))
    draw.text(((target_w - w1) // 2, y1), t1, font=font_main, fill=(255, 255, 255, 255))
    
    # Linha 2 (Destaque em Vermelho Profundo / Carmesim de Tensão)
    bbox2 = draw.textbbox((0, 0), t2, font=font_liberdade)
    w2 = bbox2[2] - bbox2[0]
    y2 = y1 + 105
    # Sombra
    draw.text(((target_w - w2) // 2 + 4, y2 + 4), t2, font=font_liberdade, fill=(0, 0, 0, 255))
    draw.text(((target_w - w2) // 2, y2), t2, font=font_liberdade, fill=(225, 35, 55, 255))
    
    # Linha 3
    bbox3 = draw.textbbox((0, 0), t3, font=font_main)
    w3 = bbox3[2] - bbox3[0]
    y3 = y2 + 115
    # Sombra
    draw.text(((target_w - w3) // 2 + 3, y3 + 3), t3, font=font_main, fill=(0, 0, 0, 255))
    draw.text(((target_w - w3) // 2, y3), t3, font=font_main, fill=(255, 255, 255, 255))
    
    # 3. Rodapé / Subtítulo Editorial
    sub = "GÊNERO, POLÍTICA E DISPUTA PELO PODER"
    bbox_sub = draw.textbbox((0, 0), sub, font=font_sub)
    w_sub = bbox_sub[2] - bbox_sub[0]
    y_sub = 1720
    # Sombra
    draw.text(((target_w - w_sub) // 2 + 2, y_sub + 2), sub, font=font_sub, fill=(0, 0, 0, 255))
    draw.text(((target_w - w_sub) // 2, y_sub), sub, font=font_sub, fill=(210, 215, 225, 255))
    
    # Salvar nos destinos
    os.makedirs("VIDEO_LIBERDADE_MULHERES_FINAL", exist_ok=True)
    out_cover = "VIDEO_LIBERDADE_MULHERES_FINAL/capa_liberdade_mulheres.png"
    combined.convert("RGB").save(out_cover, "PNG", quality=95)
    combined.convert("RGB").save("assets/images/capa_liberdade_mulheres.png", "PNG", quality=95)
    print(f"Capa gerada com sucesso em: {out_cover}")

if __name__ == "__main__":
    create_cover()
