"""
Script de Renderização Editorial e Visual:
Carrossel "Coisas que uma criança dos anos 80 fazia sem saber que estava estimulando a linguagem"
Fonoaudióloga Sônia Torres · CRFa 1-17701

Gera:
1. Templates HTML desacoplados e editáveis em:
   /anos-80-brincadeiras-linguagem/templates-editaveis/
2. 8 slides individuais em formato vertical 4:5 (1080 x 1350 px) PNG em:
   /anos-80-brincadeiras-linguagem/slides-finais/
3. Painel de preview preview.html para conferência lado a lado no navegador
"""

import os
import sys
import base64
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"c:\Users\Gamer\OneDrive\Documentos\Materiais-Sonia\anos-80-brincadeiras-linguagem"
PHOTOS_DIR = os.path.join(BASE_DIR, "raw-photos")
OUTPUT_DIR = os.path.join(BASE_DIR, "slides-finais")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates-editaveis")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

def image_to_base64(filepath):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "rb") as f:
        return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"

# Dados estruturados dos 8 slides
SLIDES = [
    {
        "id": "01",
        "type": "capa",
        "tag": "MEMÓRIA AFETIVA & LINGUAGEM",
        "indicator": "01/08",
        "title_pre": "Coisas que uma criança dos",
        "title_highlight": "ANOS 80",
        "title_pos": "fazia sem saber que estava estimulando a linguagem",
        "author": "Sônia Torres · Fonoaudióloga · CRFa 1-17701",
        "swipe": "Arraste para o lado 👉",
        "photo": "foto-slide-01.jpg"
    },
    {
        "id": "02",
        "type": "faz_de_conta",
        "tag": "INFÂNCIA DOS ANOS 80",
        "indicator": "02/08",
        "title": "Transformava qualquer coisa em brincadeira.",
        "complement": "E inventava personagens, situações, diálogos e histórias.",
        "concept_badge": "FAZ DE CONTA & SÍMBOLOS",
        "photo": "foto-slide-02.jpg"
    },
    {
        "id": "03",
        "type": "inventar_historias",
        "tag": "INFÂNCIA DOS ANOS 80",
        "indicator": "03/08",
        "title": "Uma brincadeira começava de um jeito...",
        "title_highlight": "...e terminava de outro completamente diferente.",
        "text_small": "Criar histórias coloca palavras, ideias e sequências em movimento.",
        "concept_badge": "NARRATIVA & SEQUENCIAMENTO",
        "photo": "foto-slide-03.jpg"
    },
    {
        "id": "04",
        "type": "negociar_regras",
        "tag": "INFÂNCIA DOS ANOS 80",
        "indicator": "04/08",
        "quotes": [
            "“Agora é minha vez!”",
            "“Não vale!”",
            "“Você fica no gol.”",
            "“Depois eu troco.”"
        ],
        "complement": "Brincar junto também exigia explicar, argumentar, combinar e responder.",
        "concept_badge": "COMUNICAÇÃO PRAGMÁTICA",
        "photo": "foto-slide-04.jpg"
    },
    {
        "id": "05",
        "type": "cantar_rimas",
        "tag": "INFÂNCIA DOS ANOS 80",
        "indicator": "05/08",
        "title": "Cantigas, rimas, parlendas, adivinhas...",
        "complement": "Enquanto brincavam, as crianças exploravam sons, ritmo e palavras.",
        "concept_badge": "CONSCIÊNCIA FONOLÓGICA",
        "photo": "foto-slide-05.jpg"
    },
    {
        "id": "06",
        "type": "conversar",
        "tag": "INFÂNCIA DOS ANOS 80",
        "indicator": "06/08",
        "title": "Boa parte da brincadeira era... conversar.",
        "rhythm_words": [
            "Perguntar.",
            "Responder.",
            "Contar.",
            "Escutar.",
            "Esperar a vez."
        ],
        "concept_badge": "TURNOS DE CONVERSA",
        "photo": "foto-slide-06.jpg"
    },
    {
        "id": "07",
        "type": "virada_presente",
        "tag": "DESENVOLVIMENTO HOJE",
        "indicator": "07/08",
        "title_virada": "Não precisamos voltar aos anos 80.",
        "complement_virada": "Precisamos preservar oportunidades para a criança conversar, criar, brincar e interagir.",
        "photo": "foto-slide-07.jpg"
    },
    {
        "id": "08",
        "type": "engajamento",
        "tag": "ÁLBUM DE MEMÓRIAS",
        "indicator": "08/08",
        "title": "Qual dessas você fazia?",
        "checklist": [
            "Brincava de casinha",
            "Inventava histórias",
            "Cantava cantigas",
            "Brincava na rua",
            "Criava regras para as brincadeiras",
            "Todas as anteriores"
        ],
        "cta_main": "Marque alguém que brincava com você.",
        "cta_sub": "E conte nos comentários uma brincadeira que ficou faltando.",
        "footer_name": "Sônia Torres",
        "footer_cred": "Fonoaudióloga | CRFa 1-17701",
        "photo": "foto-slide-08.jpg"
    }
]

CSS_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
}

body {
    width: 1080px;
    height: 1350px;
    background-color: #EDE7DC;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #251B14;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

.slide-wrapper {
    width: 1080px;
    height: 1350px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 64px 74px 58px 74px;
    background: #F8F4EC;
    overflow: hidden;
}

/* Textura suave de papel de álbum antigo */
.slide-wrapper::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 20%, rgba(255,255,255,0.45) 0%, rgba(220,205,185,0.2) 100%);
    pointer-events: none;
    z-index: 1;
}

/* Moldura externa sutil inspirada em encadernação de álbum */
.slide-wrapper::before {
    content: "";
    position: absolute;
    top: 20px;
    left: 20px;
    right: 20px;
    bottom: 20px;
    border: 1px solid rgba(184, 78, 48, 0.16);
    border-radius: 28px;
    pointer-events: none;
    z-index: 2;
}

/* Barra superior */
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
    z-index: 3;
}

.badge-tag {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    background: #EFE6D8;
    color: #3B2A1E;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 8px 20px;
    border-radius: 100px;
    border: 1.5px solid #DFCFC0;
}

.badge-tag .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #B84E30;
}

.indicator-pill {
    font-size: 19px;
    font-weight: 700;
    color: #3B2A1E;
    background: #FFFFFF;
    padding: 7px 18px;
    border-radius: 100px;
    border: 1.5px solid #DFCFC0;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.03);
}

/* Estilo geral de moldura fotográfica analógica */
.photo-passepartout {
    width: 100%;
    background: #FFFFFF;
    padding: 14px 14px 18px 14px;
    border-radius: 20px;
    box-shadow: 0 16px 36px rgba(50, 30, 15, 0.11), 0 2px 8px rgba(0,0,0,0.04);
    border: 1.5px solid #E5DCD0;
    position: relative;
    z-index: 3;
    overflow: hidden;
}

.photo-passepartout img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 12px;
    display: block;
}

/* ================= SLIDE 1 (CAPA) ================= */
.capa-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
    z-index: 3;
}

.capa-header {
    margin-top: 4px;
    margin-bottom: 22px;
}

.capa-title-pre {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 42px;
    font-weight: 500;
    line-height: 1.15;
    color: #3E2B1F;
    letter-spacing: -0.5px;
}

.capa-title-highlight {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 78px;
    font-weight: 800;
    color: #B84E30;
    line-height: 1.02;
    letter-spacing: -1.5px;
    display: block;
    margin: 4px 0 6px 0;
    text-shadow: 1px 2px 0px rgba(184, 78, 48, 0.15);
}

.capa-title-pos {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 32px;
    font-weight: 700;
    line-height: 1.25;
    color: #2F2116;
    letter-spacing: -0.4px;
}

.capa-photo-box {
    width: 100%;
    height: 720px;
}

.capa-photo-box img {
    height: 684px;
}

.capa-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 18px;
    border-top: 1.5px solid #E5DBD0;
    margin-top: 16px;
    width: 100%;
}

.author-pill {
    font-size: 19px;
    font-weight: 600;
    color: #4A382A;
}

.swipe-pill {
    font-size: 20px;
    font-weight: 700;
    color: #B84E30;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ================= SLIDES DE CONTEÚDO (2 A 6) ================= */
.content-slide-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
    z-index: 3;
}

.editorial-header {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 20px;
}

.concept-badge {
    align-self: flex-start;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #3E5B47;
    background: #E5EDE6;
    padding: 5px 14px;
    border-radius: 6px;
    border: 1px solid #C8DAC9;
}

.content-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 47px;
    font-weight: 700;
    line-height: 1.18;
    color: #2C1D13;
    letter-spacing: -0.6px;
}

.content-complement {
    font-size: 27px;
    font-weight: 500;
    line-height: 1.4;
    color: #4C3A2D;
    letter-spacing: -0.2px;
}

.content-photo-box {
    width: 100%;
    height: 740px;
    margin-top: 6px;
}

.content-photo-box img {
    height: 704px;
}

/* Slide 3 específico */
.title-highlight-s3 {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 44px;
    font-weight: 700;
    color: #B84E30;
    line-height: 1.2;
    margin-top: 4px;
}

.text-small-s3 {
    font-size: 24px;
    font-weight: 600;
    color: #3E5B47;
    line-height: 1.35;
    background: #EAF0EB;
    padding: 12px 18px;
    border-radius: 10px;
    border-left: 4px solid #3E5B47;
    margin-top: 6px;
}

/* Slide 4 específico (Falas) */
.quotes-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
}

.quote-card {
    background: #FAF6EF;
    border: 1.5px solid #DFCFC0;
    border-radius: 12px;
    padding: 12px 16px;
    font-family: 'Fraunces', Georgia, serif;
    font-size: 25px;
    font-weight: 700;
    color: #B84E30;
    line-height: 1.25;
    box-shadow: 0 4px 10px rgba(50, 30, 15, 0.04);
}

/* Slide 6 específico (Rhythm words) */
.rhythm-container {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 10px;
    margin-bottom: 8px;
}

.rhythm-pill {
    background: #EFE6D8;
    color: #2F2015;
    font-size: 23px;
    font-weight: 700;
    padding: 8px 18px;
    border-radius: 30px;
    border: 1.5px solid #DECFC0;
}

/* ================= SLIDE 7 (A VIRADA) ================= */
.virada-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
    z-index: 3;
}

.virada-header {
    background: #FAF6EF;
    border: 2px solid #E5DBD0;
    border-radius: 20px;
    padding: 36px 36px;
    box-shadow: 0 8px 24px rgba(40, 20, 10, 0.05);
    margin-bottom: 20px;
}

.virada-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 48px;
    font-weight: 800;
    color: #B84E30;
    line-height: 1.15;
    margin-bottom: 24px;
    letter-spacing: -0.6px;
}

.virada-divider {
    width: 60px;
    height: 3px;
    background-color: #E3A857;
    margin-bottom: 24px;
}

.virada-complement {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 29px;
    font-weight: 600;
    line-height: 1.42;
    color: #2F2116;
    letter-spacing: -0.3px;
}

.virada-photo-box {
    width: 100%;
    height: 680px;
}

.virada-photo-box img {
    height: 644px;
}

/* ================= SLIDE 8 (ENGAJAMENTO & ÁLBUM) ================= */
.album-slide-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: space-between;
    z-index: 3;
}

.album-header-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 50px;
    font-weight: 800;
    color: #2F2015;
    line-height: 1.15;
    margin-bottom: 20px;
    letter-spacing: -0.8px;
}

.checklist-card {
    background: #FFFFFF;
    border: 2px solid #E5DCD0;
    border-radius: 20px;
    padding: 24px 30px;
    box-shadow: 0 10px 28px rgba(45, 25, 15, 0.06);
    margin-bottom: 24px;
}

.checklist-list {
    display: flex;
    flex-direction: column;
    gap: 13px;
    list-style: none;
}

.checklist-item {
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 23px;
    font-weight: 600;
    color: #38271B;
}

.check-box-vintage {
    width: 28px;
    height: 28px;
    border: 2px solid #B84E30;
    border-radius: 6px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #FAF4EB;
    color: #B84E30;
    font-size: 19px;
    font-weight: 800;
    flex-shrink: 0;
}

.checklist-item.all-above {
    margin-top: 4px;
    padding-top: 12px;
    border-top: 1.5px dashed #E5DCD0;
    font-weight: 700;
    color: #B84E30;
}

.album-middle-section {
    display: flex;
    gap: 22px;
    align-items: center;
    background: #F3EBDD;
    border: 2px solid #DFCFC0;
    border-radius: 20px;
    padding: 22px 26px;
    margin-bottom: 24px;
}

.polaroid-box {
    width: 170px;
    height: 170px;
    background: #FFFFFF;
    padding: 8px 8px 18px 8px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    border-radius: 8px;
    transform: rotate(-3deg);
    flex-shrink: 0;
}

.polaroid-box img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 4px;
}

.album-cta-text {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.album-cta-main {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 31px;
    font-weight: 800;
    color: #B84E30;
    line-height: 1.2;
}

.album-cta-sub {
    font-size: 21px;
    font-weight: 600;
    color: #4C3A2D;
    line-height: 1.35;
}

/* Rodapé estritamente conforme norma da usuária */
.final-footer-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 20px;
    border-top: 1.5px solid #DECFC0;
    text-align: center;
    width: 100%;
}

.final-footer-name {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 28px;
    font-weight: 700;
    color: #2F2116;
    letter-spacing: -0.3px;
    margin-bottom: 3px;
}

.final-footer-cred {
    font-size: 19px;
    font-weight: 600;
    color: #5C4738;
    letter-spacing: 0.5px;
}
"""

def generate_slide_html(slide_data, embedded_image):
    slide_id = slide_data["id"]
    slide_type = slide_data["type"]
    tag = slide_data.get("tag", "INFÂNCIA ANOS 80")
    indicator = slide_data.get("indicator", f"{slide_id}/08")
    
    top_bar = f"""
    <div class="top-bar">
        <div class="badge-tag">
            <span class="dot"></span>
            <span>{tag}</span>
        </div>
        <div class="indicator-pill">{indicator}</div>
    </div>
    """
    
    if slide_type == "capa":
        content = f"""
        <div class="capa-container">
            {top_bar}
            <div class="capa-header">
                <div class="capa-title-pre">{slide_data['title_pre']}</div>
                <div class="capa-title-highlight">{slide_data['title_highlight']}</div>
                <div class="capa-title-pos">{slide_data['title_pos']}</div>
            </div>
            
            <div class="photo-passepartout capa-photo-box">
                <img src="{embedded_image}" alt="Crianças brincando nos anos 80">
            </div>
            
            <div class="capa-footer">
                <div class="author-pill">{slide_data['author']}</div>
                <div class="swipe-pill">{slide_data['swipe']}</div>
            </div>
        </div>
        """
    elif slide_type == "faz_de_conta":
        content = f"""
        <div class="content-slide-container">
            {top_bar}
            <div class="editorial-header">
                <div class="concept-badge">{slide_data['concept_badge']}</div>
                <h1 class="content-title">{slide_data['title']}</h1>
                <p class="content-complement">{slide_data['complement']}</p>
            </div>
            
            <div class="photo-passepartout content-photo-box">
                <img src="{embedded_image}" alt="Brincadeira de faz de conta">
            </div>
        </div>
        """
    elif slide_type == "inventar_historias":
        content = f"""
        <div class="content-slide-container">
            {top_bar}
            <div class="editorial-header">
                <div class="concept-badge">{slide_data['concept_badge']}</div>
                <h1 class="content-title">{slide_data['title']}</h1>
                <div class="title-highlight-s3">{slide_data['title_highlight']}</div>
                <div class="text-small-s3">{slide_data['text_small']}</div>
            </div>
            
            <div class="photo-passepartout content-photo-box">
                <img src="{embedded_image}" alt="Inventando histórias">
            </div>
        </div>
        """
    elif slide_type == "negociar_regras":
        quotes_html = "".join([f'<div class="quote-card">{q}</div>' for q in slide_data['quotes']])
        content = f"""
        <div class="content-slide-container">
            {top_bar}
            <div class="editorial-header">
                <div class="concept-badge">{slide_data['concept_badge']}</div>
                <div class="quotes-grid">
                    {quotes_html}
                </div>
                <p class="content-complement" style="font-weight:600; color:#2E2015;">{slide_data['complement']}</p>
            </div>
            
            <div class="photo-passepartout content-photo-box" style="height: 680px;">
                <img src="{embedded_image}" alt="Negociando as regras">
            </div>
        </div>
        """
    elif slide_type == "cantar_rimas":
        content = f"""
        <div class="content-slide-container">
            {top_bar}
            <div class="editorial-header">
                <div class="concept-badge">{slide_data['concept_badge']}</div>
                <h1 class="content-title">{slide_data['title']}</h1>
                <p class="content-complement">{slide_data['complement']}</p>
            </div>
            
            <div class="photo-passepartout content-photo-box">
                <img src="{embedded_image}" alt="Cantigas de roda e rimas">
            </div>
        </div>
        """
    elif slide_type == "conversar":
        rhythm_html = "".join([f'<div class="rhythm-pill">{w}</div>' for w in slide_data['rhythm_words']])
        content = f"""
        <div class="content-slide-container">
            {top_bar}
            <div class="editorial-header">
                <div class="concept-badge">{slide_data['concept_badge']}</div>
                <h1 class="content-title">{slide_data['title']}</h1>
                <div class="rhythm-container">
                    {rhythm_html}
                </div>
            </div>
            
            <div class="photo-passepartout content-photo-box" style="height: 700px;">
                <img src="{embedded_image}" alt="Conversando e trocando turnos">
            </div>
        </div>
        """
    elif slide_type == "virada_presente":
        content = f"""
        <div class="virada-container">
            {top_bar}
            <div class="virada-header">
                <h1 class="virada-title">{slide_data['title_virada']}</h1>
                <div class="virada-divider"></div>
                <p class="virada-complement">{slide_data['complement_virada']}</p>
            </div>
            
            <div class="photo-passepartout virada-photo-box">
                <img src="{embedded_image}" alt="Interação positiva no presente">
            </div>
        </div>
        """
    elif slide_type == "engajamento":
        items_html = ""
        for item in slide_data['checklist']:
            is_all = item == "Todas as anteriores"
            cls = "checklist-item all-above" if is_all else "checklist-item"
            items_html += f"""
            <li class="{cls}">
                <div class="check-box-vintage">✓</div>
                <span>{item}</span>
            </li>
            """
            
        content = f"""
        <div class="album-slide-container">
            {top_bar}
            <div>
                <h1 class="album-header-title">{slide_data['title']}</h1>
                
                <div class="checklist-card">
                    <ul class="checklist-list">
                        {items_html}
                    </ul>
                </div>
                
                <div class="album-middle-section">
                    <div class="polaroid-box">
                        <img src="{embedded_image}" alt="Foto polaroid de infância">
                    </div>
                    <div class="album-cta-text">
                        <div class="album-cta-main">{slide_data['cta_main']}</div>
                        <div class="album-cta-sub">{slide_data['cta_sub']}</div>
                    </div>
                </div>
            </div>
            
            <div class="final-footer-box">
                <div class="final-footer-name">{slide_data['footer_name']}</div>
                <div class="final-footer-cred">{slide_data['footer_cred']}</div>
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1350">
    <title>Slide {slide_id} - Carrossel Anos 80 e Linguagem</title>
    <style>
{CSS_STYLES}
    </style>
</head>
<body>
    <div class="slide-wrapper">
        {content}
    </div>
</body>
</html>"""
    return html

def build_preview_html():
    preview_items = ""
    for slide in SLIDES:
        sid = slide["id"]
        img_src = f"slides-finais/slide_{sid}.png"
        preview_items += f"""
        <div class="slide-card">
            <div class="slide-card-header">
                <span class="slide-num">SLIDE {sid}</span>
                <span class="slide-title">{slide.get('title', slide.get('title_highlight', 'Slide ' + sid))}</span>
            </div>
            <div class="slide-img-box">
                <img src="{img_src}" alt="Slide {sid}" loading="lazy">
            </div>
            <div class="slide-actions">
                <a href="templates-editaveis/slide_{sid}.html" target="_blank">Editar Template HTML</a>
                <a href="{img_src}" download>Baixar PNG (1080x1350)</a>
            </div>
        </div>
        """
        
    preview_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview: Carrossel Anos 80 e Linguagem - Sônia Torres</title>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@700;800&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            background: #201914;
            color: #FAF4EB;
            font-family: 'Plus Jakarta Sans', sans-serif;
            margin: 0;
            padding: 40px 30px;
        }}
        .header {{
            max-width: 1400px;
            margin: 0 auto 40px auto;
            border-bottom: 1px solid #4D392B;
            padding-bottom: 24px;
        }}
        .header h1 {{
            font-family: 'Fraunces', Georgia, serif;
            color: #EFA689;
            font-size: 34px;
            margin: 0 0 10px 0;
        }}
        .header p {{
            color: #CBB9A8;
            font-size: 17px;
            margin: 0;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .slide-card {{
            background: #2D231C;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #48362A;
            box-shadow: 0 12px 28px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
        }}
        .slide-card-header {{
            padding: 14px 18px;
            background: #382B22;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #48362A;
        }}
        .slide-num {{
            font-size: 13px;
            font-weight: 800;
            background: #B84E30;
            color: #FFF;
            padding: 3px 8px;
            border-radius: 4px;
        }}
        .slide-title {{
            font-size: 13px;
            color: #E2D3C5;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 200px;
        }}
        .slide-img-box {{
            width: 100%;
            aspect-ratio: 4/5;
            background: #1A130F;
            overflow: hidden;
        }}
        .slide-img-box img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}
        .slide-actions {{
            padding: 14px 18px;
            display: flex;
            justify-content: space-between;
            background: #261D17;
            border-top: 1px solid #3D2D23;
        }}
        .slide-actions a {{
            color: #EFA689;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            transition: color 0.2s;
        }}
        .slide-actions a:hover {{
            color: #FFF;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Carrossel: Coisas que uma criança dos anos 80 fazia sem saber que estava estimulando a linguagem</h1>
        <p>Sônia Torres · Fonoaudióloga · CRFa 1-17701 · 8 slides verticais 4:5 (1080 x 1350 px)</p>
    </div>
    
    <div class="grid">
        {preview_items}
    </div>
</body>
</html>"""
    with open(os.path.join(BASE_DIR, "preview.html"), "w", encoding="utf-8") as f:
        f.write(preview_html)

def main():
    print("Iniciando geração de templates HTML...")
    
    # 1. Gerar os templates HTML individuais
    for slide in SLIDES:
        sid = slide["id"]
        photo_filename = slide["photo"]
        photo_path = os.path.join(PHOTOS_DIR, photo_filename)
        embedded_base64 = image_to_base64(photo_path)
        
        slide_html = generate_slide_html(slide, embedded_base64)
        template_path = os.path.join(TEMPLATES_DIR, f"slide_{sid}.html")
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(slide_html)
        print(f"  [OK] Template slide_{sid}.html criado com sucesso.")
        
    print("\nIniciando renderizacao de alta resolucao com Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=1.0
        )
        
        for slide in SLIDES:
            sid = slide["id"]
            template_path = os.path.join(TEMPLATES_DIR, f"slide_{sid}.html")
            output_png = os.path.join(OUTPUT_DIR, f"slide_{sid}.png")
            
            page.goto(f"file:///{template_path.replace(os.sep, '/')}")
            # Aguardar fontes do Google carregarem
            page.wait_for_timeout(600)
            page.screenshot(path=output_png, full_page=True)
            print(f"  [OK] Renderizado PNG: slide_{sid}.png (1080x1350)")
            
        browser.close()
        
    print("\nGerando pagina preview.html...")
    build_preview_html()
    print("  [OK] preview.html criado com sucesso.")
    print("\nProcesso concluido com sucesso!")

if __name__ == "__main__":
    main()
