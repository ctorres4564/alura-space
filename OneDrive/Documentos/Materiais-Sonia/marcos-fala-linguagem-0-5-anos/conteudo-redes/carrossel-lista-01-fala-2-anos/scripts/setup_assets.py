import shutil
from pathlib import Path

# Paths
workspace_dir = Path(__file__).resolve().parent.parent
assets_dir = workspace_dir / "assets"
assets_dir.mkdir(parents=True, exist_ok=True)

brain_dir = Path(r"C:\Users\Gamer\.gemini\antigravity-ide\brain\bbc9797c-a6e2-4065-b7f6-aa5d4f7af0b0")

image_map = {
    "slide-01.jpg": "slide_01_capa_1791059550736.jpg",
    "slide-02.jpg": "slide_02_palavras_1791059570314.jpg",
    "slide-03.jpg": "slide_03_vocabulario_1791059594830.jpg",
    "slide-04.jpg": "slide_04_corpo_1791059620688.jpg",
    "slide-05.jpg": "slide_05_gestos_1791059651348.jpg",
    "slide-06.jpg": "slide_06_espelho_1791059694297.jpg",
    "slide-07.jpg": "slide_07_livro_1791059731324.jpg",
    "slide-10.jpg": "slide_10_fechamento_1791059773971.jpg",
}

for dest_name, src_name in image_map.items():
    src_path = brain_dir / src_name
    dest_path = assets_dir / dest_name
    if src_path.exists():
        shutil.copy2(src_path, dest_path)
        print(f"Copiado: {src_name} -> {dest_path}")
    else:
        print(f"ERRO: Origem não encontrada: {src_path}")

print("Concluída organização de assets!")
