import subprocess
import os

scenes_info = [
    ("assets/scenes/scene_01.jpg", 17.20, "zoom_in"),
    ("assets/scenes/scene_02.jpg", 22.30, "static"),
    ("assets/scenes/scene_03.jpg", 10.50, "static"),
    ("assets/scenes/scene_04.jpg", 28.90, "zoom_in"),
    ("assets/scenes/scene_05.jpg", 5.60,  "pan"),
    ("assets/scenes/scene_06.jpg", 10.80, "zoom_in"),
    ("assets/scenes/scene_07.jpg", 22.40, "static"),
    ("assets/scenes/scene_08.jpg", 16.40, "static"),
    ("assets/scenes/scene_09.jpg", 13.10, "static"),
    ("assets/scenes/scene_10.jpg", 6.60,  "zoom_in")
]

def render_scenes():
    os.makedirs("temp_clips", exist_ok=True)
    clip_files = []
    
    for idx, (img_path, dur, motion) in enumerate(scenes_info, start=1):
        out_clip = f"temp_clips/clip_{idx:02d}.mp4"
        frames = int(round(dur * 30))
        
        if motion == "zoom_in":
            vf = (
                f"zoompan=z='min(zoom+0.0003,1.06)':d={frames}:"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
                f"format=yuv420p"
            )
        elif motion == "pan":
            vf = (
                f"zoompan=z=1.05:d={frames}:"
                f"x='(iw-iw/zoom)*(on/{frames})':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
                f"format=yuv420p"
            )
        else:
            vf = "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p"
            
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", img_path,
            "-vf", vf,
            "-t", f"{dur:.2f}",
            "-r", "30",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            out_clip
        ]
        
        print(f"Renderizando Cena {idx:02d} ({dur:.2f}s)...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clip_files.append(out_clip)
        
    with open("temp_clips/concat_list.txt", "w", encoding="utf-8") as f:
        for clip in clip_files:
            f.write(f"file '{os.path.basename(clip)}'\n")
            
    print("Todas as cenas individuais foram renderizadas com sucesso!")

def render_final_video():
    print("Concatenando cenas, unindo áudio masterizado e aplicando legendas ASS posicionadas...")
    
    temp_concat_video = "temp_clips/concatenated.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "temp_clips/concat_list.txt",
        "-c", "copy",
        temp_concat_video
    ]
    subprocess.run(cmd_concat, check=True)
    
    out_final = "VIDEO_LIBERDADE_MULHERES_FINAL/video_liberdade_mulheres.mp4"
    os.makedirs(os.path.dirname(out_final), exist_ok=True)
    
    # Filtro ASS: lê diretamente legendas.ass que possui PlayResX=1080, PlayResY=1920, Fontsize=42 e MarginV=340
    sub_filter = "ass=legendas.ass"
    
    cmd_final = [
        "ffmpeg", "-y",
        "-i", temp_concat_video,
        "-i", "assets/audio/audio_master.wav",
        "-vf", sub_filter,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-shortest",
        out_final
    ]
    print("Iniciando renderização final com nova escala e posicionamento de legendas...")
    subprocess.run(cmd_final, check=True)
    print(f"Vídeo final re-renderizado com sucesso em: {out_final}")

if __name__ == "__main__":
    render_scenes()
    render_final_video()
