import os
from PIL import Image, ImageDraw, ImageFont

def render_screens(generated_images_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    no_text_dir = os.path.join(output_dir, "fotografias-sem-texto")
    os.makedirs(no_text_dir, exist_ok=True)

    files = os.listdir(generated_images_dir)
    img_a_file = [f for f in files if f.startswith("tela_a_sem_texto") and f.endswith(".jpg")][-1]
    img_b_file = [f for f in files if f.startswith("tela_b_sem_texto") and f.endswith(".jpg")][-1]
    img_c_file = [f for f in files if f.startswith("tela_c_sem_texto") and f.endswith(".jpg")][-1]

    screens_data = [
        {
            "id": "tela-a",
            "img_path": os.path.join(generated_images_dir, img_a_file),
            "clean_name": "tela-a-sem-texto.png",
            "final_name": "tela-a-o-que-e-afasia.png",
            "lines": [
                "Afasia não é confusão mental.",
                "É uma dificuldade de linguagem",
                "depois de uma lesão no cérebro."
            ],
            "center_y": 500
        },
        {
            "id": "tela-b",
            "img_path": os.path.join(generated_images_dir, img_b_file),
            "clean_name": "tela-b-sem-texto.png",
            "final_name": "tela-b-sinais.png",
            "lines": [
                "Pode vir de repente: dificuldade",
                "para falar, entender ou escrever",
                "o que antes era simples."
            ],
            "center_y": 420
        },
        {
            "id": "tela-c",
            "img_path": os.path.join(generated_images_dir, img_c_file),
            "clean_name": "tela-c-sem-texto.png",
            "final_name": "tela-c-como-ajudar.png",
            "lines": [
                "Fale de frente, mais devagar,",
                "com frases curtas. Espere a resposta.",
                "Sem pressa, sem infantilizar."
            ],
            "center_y": 420
        }
    ]

    font_paths = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    font_path = None
    for p in font_paths:
        if os.path.exists(p):
            font_path = p
            break

    font_size = 50
    line_spacing = 22
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    for item in screens_data:
        im = Image.open(item["img_path"]).convert("RGBA")
        target_w, target_h = 1080, 1920
        
        im_ratio = im.width / im.height
        target_ratio = target_w / target_h
        if im_ratio > target_ratio:
            new_h = target_h
            new_w = int(new_h * im_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / im_ratio)
            
        im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        im = im.crop((left, top, left + target_w, top + target_h))

        clean_save_path = os.path.join(no_text_dir, item["clean_name"])
        im.convert("RGB").save(clean_save_path, "PNG")
        print(f"Salvo sem texto: {clean_save_path}")

        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)

        lines = item["lines"]
        line_boxes = [draw_overlay.textbbox((0, 0), line, font=font) for line in lines]
        line_widths = [b[2] - b[0] for b in line_boxes]
        line_heights = [b[3] - b[1] for b in line_boxes]
        
        total_text_h = sum(line_heights) + line_spacing * (len(lines) - 1)
        max_line_w = max(line_widths)

        center_y = item["center_y"]
        start_y = center_y - (total_text_h // 2)

        if start_y < 230:
            start_y = 230
        if start_y + total_text_h > 1460:
            start_y = 1460 - total_text_h

        pad_x = 55
        pad_y = 40
        box_x0 = max(35, (target_w - max_line_w) // 2 - pad_x)
        box_x1 = min(target_w - 35, (target_w + max_line_w) // 2 + pad_x)
        box_y0 = start_y - pad_y
        box_y1 = start_y + total_text_h + pad_y

        draw_overlay.rounded_rectangle(
            [box_x0, box_y0, box_x1, box_y1],
            radius=24,
            fill=(18, 18, 20, 165)
        )

        curr_y = start_y
        for i, line in enumerate(lines):
            lw = line_widths[i]
            lx = (target_w - lw) // 2
            
            draw_overlay.text((lx + 2, curr_y + 2), line, font=font, fill=(0, 0, 0, 200))
            draw_overlay.text((lx, curr_y), line, font=font, fill=(255, 255, 255, 255))
            curr_y += line_heights[i] + line_spacing

        final_im = Image.alpha_composite(im, overlay)
        final_save_path = os.path.join(output_dir, item["final_name"])
        final_im.convert("RGB").save(final_save_path, "PNG")
        print(f"Salvo final com texto: {final_save_path}")

if __name__ == "__main__":
    generated_dir = r"C:\Users\Gamer\.gemini\antigravity-ide\brain\313089f3-b824-473c-92e7-50c627569f63"
    output_dirs = [
        r"C:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia\reels\reel-afasia-avc-familia",
        r"C:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia\video-falado-afasia-avc-familia\assets"
    ]
    for out in output_dirs:
        render_screens(generated_dir, out)
