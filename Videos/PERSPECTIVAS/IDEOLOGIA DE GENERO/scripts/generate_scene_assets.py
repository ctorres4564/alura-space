import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=True):
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/impact.ttf"
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def apply_cinematic_grade(img, darken=0.4, tint=(10, 15, 25)):
    # Escurecimento sutil e tonalização fria/documental
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (tint[0], tint[1], tint[2], int(darken * 255)))
    img_rgba = img.convert("RGBA")
    return Image.alpha_composite(img_rgba, overlay)

def draw_top_kicker(draw, text, y=180, font_size=36, color=(200, 205, 215, 230), line_color=(217, 30, 54, 255)):
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((1080 - w) // 2, y), text, font=font, fill=color)
    draw.line([(540 - 70, y + 55), (540 + 70, y + 55)], fill=line_color, width=3)

def generate_all_scenes():
    print("Gerando bases visuais em 1080x1920 para as 10 cenas...")
    os.makedirs("assets/scenes", exist_ok=True)
    
    # Imagens carregadas
    img_plenario = Image.open("assets/images/plenario_discurso.jpg").resize((1080, 1920), Image.Resampling.LANCZOS)
    img_voto = Image.open("assets/images/voto_eleicao.jpg").resize((1080, 1920), Image.Resampling.LANCZOS)
    img_saude = Image.open("assets/images/saude_publica.jpg").resize((1080, 1920), Image.Resampling.LANCZOS)
    img_mob = Image.open("assets/images/mobilizacao_civica.jpg").resize((1080, 1920), Image.Resampling.LANCZOS)
    img_mulher = Image.open("assets/images/retrato_mulher.jpg").resize((1080, 1920), Image.Resampling.LANCZOS)
    
    # -------------------------------------------------------------
    # CENA 1: A PERGUNTA INCÔMODA
    # -------------------------------------------------------------
    c1 = apply_cinematic_grade(img_plenario, darken=0.45)
    d1 = ImageDraw.Draw(c1)
    draw_top_kicker(d1, "INVESTIGAÇÃO POLÍTICA", y=200)
    
    # Card escuro translúcido central
    d1.rounded_rectangle([(100, 480), (980, 960)], radius=24, fill=(10, 12, 16, 220), outline=(217, 30, 54, 180), width=2)
    f_c1_title = get_font(52, bold=True)
    f_c1_red = get_font(68, bold=True)
    f_c1_sub = get_font(38, bold=False)
    
    t1 = "POR QUE TANTO MEDO?"
    t2 = "IDEOLOGIA DE GÊNERO"
    t3 = "DISPUTA DE PODER VS DEFESA DA FAMÍLIA"
    
    w_t1 = d1.textbbox((0, 0), t1, font=f_c1_title)[2]
    w_t2 = d1.textbbox((0, 0), t2, font=f_c1_red)[2]
    w_t3 = d1.textbbox((0, 0), t3, font=f_c1_sub)[2]
    
    d1.text(((1080 - w_t1) // 2, 540), t1, font=f_c1_title, fill=(255, 255, 255, 255))
    d1.text(((1080 - w_t2) // 2, 650), t2, font=f_c1_red, fill=(225, 35, 55, 255))
    d1.text(((1080 - w_t3) // 2, 790), t3, font=f_c1_sub, fill=(190, 200, 215, 240))
    c1.convert("RGB").save("assets/scenes/scene_01.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 2: A CONSTRUÇÃO DE UM INIMIGO
    # -------------------------------------------------------------
    c2 = Image.new("RGBA", (1080, 1920), (12, 14, 18, 255))
    d2 = ImageDraw.Draw(c2)
    draw_top_kicker(d2, "CONSTRUÇÃO DE DISCURSO", y=180, line_color=(138, 43, 226, 255))
    
    # Subtítulo de introdução
    f_sec = get_font(38, bold=False)
    txt_sec = "Termos distintos agrupados sob uma única narrativa:"
    w_sec = d2.textbbox((0, 0), txt_sec, font=f_sec)[2]
    d2.text(((1080 - w_sec) // 2, 280), txt_sec, font=f_sec, fill=(180, 185, 195, 240))
    
    # Caixas dos termos
    termos = ["FEMINISMO", "EDUCAÇÃO SEXUAL", "DIREITOS LGBT", "AUTONOMIA DAS MULHERES"]
    f_term = get_font(42, bold=True)
    y_box = 370
    for term in termos:
        d2.rounded_rectangle([(120, y_box), (960, y_box + 90)], radius=16, fill=(22, 26, 34, 230), outline=(50, 60, 80, 200), width=2)
        w_tm = d2.textbbox((0, 0), term, font=f_term)[2]
        d2.text(((1080 - w_tm) // 2, y_box + 22), term, font=f_term, fill=(230, 235, 245, 255))
        y_box += 115
        
    # Seta visual apontando para a rotulação
    d2.polygon([(540, 860), (510, 825), (570, 825)], fill=(217, 30, 54, 255))
    
    # Grande rótulo: O Inimigo Simbólico
    d2.rounded_rectangle([(80, 880), (1000, 1080)], radius=20, fill=(217, 30, 54, 240), outline=(255, 255, 255, 220), width=3)
    f_rot = get_font(56, bold=True)
    f_subrot = get_font(34, bold=True)
    rot_txt = "O INIMIGO SIMBÓLICO"
    rot_txt2 = "“IDEOLOGIA DE GÊNERO”"
    d2.text(((1080 - d2.textbbox((0, 0), rot_txt, font=f_rot)[2]) // 2, 915), rot_txt, font=f_rot, fill=(255, 255, 255, 255))
    d2.text(((1080 - d2.textbbox((0, 0), rot_txt2, font=f_subrot)[2]) // 2, 995), rot_txt2, font=f_subrot, fill=(255, 240, 240, 255))
    
    # Pergunta reflexiva
    q2 = "MAS QUAL É A VERDADEIRA AMEAÇA?"
    f_q2 = get_font(44, bold=True)
    w_q2 = d2.textbbox((0, 0), q2, font=f_q2)[2]
    d2.text(((1080 - w_q2) // 2, 1160), q2, font=f_q2, fill=(255, 215, 0, 255))
    
    c2.convert("RGB").save("assets/scenes/scene_02.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 3: A DISPUTA PELO PODER (Camila Galetti)
    # -------------------------------------------------------------
    c3 = Image.new("RGBA", (1080, 1920), (10, 12, 16, 255))
    d3 = ImageDraw.Draw(c3)
    draw_top_kicker(d3, "ANÁLISE SOCIOLÓGICA", y=180)
    
    d3.rounded_rectangle([(90, 290), (990, 480)], radius=18, fill=(18, 22, 30, 230), outline=(217, 30, 54, 150), width=2)
    f_c3_aut = get_font(44, bold=True)
    f_c3_sub = get_font(32, bold=False)
    d3.text((130, 330), "Profa. Dra. Camila Galetti", font=f_c3_aut, fill=(255, 255, 255, 255))
    d3.text((130, 395), "Pesquisadora e Socióloga (UnB)", font=f_c3_sub, fill=(180, 190, 205, 240))
    d3.text((130, 435), "Estudos de Gênero, Política e Relações de Poder", font=f_c3_sub, fill=(140, 150, 170, 230))
    
    # 4 Pilares Conceituais
    pilares = [
        ("FAMÍLIA", "Organização e controle social"),
        ("CORPO / SEXUALIDADE", "Autonomia vs. tutela moral"),
        ("AUTORIDADE", "Quem tem legitimidade de decisão"),
        ("PODER", "A disputa central pelas regras sociais")
    ]
    y_p = 530
    for titulo, desc in pilares:
        d3.rounded_rectangle([(90, y_p), (990, y_p + 115)], radius=16, fill=(20, 24, 32, 220), outline=(138, 43, 226, 160), width=2)
        d3.text((130, y_p + 20), titulo, font=get_font(40, bold=True), fill=(225, 35, 55, 255))
        d3.text((130, y_p + 68), desc, font=get_font(30, bold=False), fill=(200, 210, 225, 240))
        y_p += 145
        
    c3.convert("RGB").save("assets/scenes/scene_03.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 4: A CONTRADIÇÃO DO VOTO FEMININO
    # -------------------------------------------------------------
    c4 = apply_cinematic_grade(img_voto, darken=0.5)
    d4 = ImageDraw.Draw(c4)
    draw_top_kicker(d4, "DADOS OFICIAIS ELEITORAIS", y=180)
    
    # Painel Estatístico Oficial do TSE
    d4.rounded_rectangle([(90, 290), (990, 780)], radius=24, fill=(10, 14, 20, 235), outline=(0, 180, 136, 200), width=2)
    d4.text((140, 330), "TRIBUNAL SUPERIOR ELEITORAL (TSE)", font=get_font(34, bold=True), fill=(0, 200, 150, 255))
    
    # Número gigante 52.8%
    d4.text((140, 400), "52,8%", font=get_font(130, bold=True), fill=(255, 255, 255, 255))
    d4.text((140, 560), "DO ELEITORADO BRASILEIRO É FEMININO", font=get_font(40, bold=True), fill=(255, 215, 0, 255))
    d4.text((140, 630), "Mais de 82 milhões de eleitoras no país.", font=get_font(32, bold=False), fill=(190, 200, 215, 240))
    d4.text((140, 680), "Nenhum projeto político sobrevive ignorando seus votos.", font=get_font(30, bold=False), fill=(160, 175, 190, 220))
    
    # O dilema político
    d4.rounded_rectangle([(90, 830), (990, 1140)], radius=24, fill=(16, 20, 28, 235), outline=(217, 30, 54, 200), width=2)
    d4.text((130, 870), "O PARADOXO CONSERVADOR:", font=get_font(36, bold=True), fill=(217, 30, 54, 255))
    d4.text((130, 940), "• Votar e ocupar cargos?", font=get_font(38, bold=True), fill=(255, 255, 255, 255))
    d4.text((130, 1020), "• Desde que não questione os papéis tradicionais.", font=get_font(32, bold=False), fill=(220, 225, 235, 240))
    
    c4.convert("RGB").save("assets/scenes/scene_04.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 5: O ANTIFEMINISMO COMO INSTRUMENTO POLÍTICO
    # -------------------------------------------------------------
    c5 = apply_cinematic_grade(img_mob, darken=0.45)
    d5 = ImageDraw.Draw(c5)
    draw_top_kicker(d5, "ESTRATÉGIA DE MOBILIZAÇÃO", y=200)
    
    d5.rounded_rectangle([(90, 520), (990, 920)], radius=24, fill=(12, 14, 20, 235), outline=(217, 30, 54, 240), width=3)
    q5 = "O ANTIFEMINISMO É TAMBÉM"
    q5_2 = "UMA ESTRATÉGIA POLÍTICA?"
    w_q5 = d5.textbbox((0, 0), q5, font=get_font(52, bold=True))[2]
    w_q5_2 = d5.textbbox((0, 0), q5_2, font=get_font(56, bold=True))[2]
    d5.text(((1080 - w_q5) // 2, 600), q5, font=get_font(52, bold=True), fill=(255, 255, 255, 255))
    d5.text(((1080 - w_q5_2) // 2, 700), q5_2, font=get_font(56, bold=True), fill=(225, 35, 55, 255))
    
    c5.convert("RGB").save("assets/scenes/scene_05.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 6: O CORPO FEMININO COMO TERRITÓRIO DE DISPUTA
    # -------------------------------------------------------------
    c6 = apply_cinematic_grade(img_saude, darken=0.48)
    d6 = ImageDraw.Draw(c6)
    draw_top_kicker(d6, "DIREITOS & SAÚDE PÚBLICA", y=180)
    
    # Painel comparativo
    d6.rounded_rectangle([(90, 320), (990, 680)], radius=20, fill=(12, 16, 24, 235), outline=(0, 160, 220, 180), width=2)
    d6.text((140, 360), "TRATAMENTO DE SAÚDE PÚBLICA", font=get_font(38, bold=True), fill=(0, 190, 245, 255))
    d6.text((140, 440), "• Indicadores de mortalidade materna", font=get_font(32, bold=False), fill=(220, 230, 245, 240))
    d6.text((140, 510), "• Desigualdade social e racial no SUS", font=get_font(32, bold=False), fill=(220, 230, 245, 240))
    d6.text((140, 580), "• Autonomia e integridade reprodutiva", font=get_font(32, bold=False), fill=(220, 230, 245, 240))
    
    d6.rounded_rectangle([(90, 720), (990, 1080)], radius=20, fill=(20, 12, 14, 235), outline=(217, 30, 54, 200), width=2)
    d6.text((140, 760), "DESVIO PARA JULGAMENTO MORAL", font=get_font(38, bold=True), fill=(225, 35, 55, 255))
    d6.text((140, 840), "• Criminalização de vulnerabilidades", font=get_font(32, bold=False), fill=(245, 220, 220, 240))
    d6.text((140, 910), "• Instrumento de pânico moral e polarização", font=get_font(32, bold=False), fill=(245, 220, 220, 240))
    d6.text((140, 980), "• Tutela estatal sobre o corpo feminino", font=get_font(32, bold=False), fill=(245, 220, 220, 240))
    
    c6.convert("RGB").save("assets/scenes/scene_06.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 7: VIOLÊNCIA POLÍTICA CONTRA MULHERES
    # -------------------------------------------------------------
    c7 = apply_cinematic_grade(img_plenario, darken=0.55)
    d7 = ImageDraw.Draw(c7)
    draw_top_kicker(d7, "LEGISLAÇÃO BRASILEIRA", y=180)
    
    d7.rounded_rectangle([(90, 300), (990, 740)], radius=24, fill=(12, 14, 18, 240), outline=(217, 30, 54, 220), width=3)
    d7.text((130, 350), "VIOLÊNCIA POLÍTICA DE GÊNERO", font=get_font(44, bold=True), fill=(225, 35, 55, 255))
    d7.text((130, 430), "LEI FEDERAL Nº 14.192 / 2021", font=get_font(36, bold=True), fill=(255, 255, 255, 255))
    
    lei_desc = (
        "“Assediar, constranger, humilhar, perseguir ou ameaçar,\n"
        "por qualquer meio, candidata ou detentora de mandato\n"
        "eletivo, utilizando-se de menosprezo ou discriminação à\n"
        "condição de mulher...” (Art. 359-P do Código Eleitoral)"
    )
    d7.text((130, 510), lei_desc, font=get_font(28, bold=False), fill=(200, 210, 225, 240))
    
    # Alvos dos ataques
    d7.rounded_rectangle([(90, 780), (990, 1140)], radius=20, fill=(18, 20, 26, 235), outline=(138, 43, 226, 180), width=2)
    d7.text((130, 820), "FORMAS SISTEMÁTICAS DE ATAQUE:", font=get_font(34, bold=True), fill=(138, 43, 226, 255))
    d7.text((130, 890), "• Ataques à aparência física e sexualidade", font=get_font(32, bold=False), fill=(230, 235, 245, 240))
    d7.text((130, 960), "• Desqualificação da capacidade técnica e moral", font=get_font(32, bold=False), fill=(230, 235, 245, 240))
    d7.text((130, 1030), "• Intimidação para expulsão dos espaços decisórios", font=get_font(32, bold=False), fill=(230, 235, 245, 240))
    
    c7.convert("RGB").save("assets/scenes/scene_07.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 8: LIBERDADE PARA QUEM?
    # -------------------------------------------------------------
    c8 = apply_cinematic_grade(img_mob, darken=0.55)
    d8 = ImageDraw.Draw(c8)
    draw_top_kicker(d8, "CONVIVÊNCIA DEMOCRÁTICA", y=180, line_color=(255, 215, 0, 255))
    
    d8.rounded_rectangle([(90, 340), (990, 700)], radius=20, fill=(14, 18, 24, 235), outline=(70, 130, 180, 200), width=2)
    d8.text((130, 380), "CONVICÇÕES PESSOAIS (LEGÍTIMAS)", font=get_font(36, bold=True), fill=(135, 206, 250, 255))
    d8.text((130, 460), "• Crenças religiosas e tradições familiares", font=get_font(32, bold=False), fill=(210, 225, 245, 240))
    d8.text((130, 530), "• Escolhas e valores de vida individuais", font=get_font(32, bold=False), fill=(210, 225, 245, 240))
    d8.text((130, 600), "• Expressão e fé no âmbito privado e comunitário", font=get_font(32, bold=False), fill=(210, 225, 245, 240))
    
    d8.rounded_rectangle([(90, 750), (990, 1110)], radius=20, fill=(24, 12, 16, 235), outline=(217, 30, 54, 220), width=2)
    d8.text((130, 790), "IMPOSIÇÃO COMO RESTRIÇÃO DE DIREITOS", font=get_font(36, bold=True), fill=(225, 35, 55, 255))
    d8.text((130, 870), "• Transformar convicção privada em lei geral", font=get_font(32, bold=False), fill=(245, 220, 220, 240))
    d8.text((130, 940), "• Cercear a autonomia de outras pessoas", font=get_font(32, bold=False), fill=(245, 220, 220, 240))
    d8.text((130, 1010), "• Negar a cidadania plena e a liberdade de existir", font=get_font(32, bold=False), fill=(245, 220, 220, 240))
    
    c8.convert("RGB").save("assets/scenes/scene_08.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 9: O CENTRO DA DISPUTA
    # -------------------------------------------------------------
    c9 = Image.new("RGBA", (1080, 1920), (8, 10, 14, 255))
    d9 = ImageDraw.Draw(c9)
    draw_top_kicker(d9, "A PERGUNTA CRUCIAL", y=180)
    
    f_q9_title = get_font(58, bold=True)
    t_q9 = "QUEM TEM AUTORIDADE?"
    w_q9 = d9.textbbox((0, 0), t_q9, font=f_q9_title)[2]
    d9.text(((1080 - w_q9) // 2, 330), t_q9, font=f_q9_title, fill=(255, 255, 255, 255))
    
    perguntas = [
        "QUEM DECIDE SOBRE O CORPO?",
        "QUEM DECIDE SOBRE A VIDA?",
        "QUEM DECIDE SOBRE A LIBERDADE?"
    ]
    y_q = 480
    for p in perguntas:
        d9.rounded_rectangle([(90, y_q), (990, y_q + 130)], radius=20, fill=(18, 22, 30, 240), outline=(217, 30, 54, 200), width=2)
        w_p = d9.textbbox((0, 0), p, font=get_font(42, bold=True))[2]
        d9.text(((1080 - w_p) // 2, y_q + 40), p, font=get_font(42, bold=True), fill=(235, 240, 250, 255))
        y_q += 165
        
    c9.convert("RGB").save("assets/scenes/scene_09.jpg", "JPEG", quality=95)
    
    # -------------------------------------------------------------
    # CENA 10: ENCERRAMENTO
    # -------------------------------------------------------------
    # Imagem de mulher com fade suave para preto e pergunta final
    c10 = apply_cinematic_grade(img_mulher, darken=0.25)
    d10 = ImageDraw.Draw(c10)
    
    # Letreiro final em fade escuro
    d10.rectangle([(0, 1300), (1080, 1920)], fill=(6, 8, 12, 230))
    d10.line([(540 - 80, 1420), (540 + 80, 1420)], fill=(217, 30, 54, 255), width=4)
    
    tf1 = "QUEM TEM MEDO DA"
    tf2 = "LIBERDADE"
    tf3 = "DAS MULHERES?"
    
    f_tf = get_font(60, bold=True)
    f_tf_red = get_font(76, bold=True)
    
    w_tf1 = d10.textbbox((0, 0), tf1, font=f_tf)[2]
    w_tf2 = d10.textbbox((0, 0), tf2, font=f_tf_red)[2]
    w_tf3 = d10.textbbox((0, 0), tf3, font=f_tf)[2]
    
    d10.text(((1080 - w_tf1) // 2, 1460), tf1, font=f_tf, fill=(255, 255, 255, 255))
    d10.text(((1080 - w_tf2) // 2, 1540), tf2, font=f_tf_red, fill=(225, 35, 55, 255))
    d10.text(((1080 - w_tf3) // 2, 1640), tf3, font=f_tf, fill=(255, 255, 255, 255))
    
    c10.convert("RGB").save("assets/scenes/scene_10.jpg", "JPEG", quality=95)
    
    print("Todas as 10 bases cênicas geradas com sucesso em assets/scenes/!")

if __name__ == "__main__":
    generate_all_scenes()
