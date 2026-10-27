import json
import os

def format_timestamp_srt(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_timestamp_ass(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis >= 100:
        centis = 99
    return f"{hours:d}:{minutes:02d}:{secs:02d}.{centis:02d}"

def split_text_into_lines(text, max_chars=28):
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    
    for word in words:
        if current_len + len(word) + (1 if current_line else 0) <= max_chars:
            current_line.append(word)
            current_len += len(word) + (1 if len(current_line) > 1 else 0)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_len = len(word)
            
    if current_line:
        lines.append(" ".join(current_line))
        
    if len(lines) > 2:
        mid = len(lines) // 2
        line1 = " ".join(lines[:mid])
        line2 = " ".join(lines[mid:])
        return f"{line1}\n{line2}"
    return "\n".join(lines)

def generate_subtitles():
    with open("transcription.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    srt_entries = []
    ass_events = []
    
    # Cabeçalho ASS com resolução explícita 1080x1920
    # Alignment=2 (Bottom Center), MarginV=360 (Safe area inferior, abaixo do card central e acima de botões)
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,42,&H00FFFFFF,&H000000FF,&H000A0A0A,&H80000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,60,60,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    entry_id = 1
    for seg in data:
        words = seg.get("words", [])
        if len(words) >= 6 and (seg["end"] - seg["start"]) > 2.8:
            chunk_size = 5 if len(words) >= 10 else 4
            for i in range(0, len(words), chunk_size):
                chunk = words[i:i+chunk_size]
                chunk_start = chunk[0]["start"]
                chunk_end = chunk[-1]["end"]
                chunk_text = " ".join(w["word"] for w in chunk)
                formatted_text = split_text_into_lines(chunk_text, max_chars=28)
                
                # SRT
                srt_entries.append(
                    f"{entry_id}\n"
                    f"{format_timestamp_srt(chunk_start)} --> {format_timestamp_srt(chunk_end)}\n"
                    f"{formatted_text}\n"
                )
                
                # ASS
                ass_text = formatted_text.replace("\n", r"\N")
                ass_events.append(
                    f"Dialogue: 0,{format_timestamp_ass(chunk_start)},{format_timestamp_ass(chunk_end)},Default,,0,0,0,,{ass_text}"
                )
                entry_id += 1
        else:
            formatted_text = split_text_into_lines(seg["text"], max_chars=28)
            srt_entries.append(
                f"{entry_id}\n"
                f"{format_timestamp_srt(seg['start'])} --> {format_timestamp_srt(seg['end'])}\n"
                f"{formatted_text}\n"
            )
            ass_text = formatted_text.replace("\n", r"\N")
            ass_events.append(
                f"Dialogue: 0,{format_timestamp_ass(seg['start'])},{format_timestamp_ass(seg['end'])},Default,,0,0,0,,{ass_text}"
            )
            entry_id += 1
            
    # Salvar SRT
    srt_content = "\n".join(srt_entries)
    with open("legendas.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
    with open("VIDEO_LIBERDADE_MULHERES_FINAL/legendas.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
        
    # Salvar ASS
    ass_content = ass_header + "\n".join(ass_events)
    with open("legendas.ass", "w", encoding="utf-8") as f:
        f.write(ass_content)
    with open("VIDEO_LIBERDADE_MULHERES_FINAL/legendas.ass", "w", encoding="utf-8") as f:
        f.write(ass_content)
        
    print(f"Legendas geradas com sucesso em SRT e ASS (1080x1920)! {entry_id - 1} blocos criados.")

if __name__ == "__main__":
    generate_subtitles()
