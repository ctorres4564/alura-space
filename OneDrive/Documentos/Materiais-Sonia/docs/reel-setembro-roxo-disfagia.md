# Documentação Técnica — Reel: Setembro Roxo (Conscientização sobre Disfagia)

Este documento descreve a arquitetura, o fluxo de dados, as decisões de design e o guia de manutenção para os **3 slides intermediários** do Reel sobre o **Setembro Roxo**, campanha de conscientização sobre disfagia conduzida pela fonoaudióloga **Sônia Torres (CRFa 1-17701)**.

---

## 1. Objetivo do Projeto

Produzir três peças visuais verticais para Instagram Reel (1080 × 1920 px, 9:16) destinadas a serem inseridas entre dois vídeos falados da fonoaudióloga Sônia Torres:
1. **Vídeo inicial da Sônia** (~10 segundos);
2. **Slide 1 — Apresentação** (~5 a 6 segundos);
3. **Slide 2 — Sinais de Alerta** (~5 a 6 segundos);
4. **Slide 3 — Ação, Acolhimento e Assinatura** (~5 a 6 segundos);
5. **Vídeo final da Sônia** (~10 segundos).

### Princípios Visuais
- **Fotografia Documental Brasileira**: Estética observacional e calorosa inspirada em câmeras full-frame profissionais (Sony A7 IV e Canon EOS R6 Mark II com lentes 35mm e 50mm f/1.8).
- **Sem Sensacionalismo**: Foco na dignidade da pessoa idosa, sem representações de aflição, asfixia, emergência ou mãos na garganta.
- **Roxo na Medida Certa**: Utilizado em elementos gráficos sutis (badges, marcadores e linhas), sem banhar a cena com filtros roxos artificiais ou tingir a pele.
- **Respeito Estrito à Safe Zone**: Tipografia concentrada na área central segura para evitar sobreposição com ícones laterais do Instagram, tarja superior de status e controles inferiores (áudio, legenda e perfil).

---

## 2. Estrutura de Diretórios e Arquivos

```text
Materiais-Sonia/
├── reels/
│   └── reel-setembro-roxo-disfagia/
│       ├── 01-slide-apresentacao.png           # Slide 1 final diagramado
│       ├── 02-slide-sinais.png                 # Slide 2 final diagramado
│       ├── 03-slide-acao.png                   # Slide 3 final diagramado
│       └── fotografias-sem-texto/
│           ├── 01-slide-apresentacao-sem-texto.png
│           ├── 02-slide-sinais-sem-texto.png
│           └── 03-slide-acao-sem-texto.png
├── prompts/
│   └── reel-setembro-roxo-disfagia-prompts.md  # Referência completa dos prompts
├── scripts/
│   └── gerar_telas_reel_setembro_roxo.py       # Script gerador e diagramador
└── docs/
    └── reel-setembro-roxo-disfagia.md          # Esta documentação técnica
```

---

## 3. Arquitetura e Fluxo de Dados

O pipeline de criação segue a metodologia de separação estrita entre base fotográfica e camada tipográfica:

1. **Geração da Base Fotográfica (9:16)**:
   - Geração de fotografias sem texto com espaço negativo planejado no terço superior.
   - Preservação da imagem bruta de alta definição.

2. **Isolamento de Imagens Limpas**:
   - As imagens base são redimensionadas em alta precisão (LANCZOS) e arquivadas na pasta `fotografias-sem-texto/`. Isso permite reaproveitá-las no Canva, CapCut ou Premiere a qualquer momento.

3. **Composição Gráfica Automatizada via Python (Pillow)**:
   - Aplicação de gradiente sutil de proteção no terço superior (contraste perfeito sobre fundos claros).
   - Diagramação tipográfica com alinhamento óptico, hierarquia de pesos (Bold/Regular/Semibold) e sombras de contorno suaves.
   - Inserção dos detalhes temáticos em roxo (`#702C8E` e `#8E44AD`).
   - Inserção dos créditos profissionais protegidos no rodapé do Slide 3:
     * **Sônia Torres**
     * **Fonoaudióloga | CRFa 1-17701**

4. **Exportação**:
   - Saída em PNG de alta definição (1080 × 1920 px) pronta para ingestão direta no editor de vídeo.

---

## 4. Especificações Técnicas de Cada Slide

### Slide 1 — Apresentação
- **Imagem**: Idosa brasileira em café da manhã na cozinha, atmosfera acolhedora e reflexiva.
- **Badge**: `SETEMBRO ROXO` em cápsula roxa institucional nobre.
- **Título**: `Conscientização sobre disfagia`.
- **Texto complementar**: `Dificuldades para engolir podem afetar alimentação, hidratação e segurança.`

### Slide 2 — Sinais de Alerta
- **Imagem**: Senhor idoso brasileiro à mesa segurando copo de água, com refeição e familiar ao fundo.
- **Tag**: `SETEMBRO ROXO · DISFAGIA`.
- **Título**: `Alguns sinais merecem atenção`.
- **Lista com Marcadores Roxos**:
  - *Tosse ou engasgos ao comer ou beber*
  - *Voz molhada após engolir*
  - *Refeições muito demoradas*
  - *Dificuldade para engolir*

### Slide 3 — Ação e Fechamento
- **Imagem**: Consulta fonoaudiológica humanizada com escuta acolhedora, contato humano e segurança.
- **Título**: `Dificuldade para engolir não deve ser ignorada.`
- **Texto complementar**: `A avaliação adequada ajuda a identificar o que está acontecendo e orientar os cuidados necessários.`
- **Destaque**: `Informação também é cuidado.`
- **Rodapé / Assinatura**: `Sônia Torres | Fonoaudióloga | CRFa 1-17701`.

---

## 5. Diretrizes de Movimento para a Edição do Vídeo (Reel)

Para que os slides não pareçam congelados estaticamente durante os 5 a 6 segundos de cada um, recomenda-se aplicar movimentos ultra-sutis no CapCut, Premiere ou DaVinci Resolve:
- **Slide 1**: *Zoom-in* muito lento e contínuo (escala de 100% para 104% em 6s).
- **Slide 2**: Movimento de *pan* lateral quase imperceptível ou zoom progressivo suave (100% para 103%).
- **Slide 3**: *Zoom-out* muito suave (104% para 100% em 6s), conduzindo a atenção de volta ao vídeo final da fonoaudióloga.
- **Transições**: Evite cortes bruscos, flashes ou glitches; utilize *dissolve* suave (0.3s) ou corte seco elegante alinhado à fala.

---

## 6. Como Manter e Reexecutar

Caso necessite alterar textos, espaçamentos ou trocar qualquer imagem de base:
1. Abra o arquivo [`gerar_telas_reel_setembro_roxo.py`](file:///c:/Users/Gamer/OneDrive/Documentos/Materiais-Sonia/scripts/gerar_telas_reel_setembro_roxo.py);
2. Ajuste as variáveis de texto ou coordenadas nos métodos `render_slide_1`, `render_slide_2` ou `render_slide_3`;
3. Execute o script no terminal:
   ```bash
   python c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia\scripts\gerar_telas_reel_setembro_roxo.py
   ```
4. Os arquivos serão atualizados imediatamente na pasta [`reel-setembro-roxo-disfagia`](file:///c:/Users/Gamer/OneDrive/Documentos/Materiais-Sonia/reels/reel-setembro-roxo-disfagia).
