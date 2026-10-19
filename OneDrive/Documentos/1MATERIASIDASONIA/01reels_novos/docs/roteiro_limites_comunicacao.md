# Documentação Técnica e Editorial: Reel "Essa Criança Não Precisa de Fono" (Versão com Áudios Reais da Pasta `audios2`)

- **Título:** Essa criança não precisa de fono. Precisa é de limites!
- **Profissional:** Sônia Torres — Fonoaudióloga
- **Formato:** Vídeo vertical 9:16 (1080×1920), 30 fps, MP4 (H.264 / AAC)
- **Duração Total:** 41.50 segundos
- **Objetivo:** Desmistificar a confusão frequente entre dificuldades de linguagem/comunicação infantil e desobediência ou falta de limites.
- **Origem dos Áudios:** Gravações reais da pasta `audios2/` (`audio1.mp3` a `audio6.mp3`).

---

## 1. Timeline e Sincronização Detalhada

| Marco Temporal | Áudio Fonte | Trecho Falado | Cena Visual | Lettering na Tela (Safe Area) |
| :--- | :--- | :--- | :--- | :--- |
| **00:00.0 – 00:03.2** | `audio1.mp3` (pt 1) | *"Na minha época, criança assim precisava era de limites."* | **Cena 1:** Menina no sofá angustiada tentando falar; mãe ao fundo de braços cruzados | “NA MINHA ÉPOCA, CRIANÇA ASSIM PRECISAVA DE LIMITES!” |
| **00:03.2 – 00:06.5** | `audio1.mp3` (pt 2) | *"Quantas vezes você já ouviu essa frase?"* | **Cena 1:** Câmera continua em aproximação lenta (push-in) | “QUANTAS VEZES VOCÊ JÁ OUVIU ESSA FRASE?” |
| **00:06.5 – 00:09.5** | `audio2.mp3` (pt 1) | *"Mas será que todo comportamento interpretado como desobediência..."* | **Cena 2:** Menina apontando para o brinquedo na mesa; mãe com dúvida | “TODO COMPORTAMENTO INTERPRETADO COMO DESOBEDIÊNCIA...” |
| **00:09.5 – 00:12.6** | `audio2.mp3` (pt 2) | *"...é realmente falta de limites?"* | **Cena 2:** Pan lateral suave direcionando o olhar | “...É REALMENTE FALTA DE LIMITES?” |
| **00:12.6 – 00:16.8** | `audio3.mp3` (pt 1) | *"Algumas crianças encontram dificuldades para compreender ou expressar o que desejam..."* | **Cena 3:** Close-up emotivo e expressivo no olhar da menina | “DIFICULDADES PARA COMPREENDER OU SE EXPRESSAR...” |
| **00:16.8 – 00:21.1** | `audio3.mp3` (pt 2) | *"...e essa dificuldade pode provocar frustração."* | **Cena 3:** Close-in sutil evidenciando a vulnerabilidade | “...PODEM GERAR MUITA FRUSTRAÇÃO.” |
| **00:21.1 – 00:25.0** | `audio4.mp3` (pt 1) | *"Isso não significa que toda a crise esteja relacionada à linguagem."* | **Cena 4:** Mãe agachada na altura da filha, segurando suas mãos com carinho | “NEM TODA CRISE ESTÁ NA LINGUAGEM.” |
| **00:25.0 – 00:29.1** | `audio4.mp3` (pt 2) | *"Significa que precisamos compreender antes de julgar."* | **Cena 4:** Tracking lateral suave na escuta afetuosa | “PRECISAMOS COMPREENDER ANTES DE JULGAR.” |
| **00:29.1 – 00:35.3** | `audio5.mp3` | *"E você, acha que muitos adultos confundem dificuldades de comunicação com falta de educação?"* | **Cena 5:** Card de alto contraste em roxo profundo e dourado | “NEM TODA CRISE É BIRRA.” (Branco)<br>“CONFUNDIMOS COMUNICAÇÃO COM FALTA DE EDUCAÇÃO?” (Dourado) |
| **00:35.3 – 00:37.5** | `audio6.mp3` | *"Conte sua opinião nos comentários."* | **Cena 6:** Card Final Institucional Sônia Torres | Chamada falada sobre o card |
| **00:37.5 – 00:41.5** | *(Música)* | *(Trilha instrumental de piano e violão em destaque suave com fade-out)* | **Cena 6:** Exposição completa dos dados de contato por mais 4 segundos | “FALTA DE LIMITES OU DIFICULDADE DE COMUNICAÇÃO?”<br>“O QUE VOCÊ PENSA? COMENTE!”<br>Sônia Torres \| Fonoaudióloga |

---

## 2. Parâmetros de Mixagem e Áudio

- **Normalização EBU R128:** -16 LUFS integrado (padrão Instagram/Reels).
- **Trilha de Fundo:**
  - `00:00 a 00:37.5`: Ducking constante a **-26 dB** para manter a inteligibilidade cristalina da voz humana.
  - `00:37.5 a 00:39.5`: Subida suave da música para **-15 dB** no card final.
  - `00:39.5 a 00:41.5`: Fade-out progressivo de 2 segundos.
- **Efeito de Impacto:** Frequência de 55 Hz adicionada aos 0.05s de abertura, realçando a força da primeira frase sem sobrecarregar o áudio.

---

## 3. Scripts de Execução

- `scripts/renderizar_reel_limites_v2.py`: Script principal de montagem, renderização e sincronização.
