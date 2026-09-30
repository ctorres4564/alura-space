import os
import subprocess
import shutil

def run_cmd(cmd, step_name):
    print(f"\n--- Iniciando: {step_name} ---")
    print("Comando:", " ".join(cmd) if isinstance(cmd, list) else cmd)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print(f"ERRO em {step_name}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
        raise RuntimeError(f"Falha ao executar {step_name}")
    print(f"Sucesso: {step_name}")
    return result.stdout

def build_reel():
    base_dir = r"C:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia\reels\reel-afasia-avc-familia"
    local_dir = r"C:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia\video-falado-afasia-avc-familia"
    tmp_dir = os.path.join(base_dir, "_tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    clipe_1 = os.path.join(local_dir, "clipe-1.mp4")
    clipe_2 = os.path.join(local_dir, "clipe-2.mp4")
    tela_a = os.path.join(base_dir, "tela-a-o-que-e-afasia.png")
    tela_b = os.path.join(base_dir, "tela-b-sinais.png")
    tela_c = os.path.join(base_dir, "tela-c-como-ajudar.png")
    card_contato = os.path.join(base_dir, "06-contatos.png")

    seg_1 = os.path.join(tmp_dir, "seg-1-abertura.mp4")
    seg_2 = os.path.join(tmp_dir, "seg-2-tela-a.mp4")
    seg_3 = os.path.join(tmp_dir, "seg-3-tela-b.mp4")
    seg_4 = os.path.join(tmp_dir, "seg-4-tela-c.mp4")
    seg_5 = os.path.join(tmp_dir, "seg-5-encerramento.mp4")
    seg_6 = os.path.join(tmp_dir, "seg-6-contatos.mp4")

    # 1. Normalizar clipe 1 (Sônia abertura)
    cmd_seg1 = (
        f'ffmpeg -y -i "{clipe_1}" '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" '
        f'-r 30 -c:v libx264 -preset slow -crf 18 -c:a aac -ar 44100 -ac 2 "{seg_1}"'
    )
    run_cmd(cmd_seg1, "Segmento 1 - Sônia Abertura")

    # 2. Tela A (O que é afasia) com Ken Burns zoom lento
    cmd_seg2 = (
        f'ffmpeg -y -loop 1 -i "{tela_a}" '
        f'-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z=\'min(zoom+0.0006,1.04)\':d=125:s=1080x1920:fps=30,format=yuv420p" '
        f'-t 4.2 -r 30 -c:v libx264 -preset slow -crf 18 -c:a aac -shortest -pix_fmt yuv420p "{seg_2}"'
    )
    run_cmd(cmd_seg2, "Segmento 2 - Tela A")

    # 3. Tela B (Sinais)
    cmd_seg3 = (
        f'ffmpeg -y -loop 1 -i "{tela_b}" '
        f'-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z=\'min(zoom+0.0006,1.04)\':d=125:s=1080x1920:fps=30,format=yuv420p" '
        f'-t 4.2 -r 30 -c:v libx264 -preset slow -crf 18 -c:a aac -shortest -pix_fmt yuv420p "{seg_3}"'
    )
    run_cmd(cmd_seg3, "Segmento 3 - Tela B")

    # 4. Tela C (Como ajudar em casa)
    cmd_seg4 = (
        f'ffmpeg -y -loop 1 -i "{tela_c}" '
        f'-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z=\'min(zoom+0.0006,1.04)\':d=125:s=1080x1920:fps=30,format=yuv420p" '
        f'-t 4.2 -r 30 -c:v libx264 -preset slow -crf 18 -c:a aac -shortest -pix_fmt yuv420p "{seg_4}"'
    )
    run_cmd(cmd_seg4, "Segmento 4 - Tela C")

    # 5. Normalizar clipe 2 (Sônia encerramento)
    cmd_seg5 = (
        f'ffmpeg -y -i "{clipe_2}" '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" '
        f'-r 30 -c:v libx264 -preset slow -crf 18 -c:a aac -ar 44100 -ac 2 "{seg_5}"'
    )
    run_cmd(cmd_seg5, "Segmento 5 - Sônia Encerramento")

    # 6. Card de contatos (fade in 0.3s, 3.3s de duração)
    cmd_seg6 = (
        f'ffmpeg -y -loop 1 -i "{card_contato}" '
        f'-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 '
        f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fade=t=in:st=0:d=0.3,format=yuv420p" '
        f'-t 3.3 -r 30 -c:v libx264 -preset slow -crf 18 -c:a aac -shortest -pix_fmt yuv420p "{seg_6}"'
    )
    run_cmd(cmd_seg6, "Segmento 6 - Card de Contatos")

    # 7. Concatenação dos 6 segmentos
    output_final = os.path.join(base_dir, "reel-afasia-avc-final.mp4")
    local_output_final = os.path.join(local_dir, "reel-afasia-avc-final.mp4")

    cmd_concat = (
        f'ffmpeg -y '
        f'-i "{seg_1}" -i "{seg_2}" -i "{seg_3}" -i "{seg_4}" -i "{seg_5}" -i "{seg_6}" '
        f'-filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a][4:v][4:a][5:v][5:a]concat=n=6:v=1:a=1[outv][outa]" '
        f'-map "[outv]" -map "[outa]" -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 192k '
        f'-r 30 -pix_fmt yuv420p "{output_final}"'
    )
    run_cmd(cmd_concat, "Concatenação Final dos 6 Segmentos")

    # Copiar também para local_dir
    shutil.copyfile(output_final, local_output_final)
    print(f"Vídeo final duplicado para pasta local: {local_output_final}")

    # Limpeza da pasta _tmp
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
        print("Pasta temporária _tmp/ removida com sucesso!")

if __name__ == "__main__":
    build_reel()
