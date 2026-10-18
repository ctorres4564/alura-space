import subprocess
import glob
import os

def check_video_details(video_path):
    print(f"=== DETALHES DE: {video_path} ===")
    cmd = [
        "ffmpeg", "-i", video_path
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="ignore")
    lines = [l.strip() for l in res.stderr.splitlines() if any(k in l for k in ["Duration", "Stream #", "Video:", "Audio:"])]
    for l in lines:
        print(" ", l)

def extract_sample_frame(video_path, out_name):
    os.makedirs("docs/frames", exist_ok=True)
    out_path = os.path.join("docs/frames", out_name)
    cmd = [
        "ffmpeg", "-ss", "00:00:10", "-i", video_path, "-vframes", "1", "-q:v", "2", "-y", out_path
    ]
    subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if os.path.exists(out_path):
        print(f" Frame extraído para {out_path}")

def main():
    videos = [
        "historias chinesas 2/historias chinesas 2.mp4",
        "Ep2_WuZetian_720p_parte1de4.mp4",
        "Ep2_WuZetian_720p_parte2de4.mp4",
        "Ep2_WuZetian_720p_parte3de4.mp4",
        "Ep2_WuZetian_720p_parte4de4.mp4",
    ]
    for v in videos:
        if os.path.exists(v):
            check_video_details(v)
            clean_name = os.path.basename(v).replace(".mp4", ".jpg")
            extract_sample_frame(v, clean_name)

if __name__ == "__main__":
    main()
