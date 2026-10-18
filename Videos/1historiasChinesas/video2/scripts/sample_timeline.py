import subprocess
import os

def extract_timeline(video_path, timestamps, prefix):
    os.makedirs("docs/frames", exist_ok=True)
    for ts in timestamps:
        out_name = f"docs/frames/{prefix}_{ts.replace(':', '_')}.jpg"
        cmd = ["ffmpeg", "-ss", ts, "-i", video_path, "-vframes", "1", "-q:v", "2", "-y", out_name]
        subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(f"Extraído {out_name}")

def main():
    timestamps_full = ["00:00:03", "00:00:25", "00:01:00", "00:02:30", "00:05:00", "00:10:00", "00:15:00", "00:20:00", "00:21:30"]
    extract_timeline("historias chinesas 2/historias chinesas 2.mp4", timestamps_full, "full")

    timestamps_p1 = ["00:00:03", "00:00:20", "00:01:00", "00:03:00", "00:05:00"]
    extract_timeline("Ep2_WuZetian_720p_parte1de4.mp4", timestamps_p1, "p1")

if __name__ == "__main__":
    main()
