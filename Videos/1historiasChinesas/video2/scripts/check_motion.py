import subprocess

def analyze_motion_and_audio():
    # Extrai 2 frames com 3 segundos de diferença para testar se há zoom/movimento (Ken Burns)
    t1 = "00:01:05"
    t2 = "00:01:08"
    cmd1 = ["ffmpeg", "-ss", t1, "-i", "historias chinesas 2/historias chinesas 2.mp4", "-vframes", "1", "-y", "docs/frames/motion_t1.jpg"]
    cmd2 = ["ffmpeg", "-ss", t2, "-i", "historias chinesas 2/historias chinesas 2.mp4", "-vframes", "1", "-y", "docs/frames/motion_t2.jpg"]
    subprocess.run(cmd1, capture_output=True)
    subprocess.run(cmd2, capture_output=True)
    
    # Compara os 2 frames
    import filecmp
    # ou usando opencv ou checando tamanho
    from PIL import Image
    import numpy as np
    
    im1 = np.array(Image.open("docs/frames/motion_t1.jpg"))
    im2 = np.array(Image.open("docs/frames/motion_t2.jpg"))
    diff = np.mean(np.abs(im1.astype(float) - im2.astype(float)))
    print(f"Diferença média entre t1 ({t1}) e t2 ({t2}): {diff:.2f}")
    if diff > 1.0:
        print(">> HÁ MOVIMENTO DE CÂMERA / ANIMAÇÃO / ZOOM ENTRE FRAMES!")
    else:
        print(">> IMAGEM ESTÁTICA.")

if __name__ == "__main__":
    analyze_motion_and_audio()
