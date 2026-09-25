# Guia do Destaque Instagram "Quem é" — Sônia Torres

Este documento fornece as especificações completas de arquitetura, fluxo de produção, diretrizes visuais e guia de manutenção para o conjunto de Stories e Capa do Destaque **"Quem é"** no perfil do Instagram de **Sônia Torres (Fonoaudióloga, CRFa 1-17701)**.

---

## 1. Visão Geral e Objetivo
O Destaque "Quem é" é o ponto de contato inicial mais estratégico para novos visitantes que chegam ao perfil profissional (@torresdafono / sonia.fonosuite.com). 
O objetivo deste conjunto é estabelecer:
- **Acolhimento e calor humano:** Apresentar Sônia com sua fotografia real, sem artificialismo.
- **Credibilidade e autoridade ética:** Destacar sua sólida formação pela Universidade Federal do Rio de Janeiro (UFRJ) e seu registro profissional (CRFa 1-17701).
- **Abordagem clínica individualizada:** Explicar a metodologia focada na escuta atenta, avaliação diagnóstica e cuidado personalizado.
- **Clareza de atuação:** Informar que o atendimento contempla diferentes fases da vida (Crianças, Adultos e Idosos).
- **Próximo passo sem fricção:** Convidar a visitar os outros destaques ou acessar o site institucional sonia.fonosuite.com com espaço reservado para sticker de link.

---

## 2. Arquitetura e Especificações Técnicas

### 2.1 Dimensões e Proporções
- **Stories (01 a 05):** 1080 × 1920 px (proporção 9:16 vertical).
- **Capa Quadrada:** 1080 × 1080 px (1:1) com diâmetro central seguro de 700 px para o recorte circular do Instagram.
- **Capa Versão Story:** 1080 × 1920 px com elemento circular centralizado em Y = 960 px.
- **Prancha de Visão Geral:** 3000 × 1088 px para conferência editorial e aprovação.

### 2.2 Zonas de Segurança (Safe Zones)
- **Margem Superior Segura:** 220 px livres no topo (protege contra a barra de status do celular, contagem de tempo de stories e dados de perfil do Instagram).
- **Margem Inferior Segura:** 260 px livres na base (protege contra o campo nativo de resposta "Enviar mensagem", botão de curtir e compartilhar).
- **Margens Laterais:** Mínimo de 70 px de respiro.

### 2.3 Paleta Cromática
| Token | Cor Hex | RGB | Aplicação |
|---|---|---|---|
| `COLOR_DEEP_GREEN` | `#1D382B` | `(29, 56, 43)` | Verde Petróleo Profundo: Títulos principais, fundos de cartões institucionais e capa |
| `COLOR_OLIVE` | `#44634B` | `(68, 99, 75)` | Verde Oliva Clínico: Subtítulos, linhas de destaque e tags secundárias |
| `COLOR_OFFWHITE` | `#FAF7F2` | `(250, 247, 242)` | Creme Acolhedor: Fundo geral dos Stories e elementos da Capa |
| `COLOR_CARD` | `#F4EFE8` | `(244, 239, 232)` | Bege Claro: Cartões de apoio, slot do sticker e citações |
| `COLOR_CHARCOAL` | `#2E2C29` | `(46, 44, 41)` | Grafite Suave: Corpo de texto editorial com alto contraste sem agressividade |
| `COLOR_MUTED` | `#706B64` | `(112, 107, 100)` | Cinza Neutro: Rótulos de instrução e legendas |
| `COLOR_BORDER` | `#E2DBD0` | `(226, 219, 208)` | Areia Divisório: Linhas e contornos sutis de cartões |

### 2.4 Tipografia
- Família: **Plus Jakarta Sans** (`PlusJakartaSans-Variable.ttf`).
- Títulos: 68px a 76px (Bold 700 / SemiBold 600).
- Subtítulos: 38px a 44px (SemiBold 600 / Medium 500).
- Corpo de texto: 34px a 38px (Regular 400), entrelinha de 46px a 56px.
- Tags e pílulas: 24px a 26px (Bold 700, caixa alta).

---

## 3. Estrutura dos Arquivos e Fluxo de Dados

```
1MATERIASIDASONIA/
├── assets/
│   ├── fonts/
│   │   └── PlusJakartaSans-Variable.ttf
│   ├── destaque-quem-e/
│   │   ├── story_01_apresentacao.png   (Story 01 - 1080x1920)
│   │   ├── story_02_formacao.png       (Story 02 - 1080x1920)
│   │   ├── story_03_forma_trabalho.png (Story 03 - 1080x1920)
│   │   ├── story_04_quem_atende.png    (Story 04 - 1080x1920)
│   │   ├── story_05_chamada_final.png  (Story 05 - 1080x1920)
│   │   ├── capa_destaque_quem_e.png    (Capa 1080x1080)
│   │   ├── capa_destaque_quem_e_story.png (Capa Story 1080x1920)
│   │   ├── prancha_visao_geral.png     (Prancha de Aprovação)
│   │   ├── consultorio_respiro.jpg     (Foto de apoio consultório)
│   │   └── registro_clinico_maos.jpg   (Foto de apoio avaliação)
│   └── sonia_pao_de_acucar.jpeg        (Fotografia real de Sônia Torres)
├── docs/
│   ├── destaque-quem-e-planejamento.md
│   └── destaque-quem-e-guia.md
├── prompts/
│   └── destaque-quem-e-prompts.md
└── scripts/
    └── gerar_destaque_quem_e.py
```

### Fluxo de Dados:
1. `sonia_pao_de_acucar.jpeg` + `POST.png` + `registro_clinico_maos.jpg` fornecem a base visual autêntica sem distorção.
2. `gerar_destaque_quem_e.py` carrega fontes vetoriais, calcula quebras de linha automáticas e ajusta a proporção via `ImageOps.fit`.
3. O script exporta os 5 Stories PNG e as 2 versões da Capa na pasta `assets/destaque-quem-e/`.
4. Uma prancha comparativa (`prancha_visao_geral.png`) é gerada em lote para validação visual.

---

## 4. Conteúdo Detalhado por Tela

### Story 01 — Apresentação
- **Fotografia:** Retrato autêntico de Sônia Torres com jaleco clínico bordado e Pão de Açúcar ao fundo no Rio de Janeiro.
- **Hierarquia:**
  - Badge: `CRFa 1-17701`
  - Nome: **Sônia Torres**
  - Profissão: *Fonoaudióloga*
  - Mensagem: *"Comunicação, desenvolvimento e cuidado em diferentes fases da vida."*

### Story 02 — Formação
- **Fotografia:** Detalhe de Sônia em contexto profissional com foco no jaleco e sorriso acolhedor.
- **Hierarquia:**
  - Tag: `TRAJETÓRIA PROFISSIONAL`
  - Título: **Minha formação**
  - Instituição: *"Sou fonoaudióloga formada pela Universidade Federal do Rio de Janeiro — UFRJ."*
  - Citação: *"A Fonoaudiologia me permite trabalhar com algo essencial: a comunicação humana."*

### Story 03 — Forma de Trabalho
- **Fotografia:** Mãos em registro clínico com prancheta de avaliação individualizada e blocos terapêuticos.
- **Hierarquia:**
  - Tag: `MÉTODO E CUIDADO`
  - Título: **Cada pessoa é diferente.**
  - Metodologia: *"Por isso, o atendimento começa pela escuta, pela avaliação e pela compreensão das necessidades de cada pessoa e de sua família."*
  - Destaque: *"A partir daí, o cuidado é individualizado."*

### Story 04 — Quem Atende
- **Fotografia:** Família multigeracional interagindo com naturalidade (leitura e blocos lúdicos).
- **Hierarquia:**
  - Tag: `PÚBLICO E ATUAÇÃO`
  - Título: **Atendimento fonoaudiológico**
  - Três pílulas de público: `Crianças` • `Adultos` • `Idosos`
  - Escopo: *"Com atenção às necessidades de comunicação, fala, linguagem e outras demandas fonoaudiológicas."*

### Story 05 — Chamada Final
- **Hierarquia:**
  - Tag: `PRÓXIMO PASSO`
  - Título: **Quer saber como posso ajudar?**
  - Texto de acolhimento: *"Conheça os outros destaques ou entre em contato comigo."*
  - **Slot Interativo do Sticker:**
    - Indicador de Link com ícone de elos e URL `sonia.fonosuite.com`.
    - Guia para sobreposição do sticker de Link no app do Instagram.
  - Cartão de Contato Oficial:
    - **Sônia Torres**
    - *Fonoaudióloga | CRFa 1-17701*
    - Endereço oficial: *sonia.fonosuite.com*

### Capa do Destaque — "Quem é"
- Fundo em Verde Petróleo Profundo (`#1D382B`).
- Ícone minimalista vetorial de perfil humano em Creme Acolhedor (`#FAF7F2`).
- Tipografia: **Quem é** em 92px bold.
- Círculo de segurança calibrado para o recorte circular do Instagram (diâmetro de 680-800 px).

---

## 5. Como Manter e Regerar o Conjunto
Para atualizar textos ou trocar imagens de fundo no futuro:
1. Abra o arquivo [gerar_destaque_quem_e.py](file:///c:/Users/Gamer/OneDrive/Documentos/1MATERIASIDASONIA/scripts/gerar_destaque_quem_e.py).
2. Altere os textos ou caminhos das imagens nas funções `generate_story_01` até `generate_story_05`.
3. Execute o comando no terminal:
   ```powershell
   python scripts/gerar_destaque_quem_e.py
   ```
4. As novas imagens serão geradas automaticamente na pasta `assets/destaque-quem-e/`.
