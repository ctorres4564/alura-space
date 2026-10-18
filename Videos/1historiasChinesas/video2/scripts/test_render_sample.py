import subprocess
import os

def render_sample():
    os.makedirs("docs/samples", exist_ok=True)
    out_video = "docs/samples/sample_bloco1_card.mp4"
    card_img = "assets/title_cards/B1-1.png"
    
    # Input buscado em 77.28s com duração de 10s
    # O tempo dentro do filtro é relativo ao trecho (0 a 10s)
    filter_complex = (
        "[1:v]format=rgba,fade=t=in:st=0.5:d=0.5:alpha=1,fade=t=out:st=6.5:d=0.5:alpha=1[card];"
        "[0:v][card]overlay=0:0:enable='between(t,0.5,7.0)'[v]"
    )
    
    cmd = [
        "ffmpeg",
        "-ss", "77.28", "-t", "10", "-i", "historias chinesas 2/historias chinesas 2.mp4",
        "-loop", "1", "-t", "10", "-i", card_img,
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-y", out_video
    ]
    print("Renderizando amostra de teste corrigida...")
    subprocess.run(cmd, check=True)
    print(f"Amostra renderizada com sucesso: {out_video}")

    # Extrai um frame em 3s da amostra para conferência visual
    sample_frame = "docs/samples/sample_bloco1_frame.jpg"
    cmd_frame = ["ffmpeg", "-ss", "3", "-i", out_video, "-vframes", "1", "-y", sample_frame]
    subprocess.run(cmd_frame, check=True)
    print(f"Frame extraído para: {sample_frame}")

if __name__ == "__main__":
    render_sample()
