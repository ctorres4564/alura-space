# Histórias Chinesas — Ep. 2: Wu Zetian

Documentário histórico e épico sobre **Wu Zetian**, a única mulher a governar a China imperial como imperadora soberana em nome próprio (Dinastia Zhou).

---

## 🎯 Objetivo do Projeto
Automatizar a produção, sincronização audiovisual e renderização do vídeo master unificado em Full HD (1080p, 30fps), contendo:
- 12 blocos narrativos + gancho + abertura + vinheta oficial + chamada final (CTA);
- Movimentação suave de câmera (Ken Burns);
- 42 cartões de contexto histórico com design imperial Tang;
- Legendas sincronizadas;
- Renderização modular sem perda de sincronia.

---

## 🛠️ Stack Utilizada
- **Python 3.12**
- **FFmpeg 7.1**
- **Pillow (PIL)** (Processamento gráfico de overlays e tipografia)

---

## 📁 Estrutura de Diretórios
```text
video2/
├── assets/                  # Vinheta oficial e cartões históricos gerados
│   ├── intro_historias_chinesas.mp4
│   └── title_cards/
├── audios/                  # Faixas de áudio WAV e legendas SRT
├── docs/                    # Documentação técnica e amostras visuais
│   └── edicao_video_master.md
├── imagens/                 # 41 ilustrações cinematográficas em alta definição
├── prompts/                 # Referências de prompts e planejamento de cenas
│   └── prompts_cenas.md
├── scripts/                 # Scripts do pipeline de automação
│   ├── build_timeline_manifest.py
│   ├── generate_title_cards.py
│   ├── render_video_master.py
│   ├── check_motion.py
│   └── sample_timeline.py
├── src/                     # Manifestos de dados e timeline da montagem
│   └── timeline_manifest.json
├── Ep2_WuZetian_1080p_Master_Completo.mp4 # Vídeo Master Final Renderizado
├── ROTEIRO.docx             # Roteiro oficial
└── README.md
```

---

## 🚀 Como Executar

1. **Instalar dependências**:
   ```bash
   pip install pillow
   ```

2. **Gerar os cartões históricos**:
   ```bash
   python scripts/generate_title_cards.py
   ```

3. **Renderizar o vídeo master unificado**:
   ```bash
   python scripts/render_video_master.py
   ```
