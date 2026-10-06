# Documentação Técnica: Vídeo / Reel "O que esperar da fala, por idade"

Material audiovisual institucional desenvolvido para a fonoaudióloga **Sônia Torres (CRFa 1-17701)**.

---

## 1. Objetivo
Transformar os 10 slides do carrossel educativo em vídeo dinâmico, acessível e profissional para as redes sociais (Instagram Reels, Stories e Feed, além de TikTok e YouTube Shorts), otimizando a retenção visual com trilha sonora acústica de piano e respeito total à Safe Zone de interfaces de aplicativos móveis.

---

## 2. Especificações Técnicas dos Formatos

| Característica | Versão Reel / Stories | Versão Vídeo Feed |
|---|---|---|
| **Resolução** | 1080 × 1920 pixels | 1080 × 1350 pixels |
| **Proporção** | 9:16 (Vertical Fullscreen) | 4:5 (Vertical Retrato) |
| **Taxa de Quadros** | 30 fps | 30 fps |
| **Codec de Vídeo** | H.264 (libx264, preset fast, CRF 18) | H.264 (libx264, preset fast, CRF 18) |
| **Formato de Pixel**| yuv420p (ampla compatibilidade mobile) | yuv420p |
| **Codec de Áudio** | AAC estéreo, 44.1 kHz, 192 kbps | AAC estéreo, 44.1 kHz, 192 kbps |
| **Trilha Sonora** | Instrumental de piano (*Warm Hope*) | Instrumental de piano (*Warm Hope*) |
| **Duração Total** | 49.4 segundos | 49.4 segundos |

---

## 3. Arquitetura de Diretórios

```
Materiais-Sonia/
├── reels/
│   └── reel-o-que-esperar-da-fala-por-idade/
│       ├── frames-reel-9x16/            # 10 frames verticais 1080x1920 (PNG)
│       ├── video-carrossel-4x5.mp4      # Vídeo 4:5 para o feed (1080x1350)
│       ├── video-reel-9x16.mp4          # Vídeo 9:16 para Reels e Stories (1080x1920)
│       └── roteiro-video.md             # Roteiro, minutagem e sugestão de locução
├── prompts/
│   └── video-o-que-esperar-da-fala-por-idade-prompts.md # Direção de cena e enquadramentos
├── scripts/
│   └── gerar_video_o_que_esperar_da_fala_por_idade.py   # Script de geração audiovisual
└── docs/
    └── video-o-que-esperar-da-fala-por-idade.md         # Esta documentação técnica
```

---

## 4. Como Executar e Re-renderizar
Para atualizar ou reprocessar os vídeos após alterações nas lâminas:

```powershell
python scripts/gerar_video_o_que_esperar_da_fala_por_idade.py
```
