# Guia de Publicação — Carrossel "Fala aos 2 Anos: Checklist"

**Autora/Especialista**: Sônia Torres · Fonoaudióloga · CRFa 1-17701  
**Formato**: Carrossel Instagram (10 cards verticais 4:5 — 1080 × 1350 px)  
**Status**: Concluído e pronto para publicação

---

## 1. Objetivo
Apresentar às famílias e cuidadores os 6 principais marcos do desenvolvimento comunicativo e de linguagem aos 2 anos de idade em formato interativo de checklist. O material visa informar com base científica e afetiva, combater o mito do "esperar crescer", valorizar a diversidade étnica brasileira e orientar quando buscar avaliação especializada.

---

## 2. Arquitetura e Identidade Visual

### 2.1 Especificações Técnicas
- **Dimensões**: 1080 × 1350 pixels (Aspect Ratio 4:5 Portrait).
- **Tipografia**: *Plus Jakarta Sans* (pesos 400, 500, 600, 700, 800) via Google Fonts.
- **Paleta de Cores**:
  - Fundo principal: `#FAF7F2` (bege acolhedor, orgânico e clínico).
  - Texto principal / Destaque escuro: `#1D382B` (verde floresta profundo institucional).
  - Texto secundário / Detalhes: `#44634B` (verde oliva suave).
  - Linhas divisórias: `#DDD5C6`.
  - Slide de alerta (Card 08): Fundo escuro `#1D382B` com textos em `#FAF7F2` e `#C9D6C6`.

### 2.2 Estrutura de Diretórios
```text
carrossel-lista-01-fala-2-anos/
├── assets/                  # Imagens fotográficas de alta resolução dos slides
│   ├── slide-01.jpg
│   ├── slide-02.jpg
│   ├── slide-03.jpg
│   ├── slide-04.jpg
│   ├── slide-05.jpg
│   ├── slide-06.jpg
│   ├── slide-07.jpg
│   └── slide-10.jpg
├── cards-publicacao/        # 10 imagens PNG (1080x1350) prontas para publicação
│   ├── slide-01.png
│   ├── slide-02.png
│   ├── ...
│   └── slide-10.png
├── docs/                    # Documentação do projeto
│   └── carrossel-fala-2-anos-guia.md
├── prompts/                 # Referência completa dos prompts com regras
│   └── prompts-imagens-carrossel.md
├── scripts/                 # Automação de assets e renderização
│   ├── setup_assets.py
│   └── render_cards.py
├── templates-editaveis/     # Arquivos HTML editáveis individuais (1 a 10)
│   ├── slide-01.html
│   ├── ...
│   └── slide-10.html
└── preview.html             # Prancha com visualização completa dos 10 slides
```

---

## 3. Fluxo de Leitura e Diversidade Representada

1. **Card 01 (Capa)**: Chamada de atenção e engajamento ("Seu filho tem 2 anos? Marque o que ele já faz"). Mãos de criança afro-brasileira marcando checklist com apoio materno.
2. **Card 02 (Item 01)**: "Junta duas palavras" (ex: "quero água"). Criança parda brasileira em momento espontâneo pedindo água.
3. **Card 03 (Item 02)**: "Fala mais de 50 palavras" (Vocabulário). Flatlay de objetos cotidianos com criança nipo-brasileira brincando.
4. **Card 04 (Item 03)**: "Aponta partes do corpo" (Pelo menos duas). Criança negra apontando para o próprio pezinho descalço.
5. **Card 05 (Item 04)**: "Usa mais gestos" (Comunicação ampliada). Menino indígena brasileiro gesticulando com adulto agachado à altura dos olhos.
6. **Card 06 (Item 05)**: "Chama a si mesmo pelo nome" (Autorreconhecimento). Criança diante de espelho baixo se reconhecendo.
7. **Card 07 (Item 06)**: "Reconhece figuras nos livros" (5 a 10 figuras). Leitura compartilhada com dedinho apontando o animalzinho no livro infantil.
8. **Card 08 (Alerta Clínico)**: "Quando procurar avaliação" (Fundo verde floresta com contraste acolhedor).
9. **Card 09 (Resumo do Checklist)**: Lista consolidada de conferência rápida com botão de salvamento.
10. **Card 10 (Fechamento & CTA)**: Conclusão afetuosa e direcionamento para o link da bio. Mãos de adulto e criança entrelaçadas.

---

## 4. Como Manter e Re-exportar

Para atualizar textos ou imagens e gerar novamente os arquivos finais de publicação:
1. Edite os arquivos HTML em `templates-editaveis/`.
2. Se trocar imagens, adicione-as em `assets/` mantendo as dimensões proporcionais.
3. Execute o script de renderização no terminal:
   ```bash
   python scripts/render_cards.py
   ```
4. As 10 imagens serão re-geradas automaticamente em `cards-publicacao/`.
