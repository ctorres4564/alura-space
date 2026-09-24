# Documentação Técnica e Editorial: Reel 01 — Fala aos 12 Meses

**Série Educativa para Redes Sociais**  
**Profissional:** Sônia Torres · Fonoaudióloga · CRFa 1-17701 · `@torresdafono`  
**Peça:** Reel 01 — *"Meu filho tem 1 ano e ainda não fala nenhuma palavra. Devo me preocupar?"*  
**Formato:** Reel vertical 9:16 (1080 × 1920 pixels) — 5 telas  
**Duração estimada:** 45 segundos  
**Localização dos Arquivos:** `reels/reel-01-um-ano-sem-palavras/`

---

## 1. Objetivo da Publicação

Esclarecer, de forma humanizada, acolhedora e respaldada cientificamente, uma das angústias mais recorrentes entre pais de primeira viagem: a ausência de palavras articuladas completas aos 12 meses de idade.

A publicação tem função preventiva e orientadora:
- **Desmistificar a expectativa irreal** de frases ou vocabulário formal com apenas 1 ano.
- **Enfatizar os pré-requisitos comunicativos** que antecedem a fala (gestos sociais como dar tchau, apontar, atenção compartilhada, resposta ao nome e compreensão do "não").
- **Apresentar marcos objetivos de atenção** (como ausência de gestos aos 12m ou menos de 6 palavras aos 18m), estimulando a procura precoce de orientação profissional caso necessário.

---

## 2. Rigor Técnico e Conformidade Ética

### 2.1 Fontes Científicas Consultadas
- **Caderneta da Criança (Edição 2025/2026, Ministério da Saúde do Brasil)**: Referência nacional primária para acompanhamento do desenvolvimento da comunicação e triagem primária.
- **Sociedade Brasileira de Pediatria (SBP) / CDC — Checklists de Marcos do Desenvolvimento**: Marcos consolidados onde 75% ou mais das crianças atingem a habilidade na referida faixa etária.
- **Código de Ética da Fonoaudiologia (Resolução CFFa nº 640/2021) e Guia de Mídias Sociais (CFFa nº 756/2024)**:
  - Total ausência de promessas de cura ou diagnósticos automáticos via redes sociais.
  - Abordagem de "sinais para avaliação", sem alarmismo ou culpabilização dos responsáveis.
  - Identificação profissional obrigatória (*Sônia Torres · Fonoaudióloga · CRFa 1-17701*).
  - Proteção integral da imagem de menores: nenhuma criança identificável; enquadramentos focados em mãos, visão dorsal ou apoio afetuoso.

---

## 3. Arquitetura do Sistema Visual

As 5 telas foram desenhadas respeitando rigorosamente a **Safe Zone do Instagram Reels (1080 × 1920 px)**:

```
                  SAFE ZONE INSTAGRAM REELS (1080 × 1920 px)
  ┌────────────────────────────────────────────────────────────────────────┐
  │  Y: 0 – 240 px      Zona Superior do App (Status bar, busca, perfil)   │
  ├────────────────────────────────────────────────────────────────────────┤
  │                                                                        │
  │  Y: 260 – 1560 px   ÁREA ÚTIL EDITORIAL (LIVRE DE ELEMENTOS DA UI)     │
  │                     - Pill Badge de Categoria                          │
  │                     - Card translúcido escuro de alto contraste        │
  │                     - Tipografia editorial (Segoe UI / Plus Jakarta)   │
  │                     - Fotografia documental de fundo                   │
  │                                                                        │
  ├────────────────────────────────────────────────────────────────────────┤
  │  Y: 1600 – 1920 px  Zona Inferior do App (Nome de áudio, legenda, CTA) │
  └────────────────────────────────────────────────────────────────────────┘
```

- **Paleta Cromática:**
  - Base do Card: `#13241B` (Verde Petróleo Profundo translúcido com 89% de opacidade)
  - Borda do Card: `#547A5F` (Verde Oliva Suave, 2px)
  - Badge Superior: `#F0EBE0` (Creme Suave) com texto `#193024`
  - Destaques / Pontos de Alerta: `#F5A882` (Terracota Acolhedor)
  - Tipografia Principal: Branco Puro (`#FFFFFF`) e Branco Sálvia (`#E1E8E2`)
- **Fotografia:** Documental estilo lifestyle com luz natural, estética brasileira autêntica e representação étnico-racial inclusiva.

---

## 4. Estrutura de Diretórios e Arquivos

```
Materiais-Sonia/
├── prompts/
│   └── reel-01-um-ano-sem-palavras-prompts.md   # Prompts fotográficos detalhados (5 imagens)
├── scripts/
│   └── gerar_telas_reel_01_um_ano.py           # Script de composição gráfica Pillow
├── docs/
│   └── reel-01-um-ano-sem-palavras.md          # Esta documentação
└── reels/
    └── reel-01-um-ano-sem-palavras/
        ├── raw-photos/                         # Fotografias puras em alta resolução
        │   ├── 01-gancho.jpg
        │   ├── 02-validacao.jpg
        │   ├── 03-o-que-esperar.jpg
        │   ├── 04-sinais-alerta.jpg
        │   └── 05-fechamento.jpg
        ├── fotografias-sem-texto/              # Imagens cortadas 1080x1920 sem texto (para Canva)
        │   ├── 01-gancho-sem-texto.png ... 05-fechamento-sem-texto.png
        └── telas-finais/                       # Telas finalizadas prontas para publicação/edição
            ├── 01-gancho.png
            ├── 02-validacao.png
            ├── 03-o-que-esperar.png
            ├── 04-sinais-alerta.png
            ├── 05-fechamento.png
            └── prancha-visao-geral.png         # Painel panorâmico comparativo
```

---

## 5. Roteiro e Sincronismo para Narração em Vídeo

| Tempo | Tela | Fala sugerida para narração / locução |
| :--- | :--- | :--- |
| **00:00 – 00:03** | Tela 01 (Gancho) | *"Meu filho completou 1 ano e ainda não fala nenhuma palavra. Devo me preocupar?"* |
| **00:03 – 00:08** | Tela 02 (Validação) | *"Essa é uma das perguntas mais comuns no meu consultório. E faz todo sentido você se perguntar isso."* |
| **00:08 – 00:25** | Tela 03 (O que esperar) | *"Aos 12 meses, a comunicação aparece antes nos gestos: dar tchau, apontar o que quer, atender pelo nome e entender o 'não'. As primeiras palavras com sentido costumam surgir entre os 12 e 15 meses."* |
| **00:25 – 00:40** | Tela 04 (Sinais de alerta) | *"Mas vale conversar com o pediatra ou fono se aos 12 meses o bebê não usar nenhum gesto social, ou se aos 18 meses ainda falar menos de 6 palavras. Avaliar cedo abre caminhos."* |
| **00:40 – 00:45** | Tela 05 (Fechamento) | *"Salve esse vídeo para acompanhar o desenvolvimento ou compartilhe com quem precisa dessa orientação."* |

---

## 6. Legenda e Hashtags para o Instagram

```text
Meu filho tem 1 ano e ainda não fala nenhuma palavra — é normal?

Essa é uma das dúvidas mais frequentes nas primeiras consultas, e é natural se perguntar isso.

Por volta de 1 ano, o que costuma acontecer não são palavras completas, mas gestos como o "tchau", o ato de apontar para mostrar interesse, o reconhecimento do próprio nome e o entendimento de comandos simples como o "não".

Entre os 12 e 15 meses, é esperado que a criança já tente uma ou duas palavras além de "mamãe" e "papai", e explore sons com entonação de conversa.

Quando buscar orientação?
Vale conversar com o pediatra ou com uma fonoaudióloga se:
• Aos 12 meses a criança não fizer gestos sociais nem responder ao chamado;
• Aos 15 meses não balbuciar ou não interagir com o ambiente;
• Aos 18 meses ainda falar menos de 6 palavras com sentido.

Avaliar cedo não é rotular: é oferecer o estímulo adequado no tempo certo.

Salve este vídeo para consultar quando precisar e compartilhe com uma família!

Sônia Torres · Fonoaudióloga · CRFa 1-17701
@torresdafono

Fontes: Sociedade Brasileira de Pediatria (SBP) / Caderneta da Criança (Ministério da Saúde)
Conteúdo educativo. Não substitui avaliação individualizada.

#fonoaudiologia #desenvolvimentoinfantil #atrasodafala #fonopediatrica #primeirosanos #maternidadereal #paternidadeativa #desenvolvimentodalinguagem #vicentedecarvalho
```

---

## 7. Como Manter e Re-renderizar

Para alterar textos, cores, badges ou atualizar fotos:
1. Abra o arquivo [scripts/gerar_telas_reel_01_um_ano.py](file:///c:/Users/Gamer/OneDrive/Documentos/Materiais-Sonia/scripts/gerar_telas_reel_01_um_ano.py).
2. Edite os textos na lista `screens_data`.
3. No terminal, execute:
   ```powershell
   python scripts/gerar_telas_reel_01_um_ano.py
   ```
4. Os arquivos individuais em `telas-finais/` e a `prancha-visao-geral.png` serão regerados de forma determinística e imediata.
