# QUEM TEM MEDO DA LIBERDADE DAS MULHERES?
> Subtítulo Editorial: *Gênero, política e disputa pelo poder.*

Mini-documentário investigativo e reflexivo produzido para formato vertical (9:16) voltado a YouTube Shorts, Instagram Reels e Facebook Reels.

---

## 1. Objetivo do Projeto

Analisar criticamente como a expressão "ideologia de gênero" é empregada em disputas políticas, explorando as relações entre antifeminismo, conservadorismo, participação feminina no eleitorado (>52% segundo dados oficiais do Tribunal Superior Eleitoral), violência política contra a mulher (Lei nº 14.192/2021) e soberania sobre o próprio corpo.

---

## 2. Stack e Ferramentas Utilizadas

- **Pipeline Audiovisual & Renderização:** FFmpeg 7.1 (H.264 High Profile, AAC 48kHz, DirectWrite/libass para legendas integradas).
- **Transcrição e Sincronia Temporal:** `faster-whisper` com extração precisa de timestamps por palavra e segmento.
- **Mixagem de Áudio:** Python (`numpy`, `wave`, `subprocess`) com ducking dinâmico via sidechain compressivo e teto limite em -1.0 dBFS.
- **Design Visual & Motion:** Pillow (PIL) e geração conceitual 1080x1920 com estética cinematográfica chiaroscuro e paleta editorial sóbria (preto, grafite, branco, vermelho profundo e roxo).

---

## 3. Estrutura de Diretórios

```
/
├── assets/
│   ├── audio/            # Trilha cinematográfica e áudio master mixado
│   ├── images/           # Imagens e fotografias documentais tratadas
│   └── scenes/           # 10 bases visuais em 1080x1920
├── docs/
│   └── arquitetura_producao.md  # Arquitetura detalhada e fluxo de dados
├── prompts/
│   └── prompts_visuais.md       # Referência de prompts cinematográficos
├── scripts/
│   ├── copy_assets.py
│   ├── generate_cover.py
│   ├── generate_scene_assets.py
│   ├── generate_soundtrack.py
│   ├── generate_subtitles.py
│   ├── render_video.py
│   └── transcribe_audio.py
├── VIDEO_LIBERDADE_MULHERES_FINAL/
│   ├── video_liberdade_mulheres.mp4   # VÍDEO FINAL RENDERIZADO
│   ├── capa_liberdade_mulheres.png    # CAPA VERTICAL HD
│   ├── legenda_instagram.txt          # TEXTO PRONTO P/ INSTAGRAM
│   ├── legenda_facebook.txt           # TEXTO PRONTO P/ FACEBOOK
│   ├── titulo_descricao_youtube.txt   # TEXTO PRONTO P/ YOUTUBE SHORTS
│   ├── legendas.srt                   # ARQUIVO DE LEGENDAS SINCRONIZADAS
│   ├── fontes_e_licencas.txt          # REGISTRO DE FONTES E LICENÇAS
│   └── relatorio_producao.txt         # RELATÓRIO TÉCNICO E QA
└── README.md
```

---

## 4. Instruções de Execução / Reprodução

1. **Transcrição:**
   ```bash
   python scripts/transcribe_audio.py
   ```
2. **Geração das Legendas Sincronizadas:**
   ```bash
   python scripts/generate_subtitles.py
   ```
3. **Composição da Trilha e Mixagem Master:**
   ```bash
   python scripts/generate_soundtrack.py
   ```
4. **Geração das Artes Cênicas e da Capa:**
   ```bash
   python scripts/generate_scene_assets.py
   python scripts/generate_cover.py
   ```
5. **Renderização do Vídeo Completo:**
   ```bash
   python scripts/render_video.py
   ```
