# Planejamento: Destaque "Quem é" — Sônia Torres (Fonoaudióloga)

## 1. Objetivo
Criar um conjunto editorial e humano de 5 Stories (1080 × 1920 px, 9:16) e 1 Capa para o Destaque "Quem é" do perfil profissional de Instagram da fonoaudióloga Sônia Torres (CRFa 1-17701). O material tem como objetivo apresentar Sônia com sobriedade, calor humano, credibilidade e acolhimento para novos visitantes, sem tom de venda apelativa ou sensacionalismo.

## 2. Arquitetura e Direção Visual
- **Dimensões e Proporção:** 1080 × 1920 px (9:16) para Stories; 1080 × 1080 px (1:1) com zona circular de segurança para a Capa.
- **Áreas de Segurança Instagram:** 
  - Margem superior segura: 220 px (evita sobreposição com cabeçalho/foto de perfil/tempo de story).
  - Margem inferior segura: 260 px (evita sobreposição com barra de resposta/direct/reação).
  - Margens laterais seguras: 80 px de respiro.
- **Paleta de Cores Editorial:**
  - Verde Petróleo Profundo: `#1D382B` (rgb 29, 56, 43) — identidade institucional e autoridade.
  - Verde Oliva Clínico: `#44634B` (rgb 68, 99, 75) — tom de saúde, acolhimento e natureza.
  - Fundo Off-White / Creme: `#FAF7F2` (rgb 250, 247, 242) — fundo limpo, confortável e orgânico.
  - Cartão / Areia Suave: `#F4EFE8` (rgb 244, 239, 232) e `#EAE4D8` (rgb 234, 228, 216).
  - Grafite Texto Principal: `#2E2C29` (rgb 46, 44, 41) — legibilidade máxima sem o preto puro agressivo.
  - Cinza Muted / Apoio: `#706B64` (rgb 112, 107, 100).
  - Terracota / Coral Destaque: `#C4542E` (rgb 196, 84, 46).
- **Tipografia:**
  - Plus Jakarta Sans (Regular 400, Medium 500, SemiBold 600, Bold 700), otimizada para telas móveis.
- **Fotografia e Imagens:**
  - Story 01 e Story 02: Utilização da fotografia profissional e autêntica de Sônia Torres (`assets/sonia_pao_de_acucar.jpeg`), em jaleco com identificação ("Sônia Torres de Araújo - Fonoaudiologia" e brasão UFRJ), sorriso acolhedor e Pão de Açúcar ao fundo, sem qualquer alteração artificial de feições.
  - Story 03: Fotografia profissional de contexto clínico (materiais lúdicos de avaliação, prancheta de escuta individualizada).
  - Story 04: Fotografia humanizada com representação multigeracional natural (crianças, adultos e idosos compartilhando momentos de comunicação e leitura).
  - Story 05: Composição editorial limpa com dados de contato, identificação profissional e área reservada para sticker de link.
  - Capa: Círculo centralizado em Verde Petróleo Profundo `#1D382B` com ícone minimalista de perfil e tipografia legível em Creme `#FAF7F2`.

## 3. Arquivos Criados ou Alterados
- `/scripts/gerar_destaque_quem_e.py`: Script automatizado com Pillow para renderização determinística em alta resolução.
- `/prompts/destaque-quem-e-prompts.md`: Fichas técnicas completas no formato exigido ([Tema], [Ângulo], [Iluminação], [Lente]).
- `/docs/destaque-quem-e-guia.md`: Guia de implementação, manutenção e boas práticas.
- `/assets/destaque-quem-e/`:
  - `story_01_apresentacao.png` (1080 × 1920)
  - `story_02_formacao.png` (1080 × 1920)
  - `story_03_forma_trabalho.png` (1080 × 1920)
  - `story_04_quem_atende.png` (1080 × 1920)
  - `story_05_chamada_final.png` (1080 × 1920)
  - `capa_destaque_quem_e.png` (1080 × 1080)
  - `capa_destaque_quem_e_story.png` (1080 × 1920)
  - `prancha_visao_geral.png` (visão geral de todos os slides e capa)

## 4. Dependências Necessárias
- Python 3 com biblioteca `Pillow` (já instalada no ambiente).

## 5. Possíveis Riscos e Mitigações
- **Risco de corte no app do Instagram:** Mitigado pelo cálculo rigoroso das zonas de segurança (padding superior de 240px e inferior de 280px para os textos centrais).
- **Risco de distorção de imagem real:** Mitigado pelo uso de redimensionamento proporcional com antialiasing Lanczos e enquadramento manual ajustado.
- **Risco de texto minúsculo em tela de celular:** Mitigado por hierarquia visual com corpo de texto entre 42px e 52px e títulos entre 64px e 82px.
