# Documentação Técnica — Carrossel "O que anotar antes da consulta"

**Peça:** Carrossel de Lista (4:5 · 1080×1350 px · 9 slides)  
**Cliente:** Sônia Torres · Fonoaudióloga (CRFa 1-17701)  
**Linha Editorial:** Infantil / Família / Observação da Comunicação Infantil  
**Diretório do Material:** `avulsos/carrossel-lista-anotar-antes-da-consulta/`  

---

## 1. Objetivo

Fornecer aos pais e familiares de crianças (com foco em comunicação no espectro autista e atrasos de linguagem) um roteiro prático e acolhedor do que observar e registrar no dia a dia para levar à consulta fonoaudiológica, neuropediátrica ou pediátrica.

A peça segue rigorosamente os princípios éticos do Código de Ética da Fonoaudiologia (Resolução CFFa nº 640/2021) e as diretrizes do consultório da Dra. Sônia Torres:
- **Não é autoteste:** sem pontuação, sem soma de respostas, sem dizer "se marcar X seu filho é autista".
- **Sem exposição de pacientes:** fotografia puramente documental com enquadramento em mãos, ambiente acolhedor e objetos do cotidiano infantil, sem exibir rostos.
- **Linguagem descritiva:** foco em situações observáveis do dia a dia (o quê, quando, com quem e onde).

---

## 2. Arquitetura do Sistema e Componentes

A geração do material é composta por 3 pilares modulares e desacoplados:

```
├── prompts/
│   └── carrossel-anotar-antes-consulta-prompts.md   <- Especificações de prompts fotográficos
├── scripts/
│   └── gerar_carrossel_anotar_antes_consulta.py    <- Motor autônomo de renderização gráfica
└── avulsos/carrossel-lista-anotar-antes-da-consulta/
    ├── carrossel-lista-02-anotar-antes-consulta.md <- Briefing original aprovado
    ├── conteudo-publicacao.md                      <- Pacote de publicação com legenda e copy
    ├── preview-grade.jpg                           <- Folha de contato / prancha 3x3 dos slides
    ├── raw-photos/                                 <- Fotografias originais de alta fidelidade
    │   ├── 01-capa.jpg
    │   ├── 03-atencao.jpg
    │   ├── 04-resposta-nome.jpg
    │   ├── 05-formas-pedir.jpg
    │   ├── 06-brincadeira.jpg
    │   ├── 07-sensorial.jpg
    │   └── 09-encerramento.jpg
    └── slides-finais/                              <- Slides finais em PNG 1080x1350 px
        ├── 01-capa.png
        ├── 02-contexto.png
        ├── 03-area-1-atencao-compartilhada.png
        ├── 04-area-2-resposta-ao-nome.png
        ├── 05-area-3-formas-de-pedir.png
        ├── 06-area-4-brincadeira-e-imitacao.png
        ├── 07-area-5-contexto-sensorial.png
        ├── 08-roteiro-de-anotacao.png
        └── 09-encerramento.png
```

---

## 3. Fluxo de Dados e Renderização

1. **Ingestão Fotográfica:**
   As fotos geradas são copiadas do cache do motor de geração para a pasta local `raw-photos/`.
2. **Processamento Geométrico:**
   Cada fotografia passa pelo processo `cover_crop` para centralização de assunto, redimensionamento proporcional Lanczos e recorte para área útil exata.
3. **Composição Tipográfica:**
   Utilização da fonte oficial *Plus Jakarta Sans Variable*, com hierarquia estabelecida:
   - Títulos de Capa e Seções: Pesos 800 (ExtraBold) e 700 (Bold).
   - Textos de Apoio e Perguntas: Peso 500 (Medium) com entrelinha calibrada para leitura mobile.
   - Metadados e Badges: Pílulas arredondadas com preenchimento nas cores oficiais `#EAE4D8` (Bege Escuro), `#1D382B` (Verde Petróleo Profundo) e `#44634B` (Verde Oliva).
4. **Controle de Contraste e Acessibilidade:**
   - Slide 02 (Contexto): Card off-white `#FFFFFF` sobre fundo `#FAF7F2` com bordas suaves `#E2DBD0`.
   - Slide 08 (Resumo de Bolso): Fundo escuro `#1D382B` com cartões de alto contraste, otimizado para prints de tela em smartphones.
5. **Compilação de Prancha:**
   Todos os 9 slides renderizados são agregados em uma grade 3x3 (`preview-grade.jpg`) com espaçamento balanceado para avaliação rápida.

---

## 4. Como Manter e Reexecutar

Para regerar os slides ou alterar qualquer texto/parâmetro visual:

1. Edite os textos ou configurações no script:
   `scripts/gerar_carrossel_anotar_antes_consulta.py`
2. Execute o script no terminal:
   ```bash
   python scripts/gerar_carrossel_anotar_antes_consulta.py
   ```
3. Os arquivos em `slides-finais/` e a imagem `preview-grade.jpg` serão atualizados instantaneamente.
