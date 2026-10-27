# Documentação Técnica — Produção Audiovisual do Reel
**Peça:** "Seu filho pode estar falando com você sem dizer uma palavra"  
**Profissional:** Sônia Torres — Fonoaudióloga (Rio de Janeiro - RJ)  
**Site:** [sonia.fonosuite.com](https://sonia.fonosuite.com) | **Contato:** (21) 97748-6801  

---

## 1. Visão Geral e Objetivo
Este projeto implementa o pipeline automatizado de produção audiovisual para o Instagram e Facebook Reels da fonoaudióloga Sônia Torres.  
A peça aborda a relevância da comunicação não verbal e gestual no desenvolvimento infantil, destacando que apontar, estender os braços e conduzir a atenção são formas legítimas de comunicação, ao mesmo tempo em que reforça a importância da avaliação fonoaudiológica diante de dúvidas sobre atraso de fala.

---

## 2. Arquitetura da Solução e Estrutura de Diretórios

```
video1/
├── assets/
│   ├── audio/           # Narração original, trilha sonora instrumental e mix final
│   ├── fonts/           # PlusJakartaSans-Variable.ttf (tipografia oficial)
│   └── images/          # Cenas fotorrealistas geradas (9:16) e card final
├── components/
│   └── final_card.py    # Renderizador do card institucional de encerramento
├── docs/
│   └── documentacao_producao_reel.md  # Esta documentação
├── prompts/
│   └── prompts_cenas_reel.md          # Especificação cinematográfica dos prompts
├── scripts/
│   ├── gerar_capa.py    # Gerador da capa oficial vertical (1080x1920)
│   └── render_reel.py   # Motor de composição de frames, Ken Burns e FFmpeg
├── services/
│   └── audio_service.py # Concatenação da voz e mixagem com ducking
├── tests/
│   ├── test_audio_pipeline.py  # Teste de integridade de áudios e assets
│   └── test_final_delivery.py  # Teste de conformidade técnica do vídeo e capa
├── utils/
│   └── time_utils.py    # Utilitários de timecode e temporização
├── 01.mp3 a 04.mp3       # Áudios brutos originais da Sônia Torres
├── capa_reel_sonia.png  # Entregável: Capa oficial em alta resolução
├── legenda_reel_sonia.txt # Entregável: Texto de copy para as redes
└── reel_sonia_comunicacao_infantil.mp4 # Entregável: Vídeo finalizado
```

---

## 3. Fluxo de Dados e Pipeline Audiovisual

1. **Ingestão e Validação de Áudio**:
   - Os 4 áudios (`01.mp3`, `02.mp3`, `03.mp3`, `04.mp3`) são lidos e concatenados sem artefatos ou cortes.
   - Duração da narração: **35,63 segundos**.
   - Adiciona-se o card final institucional com duração de **3,50 segundos**, totalizando **39,13 segundos**.
   - A trilha instrumental *Warm Hope* é inserida em loop contínuo com atenuação automática (*audio ducking* a 9% do volume nominal) durante a voz, subindo suavemente ao final da fala e concluindo com *fade out* de 1,8 segundos.

2. **Direção Visual e Consistência**:
   - Personagens: mãe negra brasileira de 30 anos e seu filho de 2 anos, com vestimentas do cotidiano e expressões naturais, em uma sala de estar residencial acolhedora e iluminada.
   - Aplicação de efeito de câmera suave (*Ken Burns* com aproximação progressiva entre 1.00 e 1.05) para manter dinamismo cinematográfico contínuo.

3. **Tipografia e Camadas Gráficas**:
   - Pílula superior (Y=190 a 330): Títulos de destaque em caixa alta, fonte *Plus Jakarta Sans*, com alto contraste sobre fundo escuro semitransparente na cor institucional `#2C1240` com borda dourada `#C8A96A`.
   - Pílula inferior (Y=1400 a 1560): Legendas sincronizadas em português brasileiro, em conformidade com as zonas seguras do Instagram Reels.

4. **Card de Identificação Profissional**:
   - Apresenta os dados fidedignos da profissional:
     - Nome: **SÔNIA TORRES**
     - Profissão: **Fonoaudióloga**
     - Localidade: **Rio de Janeiro — RJ**
     - Site: **sonia.fonosuite.com**
     - Telefone: **(21) 97748-6801**

---

## 4. Especificações Técnicas do Arquivo Final

| Parâmetro | Valor |
|---|---|
| Arquivo de Vídeo | `reel_sonia_comunicacao_infantil.mp4` |
| Resolução | 1080 × 1920 pixels (9:16 Vertical) |
| Taxa de Quadros | 30.0 fps |
| Codec de Vídeo | H.264 / AVC (High Profile, CRF 18) |
| Codec de Áudio | AAC Stereo 192 kbps, 48 kHz |
| Duração Exata | 39.13 segundos |
| Capa do Reel | `capa_reel_sonia.png` (1080 × 1920 pixels) |
| Legenda de Publicação | `legenda_reel_sonia.txt` |

---

## 5. Como Executar e Manter

Para reprocessar ou gerar novas variações do Reel:

```bash
# 1. Executar testes de validação prévia
python -m pytest tests/test_audio_pipeline.py -v

# 2. Gerar novo áudio mixado (se houver alteração de trilha ou narração)
python services/audio_service.py

# 3. Gerar card institucional final
python components/final_card.py

# 4. Gerar capa oficial
python scripts/gerar_capa.py

# 5. Renderizar o vídeo completo
python scripts/render_reel.py

# 6. Rodar testes de conformidade técnica final
python -m pytest tests/test_final_delivery.py -v
```
