# Documentação Técnica e Editorial: Reel "Essa Criança Não Precisa de Fono"

- **Título:** Essa criança não precisa de fono. Precisa é de limites!
- **Profissional:** Sônia Torres — Fonoaudióloga
- **Formato:** Vídeo vertical 9:16 (1080×1920), 30 fps, MP4 (H.264 / AAC)
- **Duração Estimada:** 30 a 33 segundos
- **Objetivo:** Provocar reflexão e quebrar o estigma de que dificuldades na fala e na linguagem infantil são meramente "birra" ou "falta de limites".

---

## 1. Arquitetura da Produção

```
01reels_novos/
├── assets/
│   └── fonts/ (Poppins, Cinzel/Playfair)
├── docs/
│   └── roteiro_limites_comunicacao.md
├── prompts/
│   └── prompts_cenas_limites.md
├── scripts/
│   ├── gerar_narracao_limites.py
│   └── renderizar_reel_limites.py
└── publicacao/
    └── limites-comunicacao/
        ├── audios/ (áudios das cenas e narração contínua normalizada)
        ├── imagens/ (quadros 1 a 6 tratados com legendas e animações)
        ├── clipes/ (clipes de vídeo com interpolação de movimento Ken Burns)
        ├── reel_sonia_limites_final.mp4 (vídeo renderizado final)
        ├── reel_sonia_capa.png (capa para Instagram)
        ├── reel_sonia_legenda.txt (texto para postagem)
        └── reel_sonia_legendas.srt (legendas sincronizadas)
```

---

## 2. Fluxo de Dados e Renderização

1. **Síntese de Áudio Neural (Edge-TTS):**
   - Cada trecho de fala é gerado com a voz neural `pt-BR-FranciscaNeural`, aplicando ajustes de entonação (pitch/rate) condizentes com o tom dramático de cada cena.
   - Os áudios são concatenados e normalizados em loudness de acordo com a norma EBU R128 (-16 LUFS).
2. **Medição Exata de Duração:**
   - As durações reais de cada trecho de áudio determinam a duração exata dos clipes das Cenas 1 a 5.
   - A Cena 6 (Card Final) permanece visível por 5,5 segundos com a música de fundo em destaque.
3. **Tratamento Visual e Tipografia:**
   - Composição de lettering de alto impacto respeitando as safe zones do Instagram (1080×1920, margens superior de 250px e inferior de 380px livres).
   - Destaque em dourado (`#D4AF37`) nas palavras-chave e tipografia refinada para reforçar autoridade e sofisticação.
4. **Animação Cinematográfica (Motion Dynamics):**
   - Aplicação de movimentos contínuos de câmera suave:
     - Cena 1: *Slow push-in* (zoom sutil aproximando na criança).
     - Cena 2: *Slow horizontal pan & push* (direcionando o olhar do gesto para o brinquedo).
     - Cena 3: *Subtle close-in* (aproximação lenta no rosto expressivo).
     - Cena 4: *Gentle lateral tracking* (movimento lateral estabilizado na conexão mãe-filha).
     - Cena 5: *Fade tipográfico dramático*.
     - Cena 6: *Card CTA estático com acabamento suave*.
5. **Mixagem de Áudio Final:**
   - Narração principal em primeiro plano.
   - Trilha sonora instrumental suave com ducking a -26 dB durante as falas e subida suave para -15 dB no card final, terminando com fade-out de 2 segundos.

---

## 3. Roteiro Cronometrado

| Cena | Janela Temporal | Texto na Tela | Narração Sônia Torres | Tom / Efeito |
| :--- | :--- | :--- | :--- | :--- |
| **1. O Julgamento** | 00:00 – 00:04 | “ESSA CRIANÇA NÃO PRECISA DE FONO! PRECISA É DE LIMITES!” | *"Essa criança não precisa de fono. Precisa é de limites!"* | Crítico, provocativo; impacto sonoro discreto inicial. |
| **2. A Dificuldade** | 00:04 – 00:10 | “ELA TENTA FALAR. NÃO CONSEGUE SE EXPLICAR. E FICA FRUSTRADA.” | *"Ela tenta dizer o que quer. Mas nem sempre consegue se fazer entender."* | Descritivo, observador e sensível. |
| **3. A Virada** | 00:10 – 00:16 | “MAS E SE NÃO FOR FALTA DE LIMITES?” | *"E se o problema não for falta de limites?"* | Interrogativo, reflexivo com pausa dramática. |
| **4. A Compreensão** | 00:16 – 00:23 | “DIFICULDADES DE COMUNICAÇÃO PODEM GERAR FRUSTRAÇÃO.” | *"Dificuldades para compreender ou se expressar também podem gerar frustração."* | Acolhedor, esclarecedor, empático. |
| **5. Frase de Impacto**| 00:23 – 00:27 | “NEM TODA CRISE É BIRRA.” (branco)<br>“NEM TODA DIFICULDADE É DESOBEDIÊNCIA.” (dourado) | *"Antes de julgar, procure compreender."* | Firme, solene, pausa expressiva. |
| **6. Card Final** | 00:27 – 00:33 | “FALTA DE LIMITES OU DIFICULDADE DE COMUNICAÇÃO? O QUE VOCÊ PENSA? COMENTE!” | *(Apenas trilha sonora reflexiva)* | Institucional, convidativo, 5 segundos legíveis. |

---

## 4. Como Manter e Reexecutar

Para reproduzir ou customizar os vídeos e recursos:
1. Executar `python scripts/gerar_narracao_limites.py` para atualizar os arquivos de áudio e narração.
2. Executar `python scripts/renderizar_reel_limites.py` para gerar os cards, clipes animados e montagem final do MP4.
3. Os arquivos finais estarão organizados e disponíveis na pasta `publicacao/limites-comunicacao/`.
