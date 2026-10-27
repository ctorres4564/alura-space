import subprocess
import wave
import numpy as np
import json
from faster_whisper import WhisperModel

def get_audio_array(wav_path):
    # Converte para 16kHz mono pcm_s16le via ffmpeg
    temp_16k = "temp_16k.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", wav_path,
        "-ar", "16000", "-ac", "1",
        "-c:a", "pcm_s16le", temp_16k
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with wave.open(temp_16k, "rb") as wf:
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
        audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        
    return audio

def transcribe():
    print("Convertendo e preparando áudio 16kHz...")
    audio = get_audio_array("01.wav")
    print(f"Áudio carregado: {len(audio)} amostras ({len(audio)/16000:.2f}s)")
    
    print("Carregando modelo faster-whisper...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    print("Transcrevendo áudio...")
    segments, info = model.transcribe(audio, beam_size=5, language="pt", word_timestamps=True)
    
    print(f"Idioma detectado: {info.language} com probabilidade {info.language_probability:.2f}")
    
    results = []
    full_text = []
    
    for segment in segments:
        words = []
        if segment.words:
            for w in segment.words:
                words.append({
                    "start": round(w.start, 2),
                    "end": round(w.end, 2),
                    "word": w.word.strip()
                })
        seg_data = {
            "id": segment.id,
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip(),
            "words": words
        }
        results.append(seg_data)
        full_text.append(segment.text.strip())
        print(f"[{seg_data['start']}s -> {seg_data['end']}s] {seg_data['text']}")
        
    with open("transcription.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))
        
    print("Transcrição concluída com sucesso e salva em transcription.json e transcription.txt.")

if __name__ == "__main__":
    transcribe()
