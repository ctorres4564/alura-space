# Documentação Técnica: Carrossel "O que esperar da fala, por idade"

Material fonoaudiológico institucional desenvolvido para a fonoaudióloga **Sônia Torres (CRFa 1-17701)**.

---

## 1. Objetivo
Produzir uma peça educativa de alto impacto e sensibilidade para o Instagram (Carrossel 4:5, 1080 × 1350 px, 10 lâminas), orientando pais, mães e cuidadores sobre os marcos normativos do desenvolvimento da fala infantil do nascimento aos 6 anos de idade, baseando-se em diretrizes da Sociedade Brasileira de Pediatria (SBP) e do Center for Disease Control and Prevention (CDC).

---

## 2. Identidade Visual e Diretrizes Éticas
- **Paleta de Cores**:
  - Bege de fundo institucional: `#FAF7F2` (RGB 250, 247, 242)
  - Verde escuro principal (títulos e ênfase): `#1D382B` (RGB 29, 56, 43)
  - Verde médio complementar (badges, destaques e moldura): `#44634B` (RGB 68, 99, 75)
  - Bege suave para contrastes e botões de ação: `#EAE4D8` (RGB 234, 228, 216)
- **Tipografia**: `Plus Jakarta Sans` (pesos 500, 700 e 800), carregada a partir de `assets/fonts/PlusJakartaSans-Variable.ttf`.
- **Safe Zone do Feed do Instagram**:
  - Dimensão total do slide: 1080 × 1350 px (4:5).
  - Zona crítica central (feed 1:1): Y entre 135 px e 1215 px.
  - Todos os títulos, caixas de texto e elementos de leitura foram estritamente diagramados dentro da zona segura para não sofrer cortes na visualização em grade do perfil.
- **Privacidade e Proteção à Criança**:
  - **Zero pacientes reais e zero rostos infantis reconhecíveis**.
  - Enquadramentos em planos detalhe (mãos, gestos), visão de costas, nuca ou desfoque de profundidade de campo suave (bokeh óptico simulando 35mm f/2.8).
- **Diversidade Étnico-Racial e de Gênero**:
  - Imagens contemplando a diversidade brasileira: bebês e cuidadores negros, pardos, brancos, com cabelos crespos, cacheados e lisos; presença equilibrada de figuras maternas e paternas nos cuidados e interações diárias.

---

## 3. Arquitetura de Arquivos

```
Materiais-Sonia/
├── carrosseis/
│   └── carrossel-o-que-esperar-da-fala-por-idade/
│       ├── raw-photos/              # 8 fotografias documentais na proporção 4:5
│       ├── slides-finais/           # 10 slides finais prontos em 1080x1350 px (PNG)
│       │   ├── 01-capa.png
│       │   ├── 02-0-a-6-meses.png
│       │   ├── 03-7-a-11-meses.png
│       │   ├── 04-1-ano.png
│       │   ├── 05-1-ano-e-6-meses.png
│       │   ├── 06-2-anos.png
│       │   ├── 07-3-a-6-anos.png
│       │   ├── 08-observe-alertas.png
│       │   ├── 09-slide-resumo.png
│       │   └── 10-encerramento.png
│       └── conteudo-publicacao.md   # Textos completos de cada lâmina e legenda para o Instagram
├── prompts/
│   └── carrossel-o-que-esperar-da-fala-por-idade-prompts.md # Especificação dos 10 prompts
├── scripts/
│   └── gerar_carrossel_o_que_esperar_da_fala_por_idade.py   # Script de automação e renderização gráfica
└── docs/
    └── carrossel-o-que-esperar-da-fala-por-idade.md         # Esta documentação técnica
```

---

## 4. Fluxo de Dados e Pipeline de Renderização

1. **Definição dos Prompts**:
   - Registro em `prompts/carrossel-o-que-esperar-da-fala-por-idade-prompts.md` com os campos obrigatórios `[Tema]`, `[Ângulo de Câmera]`, `[Iluminação]`, `[Lente/Equipamento]` e prompts fotográficos em inglês.
2. **Preparação das Fotos Documentais**:
   - As imagens fotográficas são ajustadas e cortadas pelo script para 1080 × 1350 px via filtro Lanczos em `raw-photos/`.
3. **Composição Editorial com Pillow**:
   - O script `gerar_carrossel_o_que_esperar_da_fala_por_idade.py` desenha cards em camadas com sombra difusa, badges estilizados, linhas de respiro e quebra dinâmica de texto por largura em pixels (`wrap_text_to_width`).
4. **Exportação Final**:
   - Os 10 slides são exportados em formato PNG de alta fidelidade cromática para `slides-finais/`.

---

## 5. Como Manter e Reexecutar
Para reprocessar os slides após alterações de texto ou estilo:

```powershell
python scripts/gerar_carrossel_o_que_esperar_da_fala_por_idade.py
```

O script é idempotente, recria a pasta de destino caso necessário e imprime o progresso de cada lâmina no terminal.
