import os
import json
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    # Procura fontes no Windows
    candidates = [
        "C:/Windows/Fonts/cambriab.ttf" if bold else "C:/Windows/Fonts/cambria.ttc",
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()

def render_title_card(line1_text, line2_text, out_path):
    width, height = 1920, 1080
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_sub = get_font(26, bold=True)
    font_main = get_font(34, bold=True)

    # Mede textos
    bbox_sub = draw.textbbox((0, 0), line1_text, font=font_sub)
    bbox_main = draw.textbbox((0, 0), line2_text, font=font_main)

    w_sub = bbox_sub[2] - bbox_sub[0]
    h_sub = bbox_sub[3] - bbox_sub[1]
    w_main = bbox_main[2] - bbox_main[0]
    h_main = bbox_main[3] - bbox_main[1]

    card_content_width = max(w_sub, w_main) + 40
    card_content_height = h_sub + h_main + 40

    # Posição: Canto superior esquerdo
    pad_x = 75
    pad_y = 70

    # Fundo translúcido com cantos arredondados
    rect = [pad_x, pad_y, pad_x + card_content_width + 30, pad_y + card_content_height + 15]
    draw.rounded_rectangle(rect, radius=8, fill=(15, 15, 20, 190), outline=(212, 175, 55, 140), width=1)

    # Linha vertical dourada imperial à esquerda
    gold_bar_x = pad_x + 12
    draw.line([(gold_bar_x, pad_y + 12), (gold_bar_x, pad_y + card_content_height + 3)], fill=(212, 175, 55, 255), width=4)

    # Texto Linha 1 (Data / Local em dourado)
    text_x = gold_bar_x + 18
    text_y1 = pad_y + 14
    draw.text((text_x, text_y1), line1_text, font=font_sub, fill=(243, 229, 171, 240))

    # Texto Linha 2 (Título em branco / marfim)
    text_y2 = text_y1 + h_sub + 12
    draw.text((text_x, text_y2), line2_text, font=font_main, fill=(255, 255, 255, 255))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")

def main():
    with open("src/timeline_manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)

    os.makedirs("assets/title_cards", exist_ok=True)
    count = 0
    for block in manifest["blocks"]:
        for scene in block["scenes"]:
            card = scene.get("card")
            if card:
                card_filename = f"assets/title_cards/{scene['id']}.png"
                render_title_card(card["line1"], card["line2"], card_filename)
                card["asset_path"] = card_filename
                count += 1

    # Atualiza o manifesto com os caminhos dos assets
    with open("src/timeline_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Total de {count} cartões históricos gerados com sucesso em assets/title_cards/!")

if __name__ == "__main__":
    main()
