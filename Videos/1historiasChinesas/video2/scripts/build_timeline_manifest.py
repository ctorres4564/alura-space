import json
import os
import wave

def get_wav_duration(path):
    with wave.open(path, 'rb') as w:
        frames = w.getnframes()
        rate = w.getframerate()
        return round(frames / float(rate), 3)

def build_manifest():
    manifest = {
        "project": "Wu Zetian - A Mulher que Conquistou o Trono da China",
        "resolution": {"width": 1920, "height": 1080},
        "fps": 30,
        "blocks": []
    }

    # Bloco 0: Gancho + Vinheta + Abertura
    dur_abertura = get_wav_duration("audios/gancho e abertura.wav") # ~71.28s
    manifest["blocks"].append({
        "id": "gancho_abertura",
        "audio": "audios/gancho e abertura.wav",
        "srt": "audios/gancho e abertura.srt",
        "duration": dur_abertura,
        "scenes": [
            {
                "id": "G1",
                "image": "imagens/g1.png",
                "start": 0.0,
                "duration": 5.5,
                "card": {"line1": "690 d.C. · QIANLING", "line2": "A ESTELA EM BRANCO", "show_at": 0.5, "card_duration": 4.5}
            },
            {
                "id": "INTRO_LOGO",
                "video_clip": "vinheta",
                "start": 5.5,
                "duration": 6.0,
                "card": None
            },
            {
                "id": "A1",
                "image": "imagens/a1.png",
                "start": 11.5,
                "duration": 30.0,
                "card": {"line1": "690 d.C. · LUOYANG", "line2": "A PRIMEIRA IMPERATRIZ", "show_at": 12.0, "card_duration": 6.0}
            },
            {
                "id": "A2",
                "image": "imagens/a2.png",
                "start": 41.5,
                "duration": round(dur_abertura + 6.0 - 41.5, 3), # compensa os 6s da vinheta
                "card": {"line1": "QIANLING · MAUSOLÉU IMPERIAL", "line2": "O MONUMENTO SILENCIOSO", "show_at": 42.5, "card_duration": 6.0}
            }
        ]
    })

    # Dados dos 12 blocos com imagens e cartões
    blocks_meta = [
        {
            "id": "bloco_01",
            "audio": "audios/bloco 1.wav",
            "srt": "audios/bloco 1.srt",
            "scenes": [
                {"id": "B1-1", "image": "imagens/b1-1.png", "card": {"line1": "624 d.C. · WENSHUI, SHANXI", "line2": "UMA JOVEM NO PALÁCIO"}},
                {"id": "B1-2", "image": "imagens/b1-2.png", "card": {"line1": "638 d.C. · CHANG'AN", "line2": "A DAMA DE TALENTO"}},
                {"id": "B1-3", "image": "imagens/b1-3.png", "card": {"line1": "649 d.C. · MORTE DE TAIZONG", "line2": "FIM DA PRIMEIRA ERA"}}
            ]
        },
        {
            "id": "bloco_02",
            "audio": "audios/bloco 2.wav",
            "srt": "audios/bloco 2.srt",
            "scenes": [
                {"id": "B2-1", "image": "imagens/b2-1.png", "card": {"line1": "649 d.C. · CONVENTO GAN'YE", "line2": "O CONVENTO E O RETORNO"}},
                {"id": "B2-2", "image": "imagens/b2-2.png", "card": {"line1": "650 d.C. · CORTE DE GAOZONG", "line2": "A ALIANÇA COM A IMPERATRIZ WANG"}},
                {"id": "B2-3", "image": "imagens/b2-3.png", "card": {"line1": "654 d.C. · PALÁCIO IMPERIAL", "line2": "O NASCIMENTO DA PRINCESA"}}
            ]
        },
        {
            "id": "bloco_03",
            "audio": "audios/bloco 3.wav",
            "srt": "audios/bloco 3.srt",
            "scenes": [
                {"id": "B3-1", "image": "imagens/b3-1.png", "card": {"line1": "654 d.C. · O BERÇO SILENCIOSO", "line2": "A TRAGÉDIA E A ACUSAÇÃO"}},
                {"id": "B3-2", "image": "imagens/b3-2.png", "card": {"line1": "CRÔNICAS DINÁSTICAS", "line2": "A DISPUTA HISTORIOGRÁFICA"}},
                {"id": "B3-3", "image": "imagens/b3-3.png", "card": {"line1": "655 d.C. · A CORTE FRAGMENTADA", "line2": "RESISTÊNCIA DA ARISTOCRACIA"}},
                {"id": "B3-4", "image": "imagens/b3-4.png", "card": {"line1": "655 d.C. · A COROAÇÃO", "line2": "WU É PROCLAMADA IMPERATRIZ"}}
            ]
        },
        {
            "id": "bloco_04",
            "audio": "audios/bloco 4.wav",
            "srt": "audios/bloco 4.srt",
            "scenes": [
                {"id": "B4-1", "image": "imagens/b4-1.png", "card": {"line1": "660 d.C. · ER SHENG", "line2": "OS DOIS SÁBIOS NO PODER"}},
                {"id": "B4-2", "image": "imagens/b4-2.png", "card": {"line1": "666 d.C. · MONTE TAI", "line2": "O RITUAL FENGSHAN"}},
                {"id": "B4-3", "image": "imagens/b4-3.png", "card": {"line1": "674 d.C. · TIANHOU", "line2": "A IMPERATRIZ CELESTIAL"}},
                {"id": "B4-4", "image": "imagens/b4-4.png", "card": {"line1": "INTERIOR DA CHINA", "line2": "REFORMAS SOCIAIS E AGRÍCOLAS"}}
            ]
        },
        {
            "id": "bloco_05",
            "audio": "audios/bloco 5.wav",
            "srt": "audios/bloco 5.srt",
            "scenes": [
                {"id": "B5-1", "image": "imagens/b5-1.png", "card": {"line1": "683 d.C. · MORTE DE GAOZONG", "line2": "A SUCESSÃO AMEAÇADA"}},
                {"id": "B5-2", "image": "imagens/b5-2.png", "card": {"line1": "684 d.C. · A REGÊNCIA", "line2": "O PODER ATRÁS DA CORTINA"}},
                {"id": "B5-3", "image": "imagens/b5-3.png", "card": {"line1": "684 d.C. · YANGZHOU", "line2": "A REBELIÃO CONTRA A REGENTE"}}
            ]
        },
        {
            "id": "bloco_06",
            "audio": "audios/bloco 6.wav",
            "srt": "audios/bloco 6.srt",
            "scenes": [
                {"id": "B6-1", "image": "imagens/b6-1.png", "card": {"line1": "686 d.C. · LUOYANG", "line2": "AS QUATRO URNAS DE BRONZE"}},
                {"id": "B6-2", "image": "imagens/b6-2.png", "card": {"line1": "A REDE DE INFORMANTES", "line2": "DENÚNCIAS E VIGILÂNCIA"}},
                {"id": "B6-3", "image": "imagens/b6-3.png", "card": {"line1": "OS JUÍZES IMPERIAIS", "line2": "O FIM DA VELHA NOBREZA"}},
                {"id": "B6-4", "image": "imagens/b6-4.png", "card": {"line1": "LUOYANG AO CREPÚSCULO", "line2": "A CENTRALIZAÇÃO DO ESTADO"}}
            ]
        },
        {
            "id": "bloco_07",
            "audio": "audios/bloco 7.wav",
            "srt": "audios/bloco 7.srt",
            "scenes": [
                {"id": "B7-1", "image": "imagens/B7-1.png", "card": {"line1": "688 d.C. · MINGTANG", "line2": "O SALÃO CÓSMICO DE LUOYANG"}},
                {"id": "B7-2", "image": "imagens/B7-2.png", "card": {"line1": "RIO LUO", "line2": "O PRESSÁGIO DA PEDRA SAGRADA"}},
                {"id": "B7-3", "image": "imagens/B7-3.png", "card": {"line1": "DAYUN JING", "line2": "A PROFECIA DA GRANDE NUVEM"}},
                {"id": "B7-4", "image": "imagens/B7-4.png", "card": {"line1": "690 d.C. · A COROAÇÃO", "line2": "PROCLAMAÇÃO DA DINASTIA ZHOU"}}
            ]
        },
        {
            "id": "bloco_08",
            "audio": "audios/bloco 8.wav",
            "srt": "audios/bloco 8.srt",
            "scenes": [
                {"id": "B8-1", "image": "imagens/B8-1.png", "card": {"line1": "EXAMES IMPERIAIS (KEJU)", "line2": "A ASCENSÃO DOS TALENTOS"}},
                {"id": "B8-2", "image": "imagens/B8-2.png", "card": {"line1": "PORTÃO NORTE", "line2": "BEIMEN XUESHI: OS ERUDITOS"}},
                {"id": "B8-3", "image": "imagens/B8-3.png", "card": {"line1": "CAMPOS MILITARES", "line2": "A PROFISSIONALIZAÇÃO DO EXÉRCITO"}}
            ]
        },
        {
            "id": "bloco_09",
            "audio": "audios/bloco 9.wav",
            "srt": "audios/bloco 9.srt",
            "scenes": [
                {"id": "B9-1", "image": "imagens/B9-1.png", "card": {"line1": "O DILEMA DINÁSTICO", "line2": "CLÃ WU OU CLÃ LI?"}},
                {"id": "B9-2", "image": "imagens/B9-2.png", "card": {"line1": "698 d.C. · O RETORNO", "line2": "A RESTAURAÇÃO DA LINHAGEM TANG"}}
            ]
        },
        {
            "id": "bloco_10",
            "audio": "audios/bloco 10.wav",
            "srt": "audios/bloco 10.srt",
            "scenes": [
                {"id": "B10-1", "image": "imagens/B10-1.png", "card": {"line1": "705 d.C. · LUOYANG", "line2": "O GOLPE DOS CINCO MINISTROS"}},
                {"id": "B10-2", "image": "imagens/B10-2.png", "card": {"line1": "A ABDICAÇÃO", "line2": "O RETORNO DE ZHONGZONG"}},
                {"id": "B10-3", "image": "imagens/b10-3.png", "card": {"line1": "705 d.C. · PALÁCIO SHANGYANG", "line2": "OS ÚLTIMOS DIAS DE WU ZETIAN"}}
            ]
        },
        {
            "id": "bloco_11",
            "audio": "audios/bloco 11.wav",
            "srt": "audios/bloco 11.srt",
            "scenes": [
                {"id": "B11-1", "image": "imagens/b11-1.png", "card": {"line1": "HISTORIOGRAFIA CONFUCIONISTA", "line2": "O JULGAMENTO MORAL"}},
                {"id": "B11-2", "image": "imagens/b11-2.png", "card": {"line1": "O IMPÉRIO TANG", "line2": "PROSPERIDADE E ESTABILIDADE"}}
            ]
        },
        {
            "id": "bloco_12",
            "audio": "audios/bloco 12.wav",
            "srt": "audios/bloco 12.srt",
            "scenes": [
                {"id": "B12-1", "image": "imagens/b12-1.png", "card": {"line1": "QIANLING · PROVÍNCIA DE SHAANXI", "line2": "O MAUSOLÉU DOS DOIS MONARCAS"}},
                {"id": "B12-2", "image": "imagens/b12-2.png", "card": {"line1": "WUZI BEI", "line2": "A ESTELA SEM PALAVRAS"}},
                {"id": "B12-3", "image": "imagens/b12-3.png", "card": {"line1": "EPÍLOGO", "line2": "O VEREDITO DO TEMPO"}}
            ]
        }
    ]

    for b in blocks_meta:
        dur = get_wav_duration(b["audio"])
        num_scenes = len(b["scenes"])
        scene_dur = round(dur / num_scenes, 3)
        curr_time = 0.0
        scenes_list = []
        for i, s in enumerate(b["scenes"]):
            this_dur = scene_dur if i < num_scenes - 1 else round(dur - curr_time, 3)
            scenes_list.append({
                "id": s["id"],
                "image": s["image"],
                "start": round(curr_time, 3),
                "duration": this_dur,
                "card": {
                    "line1": s["card"]["line1"],
                    "line2": s["card"]["line2"],
                    "show_at": round(curr_time + 0.8, 3),
                    "card_duration": 6.0
                } if s.get("card") else None
            })
            curr_time += this_dur

        manifest["blocks"].append({
            "id": b["id"],
            "audio": b["audio"],
            "srt": b["srt"],
            "duration": dur,
            "scenes": scenes_list
        })

    # Bloco CTA Final
    dur_cta = get_wav_duration("audios/cta final.wav")
    manifest["blocks"].append({
        "id": "cta_final",
        "audio": "audios/cta final.wav",
        "srt": None,
        "duration": dur_cta,
        "scenes": [
            {
                "id": "CTA",
                "image": "imagens/thumb.png",
                "start": 0.0,
                "duration": dur_cta,
                "card": {"line1": "HISTÓRIAS CHINESAS", "line2": "INSCREVA-SE NO CANAL", "show_at": 0.5, "card_duration": dur_cta - 1.0}
            }
        ]
    })

    os.makedirs("src", exist_ok=True)
    with open("src/timeline_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("Manifesto criado com sucesso em src/timeline_manifest.json!")

if __name__ == "__main__":
    build_manifest()
