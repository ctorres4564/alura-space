# Documentação da Edição e Renderização do Vídeo Master

## Episódio 2: Wu Zetian — A Mulher que Conquistou o Trono da China

### 1. Visão Geral e Objetivo
Este documento detalha o processo de automação, sincronização temporal, design gráfico de overlays e renderização do vídeo master unificado em Full HD (1080p, 30fps) para o canal *Histórias Chinesas*.

O objetivo foi reunir os 12 blocos narrativos, o gancho de 3 segundos, a vinheta oficial, as 41 imagens geradas por IA com movimentação de câmera (Ken Burns), as legendas e os cartões de contexto histórico (datas, locais e capítulos) com estética imperial refinada.

---

### 2. Arquitetura da Solução

O pipeline é 100% modular, reproduzível e automatizado via scripts Python e FFmpeg:

```
[Áudios WAV + Transcrições SRT + Imagens 4K]
                      │
                      ▼
   [scripts/build_timeline_manifest.py]
                      │
                      ▼
           (src/timeline_manifest.json)
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
[scripts/generate_title_cards.py]  [assets/intro_historias_chinesas.mp4]
         │ (assets/title_cards/*.png)
         └────────────┬────────────┘
                      ▼
       [scripts/render_video_master.py]
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
(14 Chunks renderizados)    (Concatenação Lossless)
        │                           │
        └─────────────┬─────────────┘
                      ▼
   [Ep2_WuZetian_1080p_Master_Completo.mp4] (1080p Full HD)
```

---

### 3. Fluxo de Dados e Componentes

1. **Manifesto da Linha do Tempo (`src/timeline_manifest.json`)**:
   - Mapeia cada bloco pelo seu áudio de referência com medição por amostragem de frames WAV (`wave.open`).
   - Define a transição de cada imagem e o momento milimétrico de entrada (`st_in`), duração (`card_duration`) e saída de cada cartão histórico.

2. **Cartões Gráficos Imperiais (`scripts/generate_title_cards.py`)**:
   - Gera overlays em PNG com canal alfa transparente (1920x1080).
   - Posicionados no canto superior esquerdo (`x=75, y=70`), garantindo distância segura e harmonia visual com as legendas narrativas na faixa inferior (`y ~ 950`).
   - Elementos de design:
     - Borda e barra vertical douradas imperial Tang (`#D4AF37`);
     - Fundo translúcido escuro (`rgba(15, 15, 20, 190)`);
     - Tipografia clássica serifada: linha de data/local em dourado marfim e linha de título em branco puro.

3. **Renderizador em Chunks (`scripts/render_video_master.py`)**:
   - Divide a renderização nos 14 blocos correspondentes aos arquivos de narração original.
   - Aplica os cartões com fade-in suave (0.5s) e fade-out suave (0.5s) através de filtros `format=rgba,fade=t=in...,fade=t=out...` e `overlay=0:0:enable='between(...)'`.
   - Concatena os blocos finais por meio de `ffmpeg -f concat -c copy`, garantindo rapidez e consistência absoluta de áudio e vídeo sem perda de sincronia.

---

### 4. Especificações Técnicas do Master Gerado

- **Arquivo**: `Ep2_WuZetian_1080p_Master_Completo.mp4`
- **Duração Total**: 21 minutos e 50 segundos (1310.89 segundos)
- **Resolução**: 1920 x 1080 (16:9 Full HD)
- **Taxa de Quadros**: 30 fps progressivo
- **Codec de Vídeo**: H.264 High Profile @ Level 4.0 (CRF 18 / Preset Fast)
- **Bitrate Médio de Vídeo**: ~2663 kbps
- **Codec de Áudio**: AAC estéreo (44.1 kHz, 195 kbps)
- **Tamanho do Arquivo**: ~448 MB

---

### 5. Como Reproduzir ou Modificar

Para re-renderizar o vídeo ou ajustar algum cartão:
1. Altere o texto ou imagem desejada em `src/timeline_manifest.json` ou no script correspondente.
2. Gere novamente os cartões:
   ```bash
   python scripts/generate_title_cards.py
   ```
3. Execute o renderizador master:
   ```bash
   python scripts/render_video_master.py
   ```
O renderizador é inteligente e só processará os chunks que forem alterados ou removidos.
