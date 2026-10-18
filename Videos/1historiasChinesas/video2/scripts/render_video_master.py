import os
import sys
import json
import subprocess

def render_block_chunk(block_index, block_data, block_start, input_video, output_chunk):
    dur = block_data["duration"]
    if block_data["id"] == "gancho_abertura":
        dur += 6.0 # vinheta

    scenes = block_data["scenes"]
    cards_in_block = [s for s in scenes if s.get("card")]

    # Monta a cadeia de filtros FFmpeg para os cartões deste bloco
    # Os inputs começam com o clipe de vídeo base (input 0)
    # Inputs seguintes (1..N) são os arquivos PNG dos cartões
    ffmpeg_inputs = [
        "-ss", str(block_start),
        "-t", str(dur),
        "-i", input_video
    ]

    filter_chains = []
    last_v = "[0:v]"

    for i, sc in enumerate(cards_in_block):
        card = sc["card"]
        card_png = card.get("asset_path", f"assets/title_cards/{sc['id']}.png")
        if not os.path.exists(card_png):
            continue

        in_idx = i + 1
        ffmpeg_inputs.extend(["-loop", "1", "-t", str(dur), "-i", card_png])

        st_in = card["show_at"]
        st_out = st_in + card["card_duration"] - 0.5
        end_time = st_in + card["card_duration"]

        card_label = f"[card_{i}]"
        next_v = f"[v_{i}]"

        # Fade in e fade out no canal alfa
        filter_chains.append(
            f"[{in_idx}:v]format=rgba,fade=t=in:st={st_in}:d=0.5:alpha=1,fade=t=out:st={st_out}:d=0.5:alpha=1{card_label};"
            f"{last_v}{card_label}overlay=0:0:enable='between(t,{st_in},{end_time})'{next_v}"
        )
        last_v = next_v

    full_filter = ";".join(filter_chains) if filter_chains else ""

    cmd = ["ffmpeg"] + ffmpeg_inputs
    if full_filter:
        cmd.extend(["-filter_complex", full_filter, "-map", last_v, "-map", "0:a"])
    else:
        cmd.extend(["-map", "0:v", "-map", "0:a"])

    cmd.extend([
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-y", output_chunk
    ])

    print(f"\n[BLOCO {block_index:02d} / {block_data['id']}] Início: {block_start:6.2f}s | Duração: {dur:6.2f}s")
    subprocess.run(cmd, check=True)
    print(f"-> Chunk gerado: {output_chunk}")

def main():
    print("=== INICIANDO RENDERIZAÇÃO DO VÍDEO MASTER EM FULL HD 1080P ===")
    
    with open("src/timeline_manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)

    os.makedirs("build/chunks", exist_ok=True)
    input_master_source = "historias chinesas 2/historias chinesas 2.mp4"
    chunks = []

    cum_time = 0.0
    for idx, block in enumerate(manifest["blocks"]):
        chunk_file = f"build/chunks/chunk_{idx:02d}_{block['id']}.mp4"
        chunks.append(chunk_file)

        # Se já existe e é válido, pode pular
        if os.path.exists(chunk_file) and os.path.getsize(chunk_file) > 100000:
            print(f"Bloco {idx:02d} ({block['id']}) já renderizado. Pulando...")
        else:
            render_block_chunk(idx, block, cum_time, input_master_source, chunk_file)

        block_dur = block["duration"]
        if block["id"] == "gancho_abertura":
            block_dur += 6.0
        cum_time += block_dur

    # Concatenação final lossless
    print("\n=== CONCATENANDO TODOS OS CHUNKS NO MASTER FINAL ===")
    concat_list_file = "build/concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for c in chunks:
            abs_c = os.path.abspath(c).replace("\\", "/")
            f.write(f"file '{abs_c}'\n")

    final_output = "Ep2_WuZetian_1080p_Master_Completo.mp4"
    concat_cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        "-y", final_output
    ]
    subprocess.run(concat_cmd, check=True)
    print(f"\n[SUCESSO] Vídeo Master Final gerado com perfeição:")
    print(f"-> Arquivo: {final_output}")
    print(f"-> Tamanho: {os.path.getsize(final_output) / (1024*1024):.2f} MB")

    # Extrai frames de conferência
    os.makedirs("docs/final_frames", exist_ok=True)
    test_points = ["00:00:20", "00:01:25", "00:04:30", "00:09:45", "00:13:55", "00:19:35", "00:21:35"]
    for tp in test_points:
        out_f = f"docs/final_frames/master_{tp.replace(':', '_')}.jpg"
        subprocess.run(["ffmpeg", "-ss", tp, "-i", final_output, "-vframes", "1", "-y", out_f], capture_output=True)
    print("Frames finais de conferência extraídos em docs/final_frames/")

if __name__ == "__main__":
    main()
