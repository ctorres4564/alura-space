import shutil
import glob
import os

def copy_images():
    brain_dir = r"C:\Users\Gamer\.gemini\antigravity-ide\brain\6633e93f-0474-43b6-849f-692f26ee4830"
    target_dir = "assets/images"
    os.makedirs(target_dir, exist_ok=True)
    
    mapping = {
        "retrato_mulher_capa*": "retrato_mulher.jpg",
        "plenario_discurso*": "plenario_discurso.jpg",
        "voto_mulheres_eleicao*": "voto_eleicao.jpg",
        "saude_publica_hospital*": "saude_publica.jpg",
        "mobilizacao_civica*": "mobilizacao_civica.jpg"
    }
    
    for pattern, dest_name in mapping.items():
        matches = glob.glob(os.path.join(brain_dir, pattern))
        if matches:
            latest = max(matches, key=os.path.getmtime)
            dest_path = os.path.join(target_dir, dest_name)
            shutil.copy2(latest, dest_path)
            print(f"Copiado: {latest} -> {dest_path}")
        else:
            print(f"Aviso: nenhum arquivo encontrado para {pattern}")

if __name__ == "__main__":
    copy_images()
