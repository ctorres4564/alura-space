"""
Script de Produção Audiovisual Automatizada — Carrossel em Vídeo / Reel
Tema: "O que esperar da fala, por idade"
Cliente: Sônia Torres — Fonoaudióloga (CRFa 1-17701)

Gera:
1. Frames verticais adaptados para Reel 9:16 (1080 x 1920 px) com Safe Zone
2. Vídeo Reel Vertical 9:16 (1080 x 1920 px, 30fps, áudio Warm Hope piano)
3. Vídeo Carrossel Feed 4:5 (1080 x 1350 px, 30fps, áudio Warm Hope piano)
4. Roteiro de publicação e minutagem em reels/reel-o-que-esperar-da-fala-por-idade/
"""

import os
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia"
SLIDES_DIR = os.path.join(BASE_DIR, "carrosseis", "carrossel-o-que-esperar-da-fala-por-idade", "slides-finais")
OUTPUT_DIR = os.path.join(BASE_DIR, "reels", "reel-o-que-esperar-da-fala-por-idade")
FRAMES_REEL_DIR = os.path.join(OUTPUT_DIR, "frames-reel-9x16")
TMP_DIR = os.path.join(OUTPUT_DIR, "_tmp")

AUDIO_PATH = os.path.join(BASE_DIR, "reels", "reel-tres-maneiras-conversar", "Warm Hope.mp3")
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "PlusJakartaSans-Variable.ttf")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRAMES_REEL_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

# Lista ordenada de slides e tempos de exibição (em segundos)
SLIDES_INFO = [
    ("01-capa.png", 4.2),
    ("02-0-a-6-meses.png", 4.8),
    ("03-7-a-11-meses.png", 4.8),
    ("04-1-ano.png", 4.8),
    ("05-1-ano-e-6-meses.png", 4.8),
    ("06-2-anos.png", 4.8),
    ("07-3-a-6-anos.png", 5.2),
    ("08-observe-alertas.png", 5.4),
    ("09-slide-resumo.png", 5.8),
    ("10-encerramento.png", 4.2),
]

COLOR_BEIGE_BG = (250, 247, 242)      # #FAF7F2
COLOR_DEEP_GREEN = (29, 56, 43)        # #1D382B
COLOR_MEDIUM_GREEN = (68, 99, 75)      # #44634B
COLOR_MUTED_BORDER = (220, 230, 224)

def get_font(size, weight=700):
    try:
        font = ImageFont.truetype(FONT_PATH, size)
        if hasattr(font, 'set_variation_by_axes'):
            font.set_variation_by_axes([weight])
        return font
    except Exception:
        if os.path.exists(r"C:\Windows\Fonts\segoeuib.ttf"):
            return ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", size)
        return ImageFont.load_default()

def run_cmd(cmd, desc):
    print(f"\n--- {desc} ---")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(f"Erro em: {desc}")
        print(f"STDOUT: {res.stdout}")
        print(f"STDERR: {res.stderr}")
        raise RuntimeError(f"Falha ao executar: {desc}")
    return res.stdout

def prepare_reel_frames():
    """
    Gera frames 1080 x 1920 (9:16) a partir dos slides 1080 x 1350.
    Enquadra o slide perfeitamente no centro vertical, adicionando cabeçalho
    e rodapé discretos fora das zonas de corte do Instagram.
    """
    font_top = get_font(21, weight=700)
    font_bot = get_font(20, weight=600)

    for i, (slide_name, _) in enumerate(SLIDES_INFO, start=1):
        src_path = os.path.join(SLIDES_DIR, slide_name)
        dest_path = os.path.join(FRAMES_REEL_DIR, f"frame_{i:02d}.png")

        slide_img = Image.open(src_path).convert("RGBA")

        # Canvas 1080 x 1920 em bege institucional
        reel_canvas = Image.new("RGBA", (1080, 1920), COLOR_BEIGE_BG)
        draw = ImageDraw.Draw(reel_canvas)

        # Barra decorativa de margem superior (Y=180 a 220, safe zone do Reel)
        top_text = "SÔNIA TORRES  ·  FONOAUDIOLOGIA INFANTIL"
        bbox_t = draw.textbbox((0, 0), top_text, font=font_top)
        tw_t = bbox_t[2] - bbox_t[0]
        tx_t = (1080 - tw_t) // 2
        draw.text((tx_t, 205), top_text, font=font_top, fill=COLOR_MEDIUM_GREEN)
        draw.line([(tx_t - 25, 218), (tx_t - 10, 218)], fill=COLOR_MUTED_BORDER, width=2)
        draw.line([(tx_t + tw_t + 10, 218), (tx_t + tw_t + 25, 218)], fill=COLOR_MUTED_BORDER, width=2)

        # Colagem do slide 1080x1350 na posição vertical central
        slide_y = 265 # De 265 a 1615 (total 1350 px de altura)
        reel_canvas.alpha_composite(slide_img, (0, slide_y))

        # Indicador de rodapé (Y=1650 a 1700, acima da barra de legenda do Reel)
        bot_text = f"PARTE {i:02d} DE 10  •  TOQUE PARA PAUSAR" if i < 10 else "COMPARTILHE COM OUTRAS FAMÍLIAS  🔖"
        bbox_b = draw.textbbox((0, 0), bot_text, font=font_bot)
        tw_b = bbox_b[2] - bbox_b[0]
        tx_b = (1080 - tw_b) // 2
        draw.text((tx_b, 1655), bot_text, font=font_bot, fill=COLOR_DEEP_GREEN)

        reel_canvas.convert("RGB").save(dest_path, "PNG")
    print(f"10 frames verticais 9:16 gerados em: {FRAMES_REEL_DIR}")

def build_video_4x5():
    """
    Gera o vídeo no formato 4:5 (1080 x 1350 px) para carrossel/feed do Instagram.
    """
    total_duration = sum(dur for _, dur in SLIDES_INFO)
    print(f"\nConstruindo Vídeo 4:5 (Duração total estimada: {total_duration:.1f}s)...")

    # 1. Gerar mini-clipes para cada slide
    concat_list_path = os.path.join(TMP_DIR, "concat_4x5.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for i, (slide_name, dur) in enumerate(SLIDES_INFO, start=1):
            slide_path = os.path.join(SLIDES_DIR, slide_name)
            seg_out = os.path.join(TMP_DIR, f"seg_4x5_{i:02d}.mp4")

            # Cria clipe de vídeo estático de alta qualidade
            cmd = (
                f'ffmpeg -y -loop 1 -i "{slide_path}" '
                f'-c:v libx264 -t {dur} -r 30 -pix_fmt yuv420p -preset fast -crf 18 '
                f'"{seg_out}"'
            )
            run_cmd(cmd, f"Segmento 4:5 #{i:02d} ({dur}s)")
            f.write(f"file '{seg_out.replace(chr(92), '/')}'\n")

    # 2. Concatenar clipes
    merged_video = os.path.join(TMP_DIR, "merged_4x5_video.mp4")
    cmd_cat = (
        f'ffmpeg -y -f concat -safe 0 -i "{concat_list_path}" '
        f'-c copy "{merged_video}"'
    )
    run_cmd(cmd_cat, "Concatenação dos segmentos 4:5")

    # 3. Adicionar trilha sonora com fade-in e fade-out sincronizados
    final_video = os.path.join(OUTPUT_DIR, "video-carrossel-4x5.mp4")
    fade_out_start = max(1.0, total_duration - 2.5)

    cmd_mux = (
        f'ffmpeg -y -i "{merged_video}" -stream_loop -1 -i "{AUDIO_PATH}" '
        f'-filter_complex "[1:a]afade=t=in:ss=0:d=1.5,afade=t=out:st={fade_out_start:.2f}:d=2.5,volume=0.85[aout]" '
        f'-map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -t {total_duration:.2f} '
        f'"{final_video}"'
    )
    run_cmd(cmd_mux, "Geração final do Vídeo 4:5 com áudio Warm Hope")
    print(f"Vídeo 4:5 gerado com sucesso: {final_video}")

def build_video_9x16():
    """
    Gera o vídeo vertical para Instagram Reels / Stories (1080 x 1920 px).
    """
    total_duration = sum(dur for _, dur in SLIDES_INFO)
    print(f"\nConstruindo Vídeo Reel 9:16 (Duração total estimada: {total_duration:.1f}s)...")

    # 1. Gerar mini-clipes verticais
    concat_list_path = os.path.join(TMP_DIR, "concat_9x16.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for i, (_, dur) in enumerate(SLIDES_INFO, start=1):
            frame_path = os.path.join(FRAMES_REEL_DIR, f"frame_{i:02d}.png")
            seg_out = os.path.join(TMP_DIR, f"seg_9x16_{i:02d}.mp4")

            cmd = (
                f'ffmpeg -y -loop 1 -i "{frame_path}" '
                f'-c:v libx264 -t {dur} -r 30 -pix_fmt yuv420p -preset fast -crf 18 '
                f'"{seg_out}"'
            )
            run_cmd(cmd, f"Segmento 9:16 #{i:02d} ({dur}s)")
            f.write(f"file '{seg_out.replace(chr(92), '/')}'\n")

    # 2. Concatenar clipes
    merged_video = os.path.join(TMP_DIR, "merged_9x16_video.mp4")
    cmd_cat = (
        f'ffmpeg -y -f concat -safe 0 -i "{concat_list_path}" '
        f'-c copy "{merged_video}"'
    )
    run_cmd(cmd_cat, "Concatenação dos segmentos 9:16")

    # 3. Adicionar trilha sonora
    final_video = os.path.join(OUTPUT_DIR, "video-reel-9x16.mp4")
    fade_out_start = max(1.0, total_duration - 2.5)

    cmd_mux = (
        f'ffmpeg -y -i "{merged_video}" -stream_loop -1 -i "{AUDIO_PATH}" '
        f'-filter_complex "[1:a]afade=t=in:ss=0:d=1.5,afade=t=out:st={fade_out_start:.2f}:d=2.5,volume=0.85[aout]" '
        f'-map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -t {total_duration:.2f} '
        f'"{final_video}"'
    )
    run_cmd(cmd_mux, "Geração final do Vídeo Reel 9:16 com áudio Warm Hope")
    print(f"Vídeo Reel 9:16 gerado com sucesso: {final_video}")

def cleanup():
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR, ignore_errors=True)
    print("Arquivos temporários removidos.")

def main():
    print("Iniciando pipeline de geração audiovisual...")
    prepare_reel_frames()
    build_video_4x5()
    build_video_9x16()
    cleanup()
    print("\nTodos os vídeos foram gerados com sucesso!")

if __name__ == "__main__":
    main()
