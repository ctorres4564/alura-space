# Documentação de Arquitetura e Produção Audiovisual

## 1. Objetivo do Projeto

Produzir o documentário político vertical (9:16, 1080x1920, 30fps) intitulado **"QUEM TEM MEDO DA LIBERDADE DAS MULHERES? — Gênero, política e disputa pelo poder"**, com duração exata de **153.8 segundos** (baseada 100% no áudio de narração original `01.wav`), gerando todos os entregáveis para YouTube Shorts, Instagram Reels e Facebook Reels.

## 2. Arquitetura do Pipeline

```
[01.wav (Áudio Original)]
        │
        ├──> [faster-whisper / numpy / ffmpeg] ─────────> [transcription.json & legendas.srt]
        │                                                               │
        ├──> [generate_soundtrack.py] ──────────────────────────┐       │
        │    (Composição musical com progressão e sidechain)    │       │
        │                                                       ▼       ▼
        └──> [generate_visuals.py] ────────────────────────> [ffmpeg compositor]
             (Renderização de frames e cenas cinematográficas)          │
                                                                        ▼
                                                   [video_liberdade_mulheres.mp4]
```

## 3. Divisão Sincronizada das 10 Cenas

| Cena | Início | Fim | Duração | Tema / Eixo Narrativo |
|---|---|---|---|---|
| **Cena 01** | 00:00.00 | 00:17.20 | 17.20s | A Pergunta Incômoda ("Por que a extrema direita fala tanto em ideologia de gênero?") |
| **Cena 02** | 00:17.20 | 00:39.50 | 22.30s | A Construção de um Inimigo ("Inimigo simbólico", rótulos agregados) |
| **Cena 03** | 00:39.50 | 00:50.00 | 10.50s | A Disputa pelo Poder (Socióloga Camila Galetti: Família, Corpo, Autoridade, Poder) |
| **Cena 04** | 00:50.00 | 00:78.90 | 28.90s | A Contradição do Voto Feminino (TSE: >52% do eleitorado vs. papéis tradicionais) |
| **Cena 05** | 00:78.90 | 00:84.50 | 05.60s | O Antifeminismo como Instrumento Político (Estratégia de mobilização) |
| **Cena 06** | 00:84.50 | 00:95.30 | 10.80s | O Corpo Feminino como Território de Disputa (Saúde pública vs. julgamento moral) |
| **Cena 07** | 00:95.30 | 01:17.70 | 22.40s | Violência Política contra Mulheres (Lei nº 14.192/2021, tribunas e ataques) |
| **Cena 08** | 01:17.70 | 01:34.10 | 16.40s | Liberdade para Quem? (Convicções pessoais vs. restrição de direitos) |
| **Cena 09** | 01:34.10 | 01:47.20 | 13.10s | O Centro da Disputa (Quem tem autoridade para definir como uma mulher deve viver?) |
| **Cena 10** | 01:47.20 | 01:53.80 | 06.60s | Encerramento ("QUEM TEM MEDO DA LIBERDADE DAS MULHERES?") |

## 4. Componentes e Tecnologias

- **Processamento de Áudio:** `ffmpeg`, `faster-whisper`, `wave`, `numpy`.
- **Geração de Imagens & Design Gráfico:** `generate_image`, `Pillow`, `matplotlib` para gráficos vetoriais de dados oficiais do TSE, layout 1080x1920.
- **Trilha Sonora Original:** Síntese e composição procedural com camadas harmônicas e sub-bass documental (piano minimalista, pulso grave, ambient drones) sintetizados matematicamente ou processados via áudio digital para garantir 100% de isenção de direitos autorais e sincronia com a narração (ducking/sidechaining suave de -14dB durante a fala).
- **Legendas Dinâmicas:** Formato SRT e renderização com fontes sólidas sem serifa, contorno escuro e destaques em cores de tensão (vermelho profundo / amarelo discreto / roxo).
- **Montagem e Renderização:** `ffmpeg` com aceleração, codificação H.264 (perfil High, CRF 18-20, yuv420p) e áudio AAC 48kHz stereo.

## 5. Como Manter e Executar a Funcionalidade

- Para gerar ou atualizar a transcrição: `python scripts/transcribe_audio.py`
- Para gerar as imagens e animações: `python scripts/generate_visual_assets.py`
- Para compor a trilha musical: `python scripts/generate_soundtrack.py`
- Para compor e exportar o vídeo final: `python scripts/render_video.py`
- Os artefatos finais são depositados diretamente em `VIDEO_LIBERDADE_MULHERES_FINAL/`.
