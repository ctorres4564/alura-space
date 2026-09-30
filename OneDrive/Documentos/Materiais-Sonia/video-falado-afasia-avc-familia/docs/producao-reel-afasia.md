# Documentação Técnica — Montagem do Reel "Depois do AVC, a fala pode mudar"

## 1. Objetivo
Produzir de ponta a ponta a peça audiovisual em formato Instagram Reel (9:16, 1080x1920, 30 fps) da fonoaudióloga Sônia Torres (CRFa 1-17701), combinando trechos falados gravados com lipsync da profissional, 3 telas explicativas documentais e card padrão de encerramento.

## 2. Arquitetura do Pipeline
```
[clipe-1.mp4 (5s - Sônia)] 
       ↓
[tela-a-o-que-e-afasia.png (4.2s com Ken Burns)]
       ↓
[tela-b-sinais.png (4.2s com Ken Burns)]
       ↓
[tela-c-como-ajudar.png (4.2s com Ken Burns)]
       ↓
[clipe-2.mp4 (6.3s - Sônia)]
       ↓
[06-contatos.png (3.3s com fade-in de 0.3s)]
       ↓
[reel-afasia-avc-final.mp4 (~27.2s, 1080x1920, 30 fps, áudio sincronizado)]
```

## 3. Fluxo de Dados e Scripts
1. **Geração e Tratamento de Imagens (`scripts/gerar_telas_explicativas.py`)**:
   - Lê as fotos brutas geradas pela IA.
   - Enquadra para 1080x1920 sem distorção.
   - Salva a fotografia pura em `fotografias-sem-texto/`.
   - Adiciona faixa translúcida de fundo com cantos arredondados e tipografia Segoe UI Bold nas zonas de segurança (safe zone y=220 a y=1470).
2. **Registro de Legenda (`scripts/salvar_legenda.py`)**:
   - Grava `legenda.txt` com o texto oficial e fontes científicas (Ministério da Saúde 2013 e SBFa 2023).
3. **Montagem e Normalização (`scripts/montar_reel.py`)**:
   - Normaliza os clipes da Sônia para 1080x1920, 30 fps, áudio estéreo 44.1 kHz AAC.
   - Gera vídeos das telas estáticas com zoom lento (`zoompan`) e áudio nulo.
   - Aplica fade de 0.3s no card de contatos.
   - Concatena os 6 segmentos de forma contínua usando o filtro `concat` do FFmpeg.
   - Limpa automaticamente arquivos intermediários da pasta `_tmp/`.

## 4. Como manter ou reproduzir
Para reproduzir ou gerar nova versão:
```bash
python scripts/gerar_telas_explicativas.py
python scripts/salvar_legenda.py
python scripts/montar_reel.py
```
Todos os arquivos finais são depositados tanto na pasta oficial do Reel `Materiais-Sonia/reels/reel-afasia-avc-familia/` quanto na raiz do projeto.
