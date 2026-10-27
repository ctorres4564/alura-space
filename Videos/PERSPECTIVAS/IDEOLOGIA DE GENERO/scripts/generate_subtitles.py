import json
import math

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def split_text_into_lines(text, max_chars=32):
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
        # Reagrupa em 2 linhas se passar
        mid = len(lines) // 2
        line1 = " ".join(lines[:mid])
        line2 = " ".join(lines[mid:])
        return f"{line1}\n{line2}"
    return "\n".join(lines)

def generate_srt():
    with open("transcription.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    srt_entries = []
    
    # Criamos blocos curtos e perfeitamente legíveis para Reels/Shorts
    entry_id = 1
    for seg in data:
        # Se o segmento for longo (> 3.5s ou > 60 caracteres), quebramos por palavras se existirem
        words = seg.get("words", [])
        if len(words) >= 6 and (seg["end"] - seg["start"]) > 3.0:
            # Dividir em 2 ou mais sub-blocos
            chunk_size = 5 if len(words) >= 10 else 4
            for i in range(0, len(words), chunk_size):
                chunk = words[i:i+chunk_size]
                chunk_start = chunk[0]["start"]
                chunk_end = chunk[-1]["end"]
                chunk_text = " ".join(w["word"] for w in chunk)
                formatted_text = split_text_into_lines(chunk_text, max_chars=28)
                
                srt_entries.append(
                    f"{entry_id}\n"
                    f"{format_timestamp(chunk_start)} --> {format_timestamp(chunk_end)}\n"
                    f"{formatted_text}\n"
                )
                entry_id += 1
        else:
            formatted_text = split_text_into_lines(seg["text"], max_chars=30)
            srt_entries.append(
                f"{entry_id}\n"
                f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n"
                f"{formatted_text}\n"
            )
            entry_id += 1
            
    srt_content = "\n".join(srt_entries)
    
    with open("legendas.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
        
    with open("VIDEO_LIBERDADE_MULHERES_FINAL/legendas.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
        
    print(f"Legendas geradas com sucesso! {entry_id - 1} blocos de legendas criados.")

if __name__ == "__main__":
    generate_srt()
