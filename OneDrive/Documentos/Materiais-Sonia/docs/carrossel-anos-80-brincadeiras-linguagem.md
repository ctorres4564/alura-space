# Documentação Técnica e Editorial: Carrossel "Coisas que uma criança dos anos 80 fazia sem saber que estava estimulando a linguagem"

**Perfil Profissional**: Sônia Torres · Fonoaudióloga · CRFa 1-17701  
**Formato da Peça**: Carrossel vertical para Instagram (4:5 — 1080 × 1350 px)  
**Quantidade**: 8 slides individuais  
**Mídia de Saída**: PNG de alta resolução + templates HTML editáveis desacoplados  
**Data**: Setembro de 2026  

---

## 1. Objetivo Editorial e Estratégia de Comunicação

### 1.1 O Gancho Nostálgico e a Entrega Fonoaudiológica
O carrossel utiliza a memória afetiva da infância brasileira dos anos 1980 como um potente conector emocional com o público adulto (pais, mães, tios, educadores e cuidadores hoje na faixa dos 30 aos 50+ anos). 

Ao reconhecer situações de sua própria infância (*"Eu fazia isso"*), o leitor é guiado suavemente por uma narrativa que desmistifica a estimulação de linguagem:
- Mostrar que **brincar livremente, interagir com pares, narrar enredos e negociar regras** são as bases mais ricas do desenvolvimento comunicativo humano.
- Posicionar a Fonoaudiologia como uma ciência acolhedora da vida cotidiana, e não como um conjunto de regras frias ou exercícios mecânicos.

### 1.2 Limites Éticos e Diretrizes Clínicas Imutáveis
Por orientação estrita e zelo profissional da Dra. Sônia Torres, este conteúdo adota salvaguardas categóricas:
1. **Sem moralismo geracional**: Jamais sugerir que *"antigamente as crianças se desenvolviam melhor"* ou que *"naquela época a infância era perfeita"*.
2. **Sem vilanização da tecnologia**: Não atacar celulares, tablets, computadores, videogames ou televisão. Não culpabilizar pais contemporâneos pela dinâmica da vida moderna.
3. **Sem afirmações diagnósticas ou terapêuticas levianas**: Não afirmar que uma brincadeira isolada "trata", "cura", "previne atraso" ou "substitui avaliação especializada".
4. **Mensagem Central (Slide 7)**:
   > *“Não precisamos voltar aos anos 80. Precisamos preservar oportunidades para a criança conversar, criar, brincar e interagir.”*

---

## 2. Arquitetura do Projeto e Estrutura de Diretórios

A peça foi construída dentro do padrão modular do ecossistema de materiais da Dra. Sônia Torres:

```text
/Materiais-Sonia/
├── docs/
│   └── carrossel-anos-80-brincadeiras-linguagem.md      # Este documento de especificação técnica e editorial
├── prompts/
│   └── carrossel-anos-80-brincadeiras-linguagem-prompts.md # Direção fotográfica e prompts nos 4 eixos
├── scripts/
│   └── render_carrossel_anos_80.py                     # Script Python de renderização e automação Playwright
└── anos-80-brincadeiras-linguagem/
    ├── raw-photos/                                     # Imagens fotográficas documentais dos slides
    ├── templates-editaveis/                            # Templates HTML desacoplados com CSS puro
    │   ├── slide_01.html
    │   ├── ...
    │   └── slide_08.html
    ├── slides-finais/                                  # Arquivos PNG finais em 1080 x 1350 px
    └── preview.html                                    # Painel de conferência lado a lado para navegador
```

---

## 3. Roteiro Editorial e Fluxo dos Slides

| Slide | Tipo / Função | Título / Conteúdo Central | Complemento / Apoio |
| :--- | :--- | :--- | :--- |
| **01** | Capa / Retenção | **“Coisas que uma criança dos anos 80 fazia sem saber que estava estimulando a linguagem”** (com destaque tipográfico em **"ANOS 80"**) | Arraste para o lado 👉 |
| **02** | Faz de Conta / Simbolismo | **“Transformava qualquer coisa em brincadeira.”** | *“E inventava personagens, situações, diálogos e histórias.”* |
| **03** | Narrativa / Sequenciamento | **“Uma brincadeira começava de um jeito... e terminava de outro completamente diferente.”** | *“Criar histórias coloca palavras, ideias e sequências em movimento.”* |
| **04** | Negociação / Pragmática | Falas vivas em destaque: *“Agora é minha vez!”*, *“Não vale!”*, *“Você fica no gol.”*, *“Depois eu troco.”* | *“Brincar junto também exigia explicar, argumentar, combinar e responder.”* |
| **05** | Consciência Fonológica e Ritmo | **“Cantigas, rimas, parlendas, adivinhas...”** | *“Enquanto brincavam, as crianças exploravam sons, ritmo e palavras.”* |
| **06** | Troca Comunicativa / Turnos | **“Boa parte da brincadeira era... conversar.”** | *“Perguntar. Responder. Contar. Escutar. Esperar a vez.”* (com espaçamento rítmico generoso) |
| **07** | Virada Conceitual Contemporânea | **“Não precisamos voltar aos anos 80.”** | *“Precisamos preservar oportunidades para a criança conversar, criar, brincar e interagir.”* |
| **08** | Interatividade e Conversão | **“Qual dessas você fazia?”** (Checklist de memórias afetivas) + **“Marque alguém que brincava com você.”** + *“E conte nos comentários uma brincadeira que ficou faltando.”* | **Crédito Obrigatório:**<br>`Sônia Torres`<br>`Fonoaudióloga \| CRFa 1-17701` |

---

## 4. Sistema Visual e Design Editorial

### 4.1 Proporção e Área de Respiro (Safe Area)
- **Dimensão Nativa**: 1080 × 1350 px (4:5 vertical).
- **Margens de Proteção**:
  - Topo: 80 px (evita cortes de nome de usuário e interface superior do Instagram).
  - Base: 100 px (evita sobreposição dos botões de curtir, salvar, comentar e áudio do app).
  - Laterais: 75 px (garante conforto de leitura e afasta o texto das bordas físicas da tela).

### 4.2 Paleta Cromática Inspirada em Álbuns Antigos
- **Creme Envelhecido / Papel de Álbum (Fundo)**: `#F7F3EB` e `#EFE8DA`
- **Marrom Profundo Quente (Tipografia Principal)**: `#2A1F16` (contraste acessível com o fundo claro)
- **Terracota Nostálgico (Destaque Principal / "ANOS 80")**: `#B85333`
- **Verde Apagado / Musgo Vintage (Tags e Indicadores)**: `#4D6251`
- **Amarelo Solar Queimado (Acentos)**: `#E3A857`
- **Azul Desaturado**: `#4F6873`

### 4.3 Tipografia
- **Títulos Editoriais**: `Fraunces` (Google Fonts, serifada com espírito editorial dos anos 70/80, calorosa e com traços orgânicos).
- **Corpo de Texto e Acentos**: `Plus Jakarta Sans` (sem serifa moderna, legível em tamanhos reduzidos em qualquer tela mobile).

### 4.4 Direção Fotográfica Analógica
- Simulação de película 35 mm (Kodak Gold / Kodak ColorPlus 200), câmeras Nikon F3 / Canon A-1, lentes 35 mm f/2 e 50 mm f/1.8.
- O Slide 7 opera a quebra de época para fotografia contemporânea limpa e ensolarada.
- O Slide 8 simula a página de encerramento de álbum de fotos clássico com cantoneiras de papel fotográfico e tipografia nítida.

---

## 5. Fluxo de Dados e Automação de Renderização

1. O script `scripts/render_carrossel_anos_80.py`:
   - Carrega as definições estruturadas dos 8 slides;
   - Compila o CSS com design system retro-editorial;
   - Converte as fotografias em Base64 ou caminhos relativos embutidos;
   - Salva cada slide como arquivo HTML individual e desacoplado em `templates-editaveis/slide_XX.html`;
   - Gera o painel de inspeção visual `preview.html`;
   - Inicializa uma instância headless do Chromium via Playwright com viewport `1080x1350` e device scale factor `1.0`;
   - Renderiza e salva screenshots nítidos em `slides-finais/slide_XX.png`.

---

## 6. Como Manter e Editar a Funcionalidade

- **Para alterar textos de um slide**: Modifique diretamente o dicionário de dados em `scripts/render_carrossel_anos_80.py` ou o arquivo `.html` correspondente em `templates-editaveis/`.
- **Para atualizar uma foto**: Substitua o arquivo correspondente em `raw-photos/` e reexecute o script de renderização.
- **Para re-renderizar todas as imagens**:
  ```powershell
  python scripts/render_carrossel_anos_80.py
  ```
- **Para revisar o resultado visual**: Abra `anos-80-brincadeiras-linguagem/preview.html` em qualquer navegador web.
