import numpy as np
import wave
import subprocess
import os

def synthesize_cinematic_soundtrack(duration_sec=154.0, sample_rate=48000):
    print("Sintetizando trilha sonora cinematográfica original...")
    total_samples = int(duration_sec * sample_rate)
    time = np.linspace(0, duration_sec, total_samples, endpoint=False)
    
    # Canais estéreo
    left = np.zeros(total_samples, dtype=np.float32)
    right = np.zeros(total_samples, dtype=np.float32)
    
    # 1. Sub-Bass Drone / Atmospheric Pad (Tonalidade: Ré menor / D minor - 73.4 Hz, 110 Hz, 146.8 Hz, 174.6 Hz)
    # Variação dinâmica pelas 10 cenas:
    # Abertura (0-17s): 73.4Hz + 110Hz (Dm) misterioso
    # Tensão crescente (17-50s): entrada de 87.3Hz (F) e 130.8Hz (C)
    # Pulso rítmico (50-84s): contradição política, batimento grave a cada 1.2s
    # Violência política (84-118s): atmosfera sombria, acordes densos
    # Reflexão e Encerramento (118-154s): fade progressivo, piano isolado
    
    drone = 0.15 * np.sin(2 * np.pi * 73.416 * time) + \
            0.10 * np.sin(2 * np.pi * 110.00 * time) + \
            0.08 * np.sin(2 * np.pi * 146.83 * time) + \
            0.05 * np.sin(2 * np.pi * 174.61 * time)
            
    # Modulação lenta LFO para sensação orgânica de respiração sonora
    lfo = 0.7 + 0.3 * np.sin(2 * np.pi * 0.08 * time)
    drone *= lfo
    
    # 2. Pulsação Rítmica Cinematográfica (Heartbeat / Sub-Pulse)
    # Ativa especialmente a partir de 15s até 145s
    pulse_bpm = 64.0  # batimentos por minuto
    beat_interval = 60.0 / pulse_bpm
    pulse = np.zeros(total_samples, dtype=np.float32)
    
    for t_beat in np.arange(15.0, 145.0, beat_interval):
        idx_start = int(t_beat * sample_rate)
        # Batida dupla (ta-tum)
        for offset, amp in [(0.0, 0.25), (0.22, 0.18)]:
            b_start = idx_start + int(offset * sample_rate)
            pulse_dur = int(0.25 * sample_rate)
            if b_start + pulse_dur < total_samples:
                t_p = np.linspace(0, 0.25, pulse_dur, endpoint=False)
                # Tombo de frequência 55Hz descendo para 35Hz
                freq = 55.0 - 20.0 * (t_p / 0.25)
                env = np.exp(-t_p * 14.0)
                pulse[b_start:b_start+pulse_dur] += amp * np.sin(2 * np.pi * freq * t_p) * env

    # 3. Piano Minimalista (Notas sutis espaçadas em Dm: D4, F4, A4, G4, E4, C4)
    # Frequências: D4=293.66, F4=349.23, A4=440.0, G4=392.0, E4=329.63, C4=261.63
    piano = np.zeros(total_samples, dtype=np.float32)
    notes = [
        (2.0, 293.66), (6.5, 349.23), (11.0, 440.0), (14.5, 392.0),
        (19.0, 293.66), (24.0, 329.63), (29.0, 349.23), (34.0, 261.63),
        (41.0, 293.66), (46.0, 349.23), (53.0, 392.0), (58.0, 440.0),
        (64.0, 349.23), (71.0, 293.66), (77.0, 329.63), (82.0, 293.66),
        (87.0, 349.23), (92.0, 392.0), (99.0, 440.0), (105.0, 349.23),
        (111.0, 329.63), (116.0, 293.66), (121.0, 261.63), (127.0, 293.66),
        (133.0, 349.23), (139.0, 392.0), (144.0, 440.0), (148.5, 293.66)
    ]
    
    for note_time, freq in notes:
        n_start = int(note_time * sample_rate)
        n_dur = int(3.5 * sample_rate)
        if n_start + n_dur <= total_samples:
            t_n = np.linspace(0, 3.5, n_dur, endpoint=False)
            # Harmônicos do piano com decaimento exponencial
            p_note = (1.0 * np.sin(2 * np.pi * freq * t_n) +
                      0.5 * np.sin(2 * np.pi * 2 * freq * t_n) +
                      0.2 * np.sin(2 * np.pi * 3 * freq * t_n) +
                      0.08 * np.sin(2 * np.pi * 4 * freq * t_n)) * np.exp(-t_n * 1.5)
            piano[n_start:n_start+n_dur] += 0.22 * p_note

    # Envelopamento da trilha geral (Fade-in 2s, Fade-out 4s no final)
    master_env = np.ones(total_samples, dtype=np.float32)
    fade_in_samples = int(2.0 * sample_rate)
    fade_out_samples = int(4.0 * sample_rate)
    master_env[:fade_in_samples] = np.linspace(0, 1, fade_in_samples)
    master_env[-fade_out_samples:] = np.linspace(1, 0, fade_out_samples)
    
    # Composição estéreo com espacialização sutil
    left = (drone * 0.7 + pulse * 0.8 + piano * 0.85) * master_env
    right = (drone * 0.75 + pulse * 0.8 + piano * 0.75) * master_env
    
    # Normalização segura da música instrumental isolada
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
    left = (left / max_val) * 0.35  # Nível de fundo cinematográfico
    right = (right / max_val) * 0.35
    
    stereo = np.vstack([left, right]).T
    stereo_int16 = (stereo * 32767).astype(np.int16)
    
    music_wav = "assets/audio/trilha_cinematografica.wav"
    os.makedirs(os.path.dirname(music_wav), exist_ok=True)
    
    with wave.open(music_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(stereo_int16.tobytes())
        
    print(f"Trilha salva em: {music_wav}")
    return music_wav

def mix_soundtrack_with_narration(narration_wav="01.wav", music_wav="assets/audio/trilha_cinematografica.wav", output_wav="assets/audio/audio_master.wav"):
    print("Mixando narração original com trilha sonora e aplicando ducking automático...")
    # Usando FFmpeg para mixar narração original preservada com trilha sonora
    # Narração preservada integralmente, trilha com sidechain/volume de fundo
    cmd = [
        "ffmpeg", "-y",
        "-i", narration_wav,
        "-i", music_wav,
        "-filter_complex",
        "[1:a]volume=0.35[bg];"
        "[0:a]volume=1.2,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[vox];"
        "[bg][vox]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=400[ducked_bg];"
        "[ducked_bg][vox]amix=inputs=2:duration=first:dropout_transition=2,alimiter=limit=-1.0dB[out]",
        "-map", "[out]",
        "-c:a", "pcm_s16le",
        "-ar", "48000",
        output_wav
    ]
    subprocess.run(cmd, check=True)
    print(f"Áudio final masterizado gerado em: {output_wav}")

if __name__ == "__main__":
    music_file = synthesize_cinematic_soundtrack()
    mix_soundtrack_with_narration()
