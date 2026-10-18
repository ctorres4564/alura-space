import os
import sys
import glob
import wave
import zipfile
import subprocess
import xml.etree.ElementTree as ET

def read_docx_text(path):
    if not os.path.exists(path):
        return ""
    z = zipfile.ZipFile(path)
    tree = ET.fromstring(z.read("word/document.xml"))
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs = []
    for p in tree.iterfind('.//w:p', namespaces):
        t = ''.join(p.itertext())
        if t.strip():
            paragraphs.append(t)
    return '\n'.join(paragraphs)

def get_wav_duration(path):
    try:
        with wave.open(path, 'rb') as w:
            frames = w.getnframes()
            rate = w.getframerate()
            return frames / float(rate)
    except Exception as e:
        return 0.0

def get_video_info(path):
    try:
        # call ffmpeg -i to get duration and streams
        res = subprocess.run(["ffmpeg", "-i", path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="ignore")
        info = []
        for line in res.stderr.splitlines():
            if "Duration:" in line or "Stream #" in line:
                info.append(line.strip())
        return " | ".join(info)
    except Exception as e:
        return str(e)

def main():
    print("=== INSPEÇÃO GERAL DO PROJETO ===")
    
    # 1. Audios
    audio_files = sorted(glob.glob("audios/*.wav"))
    print(f"\nTotal de arquivos de áudio: {len(audio_files)}")
    total_sec = 0.0
    for af in audio_files:
        dur = get_wav_duration(af)
        total_sec += dur
        srt_exists = os.path.exists(af.replace(".wav", ".srt"))
        print(f"  {os.path.basename(af):<25} -> {dur:6.2f}s ({dur/60:4.2f} min) | SRT: {srt_exists}")
    print(f"Duração Total dos Áudios: {total_sec:6.2f}s ({total_sec/60:4.2f} min)")

    # 2. Imagens
    images = sorted(glob.glob("imagens/*.png"))
    print(f"\nTotal de imagens: {len(images)}")
    for img in images:
        size_kb = os.path.getsize(img) / 1024
        print(f"  {os.path.basename(img):<15} -> {size_kb:6.1f} KB")

    # 3. Vídeos existentes
    videos = sorted(glob.glob("*.mp4") + glob.glob("historias chinesas 2/*.mp4"))
    print(f"\nVídeos existentes: {len(videos)}")
    for v in videos:
        info = get_video_info(v)
        print(f"  {v}: {info}")

    # 4. Extrair prompts do docx para prompts/prompts_cenas.md
    bloqueios_text = read_docx_text("Bloqueios retirados.docx")
    os.makedirs("prompts", exist_ok=True)
    with open("prompts/prompts_cenas.md", "w", encoding="utf-8") as f:
        f.write("# Prompts e Planejamento das Cenas - Ep. 2 Wu Zetian\n\n")
        f.write(bloqueios_text)
    print("\nArquivo 'prompts/prompts_cenas.md' gerado com sucesso.")

if __name__ == "__main__":
    main()
