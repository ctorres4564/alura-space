# Planejamento & Documentação Técnica do Carrossel de Telas

- **Profissional:** Dra. Sônia Torres · Fonoaudióloga · CRFa 1-17701
- **Tema:** *"Deixo o celular para ele ficar quieto"* (Telas na Primeira Infância)
- **Formato:** Carrossel Instagram Portrait 4:5 (1080×1350 px)
- **Origem do Conteúdo:** Reel sincronizado `reels_telas_sonia_torres.mp4`

---

## 1. Arquitetura da Solução

O carrossel foi estruturado em **7 slides** estratégicos que cobrem o arco narrativo completo do Reel original, com linguagem acolhedora, fundamentação pediátrica e rigor científico:

| Slide | Nome do Arquivo | Função Estratégica | Elemento Visual & Enquadramento |
| :--- | :--- | :--- | :--- |
| **01** | `slide_01_capa.png` | Gancho de identificação imediata | Foto Quadro 1 (Smartphone e toque suave das mãos) |
| **02** | `slide_02_acolhimento.png` | Quebra de culpa familiar e empatia | Cartões editoriais de acolhimento |
| **03** | `slide_03_ate_2_anos.png` | Marco biológico: Zero tela até 2 anos | Foto Quadro 2 (Blocos de madeira e dedinhos) |
| **04** | `slide_04_de_2_a_5_anos.png` | Marco prático: Até 1h/dia dos 2 aos 5 | Foto Quadro 3 (Massinha sensorial e ampulheta ao fundo) |
| **05** | `slide_05_estudo_cientifico.png` | Desmistificação da pesquisa JAMA | Foto Quadro 4 (Cartões ilustrados em flat lay cooperativo) |
| **06** | `slide_06_atencao_conjunta.png` | Conclusão fonoaudiológica (Joint Attention) | Foto Quadro 5 (Macro close-up no livro infantil físico) |
| **07** | `slide_07_debate_cta.png` | Convite ao debate e conversão | Card de debate off-white (#FAF8F5) com perguntas e CTA |

---

## 2. Tratamento Especial de Enquadramento das Imagens

As imagens originais foram geradas no formato 9:16 (1080×1920). Para manter a fidelidade e impacto no formato 4:5 (1080×1350) em janelas de destaque de 940 px de largura:
- Foi criada a função modular `crop_and_fit_image()`, que redimensiona a imagem pela largura e aplica um corte vertical customizado (`focus_y_ratio`) centrado estritamente na **região de ação das mãos e objetos**.
- **Quadro 1 (`focus_y_ratio=0.44`):** Centraliza o visor iluminado do aparelho celular e o contato suave entre a mão da criança e a mão do adulto.
- **Quadro 2 (`focus_y_ratio=0.48`):** Preserva a torre de bloquinhos coloridos e o amparo carinhoso da mão adulta na base.
- **Quadro 3 (`focus_y_ratio=0.46`):** Captura tanto a massinha de modelar em primeiro plano quanto a ampulheta de madeira suave ao fundo.
- **Quadro 4 (`focus_y_ratio=0.45`):** Visão zenital (*flat lay*) mantendo os cartões infantis e o gesto conjunto de apontar para a mesma gravura.
- **Quadro 5 (`focus_y_ratio=0.46`):** Macro close-up com foco pontual no dedinho indicador da criança tocando a página do livro físico.

---

## 3. Identidade Visual Institucional

- **Fundo Base:** `#1C1034` (Roxo profundo) com gradiente vertical suave.
- **Cartões de Conteúdo:** `#281848` e `#301E54` com cantos arredondados de 18 a 22 px.
- **Cores de Destaque:**
  - `#F8BA36` (Dourado quente): subtítulos, tags de relevância e pontos de atenção.
  - `#A882F5` (Lilás de realce): chamada "Arraste ➔", fontes técnicas e elementos de interação.
- **Tipografia:**
  - Títulos: `Poppins-Bold`
  - Subtítulos e ênfases: `Segoe UI Bold`
  - Textos de leitura: `Segoe UI Regular`
- **Cabeçalho & Rodapé Padronizados:**
  - Cabeçalho: Tag comemorativa de categoria à esquerda e paginação (`X/7`) à direita.
  - Rodapé: Assinatura profissional `"Sônia Torres | Fonoaudióloga · CRFa 1-17701"` e chamada de transição.

---

## 4. Fluxo de Dados e Renderização

```
[publicacao/telas-objecao/imagens/quadro*_limpo.png]
                      │
                      ▼
        [crop_and_fit_image()]
(Escala proporcional + Foco vertical por cena + Máscara arredondada)
                      │
                      ▼
        [scripts/gerar_carrossel_telas.py]
                      │
                      ▼
        [publicacao/carrossel-telas/]
   ├── slide_01_capa.png
   ├── slide_02_acolhimento.png
   ├── slide_03_ate_2_anos.png
   ├── slide_04_de_2_a_5_anos.png
   ├── slide_05_estudo_cientifico.png
   ├── slide_06_atencao_conjunta.png
   ├── slide_07_debate_cta.png
   └── prancha_contato_carrossel.jpg
```

---

## 5. Como Manter e Executar a Funcionalidade

Para renderizar novamente ou atualizar textos dos slides:

```powershell
python scripts/gerar_carrossel_telas.py
```

Os arquivos PNG são exportados prontos para publicação na pasta:
`c:\Users\Gamer\OneDrive\Documentos\1MATERIASIDASONIA\01reels_novos\publicacao\carrossel-telas\`
