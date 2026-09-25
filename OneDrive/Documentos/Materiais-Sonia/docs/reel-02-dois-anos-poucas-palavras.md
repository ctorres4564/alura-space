# Documentação Técnica e Editorial: Reel 02 — Fala aos 2 Anos (24 Meses)

**Série Educativa para Redes Sociais**  
**Profissional:** Sônia Torres · Fonoaudióloga · CRFa 1-17701 · `@torresdafono`  
**Peça:** Reel 02 — *"Meu filho tem 2 anos e fala poucas palavras. É normal?"*  
**Formato:** Reel vertical 9:16 (1080 × 1920 pixels) — 5 telas  
**Duração estimada:** 45 segundos  
**Localização dos Arquivos:** `reels/reel-02-dois-anos-poucas-palavras/`

---

## 1. Objetivo da Publicação

Orientar pais, familiares e cuidadores sobre o desenvolvimento típico da linguagem e da fala por volta dos 24 meses (2 anos de idade), respondendo à angústia comum gerada por comparações entre crianças da mesma idade.

A publicação desempenha três papéis clínicos essenciais:
1. **Validação Afetiva:** Reconhecer que a dúvida é legítima e comum, acolhendo a família sem tom punitivo ou alarmista.
2. **Critérios Objetivos da Fase:** Apresentar marcos esperados para a maioria das crianças de 2 anos (vocabulário funcional de ~50 palavras e combinação de 2 palavras com significado, como "dá água", "olha o carro").
3. **Encaminhamento Ético:** Indicar quando vale a pena buscar avaliação profissional, desmistificando o mito de "esperar até os 4 anos" e demonstrando que avaliar cedo potencializa o desenvolvimento infantil.

---

## 2. Rigor Científico e Conformidade Ética

### 2.1 Fontes Técnicas
- **Sociedade Brasileira de Pediatria (SBP) / CDC — Checklists de Desenvolvimento (2024/2025)**: Marcos consolidados para 24 meses (imitação de sons/palavras, combinação de termos e compreensão de comandos compostos).
- **Caderneta da Criança (Edição 2025/2026, Ministério da Saúde)**: Instrumento orientador nacional utilizado por pediatras e famílias brasileiras.
- **Código de Ética da Fonoaudiologia (Resolução CFFa nº 640/2021) e Guia de Mídias Sociais (CFFa nº 756/2024)**:
  - Linguagem estritamente orientadora ("sinais para conversar com a fono"), sem formulação de diagnóstico pela internet.
  - Identificação profissional obrigatória (*Sônia Torres · Fonoaudióloga · CRFa 1-17701*).
  - Total privacidade dos menores: nenhuma criança identificável; apenas enquadramentos dorsais, detalhes em mãos e brinquedos educativos.

---

## 3. Arquitetura do Sistema Visual

As peças seguem o padrão gráfico de alto contraste e conformidade com a **Safe Zone do Instagram Reels (1080 × 1920 px)**:

```
                  SAFE ZONE INSTAGRAM REELS (1080 × 1920 px)
  ┌────────────────────────────────────────────────────────────────────────┐
  │  Y: 0 – 240 px      Área Superior Protegida (Status bar, busca, perfil) │
  ├────────────────────────────────────────────────────────────────────────┤
  │                                                                        │
  │  Y: 260 – 1560 px   ÁREA ÚTIL EDITORIAL (LIVRE DE BOTÕES E LEGENDAS)   │
  │                     - Pill Badge temática superior                     │
  │                     - Card translúcido escuro (#13241B)                │
  │                     - Borda suave em Verde Oliva (#547A5F)             │
  │                     - Tipografia editorial (Segoe UI / Arial)          │
  │                     - Fotografia documental brasileira de fundo        │
  │                                                                        │
  ├────────────────────────────────────────────────────────────────────────┤
  │  Y: 1600 – 1920 px  Área Inferior Protegida (Legenda nativa e áudio)   │
  └────────────────────────────────────────────────────────────────────────┘
```

- **Paleta Cromática:**
  - Base do Card: `#13241B` (Verde Petróleo Profundo com 89% de opacidade)
  - Borda do Card: `#547A5F` (Verde Oliva Suave, 2px)
  - Badge Superior: `#F0EBE0` (Creme Suave) com texto `#193024`
  - Destaques / Pontos de Alerta: `#F5A882` (Terracota Acolhedor)
  - Tipografia Principal: Branco Puro (`#FFFFFF`) e Branco Sálvia (`#E1E8E2`)
- **Fotografia:** Cenas autênticas da rotina brasileira (piso de taco tradicional, brinquedos de madeira com fauna e flora nacionais, interação pai-filho acolhedora e retrato profissional oficial).

---

## 4. Estrutura de Diretórios e Arquivos

```
Materiais-Sonia/
├── prompts/
│   └── reel-02-dois-anos-poucas-palavras-prompts.md   # Catálogo de prompts detalhados
├── scripts/
│   └── gerar_telas_reel_02_dois_anos.py              # Script de renderização Pillow
├── docs/
│   └── reel-02-dois-anos-poucas-palavras.md          # Esta documentação técnica
└── reels/
    └── reel-02-dois-anos-poucas-palavras/
        ├── raw-photos/                               # Fotos originais puras
        │   ├── 01-gancho.jpg
        │   ├── 02-validacao.jpg
        │   ├── 03-o-que-esperar.jpg
        │   ├── 04-quando-avaliar.jpg
        │   └── 05-fechamento.jpg
        ├── fotografias-sem-texto/                    # Imagens 1080x1920 limpas para Canva/CapCut
        │   ├── 01-gancho-sem-texto.png ... 05-fechamento-sem-texto.png
        └── telas-finais/                             # Telas finalizadas com tipografia
            ├── 01-gancho.png
            ├── 02-validacao.png
            ├── 03-o-que-esperar.png
            ├── 04-quando-avaliar.png
            ├── 05-fechamento.png
            └── prancha-visao-geral.png               # Painel panorâmico comparativo
```

---

## 5. Roteiro e Sincronismo para Narração em Vídeo

| Tempo | Tela | Roteiro de Fala Sugerido (45 segundos) |
| :--- | :--- | :--- |
| **00:00 – 00:03** | Tela 01 (Gancho) | *"Meu filho completou 2 anos e fala poucas palavras. Isso é normal?"* |
| **00:03 – 00:08** | Tela 02 (Validação) | *"Essa é uma das maiores angústias dos pais no consultório, principalmente quando começam a comparar com outras crianças da mesma idade."* |
| **00:08 – 00:25** | Tela 03 (O que esperar) | *"Por volta dos 2 anos, a maioria das crianças já junte pelo menos duas palavras com sentido — como 'dá água' ou 'olha o carro' —, tem um vocabulário ativo em torno de 50 palavras e aponta para o que quer."* |
| **00:25 – 00:40** | Tela 04 (Quando avaliar) | *"Vale buscar uma avaliação se aos 24 meses seu filho ainda falar menos de 50 palavras, não combinar dois termos ou preferir puxar você pela mão em vez de tentar falar ou gesticular."* |
| **00:40 – 00:45** | Tela 05 (Fechamento) | *"Buscar orientação cedo não é rotular: é estimular com carinho e precisão. Salve este vídeo ou envie para quem precisa dessa clareza."* |

---

## 6. Legenda Pronta para o Instagram

```text
Meu filho tem 2 anos e fala poucas palavras — é normal?

Essa é uma das perguntas mais frequentes que recebo de pais aflitos no consultório. E comparar com coleguinhas da mesma idade costuma gerar muita angústia.

Cada criança tem seu tempo, mas aos 24 meses existem marcos de desenvolvimento bem consolidados. Nessa fase, o esperado para a maioria das crianças é:
• Juntar ao menos duas palavras com significado próprio ("quero água", "olha o cão");
• Ter um vocabulário ativo em torno de 50 palavras ou mais;
• Apontar para partes do corpo e objetos conhecidos quando estimulado;
• Compreender comandos simples de rotina e usar gestos expressivos.

Quando vale a pena buscar uma fonoaudióloga?
• Se a criança ainda não combina duas palavras para expressar desejos;
• Se fala significativamente menos de 50 palavras;
• Se prefere puxar a mão do adulto em vez de vocalizar ou usar gestos sociais;
• Se tem dificuldade para compreender ordens simples do dia a dia.

Esperar "o tempo da criança" não significa deixar passar sinais de que ela precisa de apoio. Avaliar cedo é abrir caminhos!

Salve este vídeo para acompanhar o desenvolvimento do seu filho e compartilhe com uma família!

Sônia Torres · Fonoaudióloga · CRFa 1-17701
@torresdafono

Fontes: Sociedade Brasileira de Pediatria (SBP) / Caderneta da Criança (Ministério da Saúde)
Conteúdo educativo. Não substitui avaliação individualizada.

#fonoaudiologia #desenvolvimentoinfantil #atrasodefala #linguageminfantil #fonopediatrica #doisoutresanos #maternidadereal #paternidadeativa #primeirainfancia #vicentedecarvalho
```

---

## 7. Como Manter e Re-renderizar

Para alterar textos, cores ou atualizar fotos:
1. Abra o arquivo [scripts/gerar_telas_reel_02_dois_anos.py](file:///c:/Users/Gamer/OneDrive/Documentos/Materiais-Sonia/scripts/gerar_telas_reel_02_dois_anos.py).
2. Edite os textos na lista `screens_data`.
3. No terminal, execute:
   ```powershell
   python scripts/gerar_telas_reel_02_dois_anos.py
   ```
4. Os arquivos individuais em `telas-finais/` e a `prancha-visao-geral.png` serão regerados de forma determinística e imediata.
