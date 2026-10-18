import subprocess
import json

def detect_scene_changes(video_path):
    print("Detectando mudanças de cena em:", video_path)
    cmd = [
        "ffmpeg", "-i", video_path,
        "-filter_complex", "select='gt(scene,0.15)',metadata=print:file=scene_cuts.txt",
        "-f", "null", "-"
    ]
    subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    
    # Processa scene_cuts.txt
    cuts = [0.0]
    if os.path.exists("scene_cuts.txt"):
        with open("scene_cuts.txt", "r") as f:
            for line in f:
                if "pts_time:" in line:
                    val = float(line.split("pts_time:")[1].strip())
                    if not cuts or val - cuts[-1] > 2.0: # evita microcortes repetidos
                        cuts.append(val)
        os.remove("scene_cuts.txt")
    print(f"Total de cortes detectados: {len(cuts)}")
    for i, c in enumerate(cuts):
        print(f"  Cena {i+1:02d}: {c:6.2f}s ({c//60:02.0f}:{c%60:05.2f})")
    return cuts

if __name__ == "__main__":
    import os
    cuts = detect_scene_changes("historias chinesas 2/historias chinesas 2.mp4")
    with open("src/detected_scene_cuts.json", "w") as f:
        json.dump(cuts, f, indent=2)
