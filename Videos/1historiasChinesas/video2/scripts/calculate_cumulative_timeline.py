import json

def main():
    with open("src/timeline_manifest.json", "r", encoding="utf-8") as f:
        m = json.load(f)

    cum_time = 0.0
    timeline = []

    for b in m["blocks"]:
        dur = b["duration"]
        if b["id"] == "gancho_abertura":
            dur += 6.0 # vinheta de 6s
        
        block_start = cum_time
        print(f"{b['id']:<18} | dur: {dur:6.2f}s | inicio: {cum_time:6.2f}s ({int(cum_time//60):02d}:{cum_time%60:05.2f})")
        
        for sc in b["scenes"]:
            if sc.get("card"):
                sc_card = sc["card"]
                card_global_start = round(block_start + sc_card["show_at"], 2)
                card_global_end = round(card_global_start + sc_card["card_duration"], 2)
                timeline.append({
                    "scene_id": sc["id"],
                    "asset_path": sc_card.get("asset_path", f"assets/title_cards/{sc['id']}.png"),
                    "start": card_global_start,
                    "end": card_global_end,
                    "line1": sc_card["line1"],
                    "line2": sc_card["line2"]
                })
        cum_time += dur

    print(f"\nTempo Total Acumulado: {cum_time:6.2f}s ({int(cum_time//60):02d}:{cum_time%60:05.2f})")
    
    with open("src/cards_global_timeline.json", "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)
    print(f"Salvo src/cards_global_timeline.json com {len(timeline)} cartões mapeados.")

if __name__ == "__main__":
    main()
