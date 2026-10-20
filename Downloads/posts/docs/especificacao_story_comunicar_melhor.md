# Documentação Técnica e Direção de Arte: Story "Um Primeiro Passo para se Comunicar Melhor"

**Cliente:** Sônia Torres | Fonoaudióloga (CRFª 1-17701)  
**Perfil:** [@torresdafono](https://instagram.com/torresdafono)  
**Formato:** Instagram Story (1080 x 1920 px / Proporção 9:16)  
**Objetivo:** Topo de funil humanizado, gerando autoridade clínica e direcionando potenciais pacientes para conhecer as modalidades de atendimento (consultório e domiciliar).

---

## 1. Arquitetura e Decisões de Design

### 1.1 Substituição da Personagem Principal
- **Foto Real de Alta Fidelidade:** Substituição de ilustrações artificiais ou imagens geradas por IA pela fotografia real da Dra. Sônia Torres em consultório clínico.
- **Enquadramento de Respiro Superior:** A foto foi posicionada estrategicamente a partir de $y = 440\text{ px}$, estendendo o topo com continuidade visual (madeira e parede neutra) para evitar que o título e elementos institucionais cobrissem o rosto, olhos ou jaleco da profissional.
- **Overlays Gradientes de Contraste AAA:**
  - *Gradiente Superior:* Café escuro translúcido ($y = 0$ até $680\text{ px}$), garantindo legibilidade nítida do gancho principal sem escurecer o semblante da especialista.
  - *Gradiente Inferior:* Transição suave na base para ancoragem do card e botão de ação.
  - *Warm Tint:* Camada sutil em tom terracota translúcido para harmonizar as temperaturas de cor.

### 1.2 Tipografia e Correção Ortográfica
- **Gancho Superior:**  
  - Linha 1: `"Um primeiro passo"` — Georgia Bold, 58px, Branco `#FFFFFF` com drop shadow sutil.
  - Linha 2: `"para se comunicar melhor"` — Georgia Italic, 58px, Ouro Champagne `#DCB88A` para destaque editorial elegante.
- **Bloco Central (Card Translúcido):**  
  - Fundo café semi-opaco translúcido (`rgba(26, 20, 18, 0.85)`) com borda sutil champanhe (`rgba(220, 184, 138, 0.55)`).
  - Micro-tag de reforço: `"CUIDADO ESPECIALIZADO & ACOLHEDOR"`.
  - Texto central com ortografia devidamente corrigida:  
    `"Atendimento fonoaudiológico para crianças, adultos e idosos, em consultório ou em domicílio no Rio de Janeiro."`  
    *(Destaque para o acento agudo correto na palavra "domicílio")*.
- **Call-to-Action (CTA):**  
  - Botão pílula em Terracota Institucional (`#C27D60`) com tipografia Segoe UI Bold 32px e chevron indicador: `"Conheça as opções >"`.

### 1.3 Safe Zones do Instagram Stories
- **Topo:** Margem de segurança de $220\text{ px}$ para não colidir com o cabeçalho do Instagram (foto de perfil, username e botão 'X').
- **Rodapé:** Margem de segurança inferior de $245\text{ px}$ para garantir que a barra de resposta/direct não sobreponha a CTA nem a assinatura.

---

## 2. Fluxo de Dados e Renderização

```
[assets/sonia_torres_real.jpg]
              │
              ▼
   [scripts/gerar_story_comunicar_melhor.py]
   ├── Redimensionamento Lanczos (1160x1740)
   ├── Extensão de Topo Atmosférica (Gaussian Blur)
   ├── Aplicação de Overlays de Contraste
   ├── Composição Tipográfica (Georgia & Segoe UI)
   ├── Renderização de Card Translúcido & Botão CTA
   └── Exportação em Alta Resolução (Quality 98)
              │
              ├──► um-primeiro-passo-para-se-comunicar-melhor.jpg (Raiz)
              └──► posts_finais/story_um_primeiro_passo_para_se_comunicar_melhor.jpg (Backup)
```

---

## 3. Como Manter e Replicar a Funcionalidade

Para gerar novamente a imagem ou alterar textos:
1. Abra o arquivo [scripts/gerar_story_comunicar_melhor.py](file:///c:/Users/Gamer/Downloads/posts/scripts/gerar_story_comunicar_melhor.py).
2. Atualize os textos nas variáveis `body_text`, `hook_part1`, `hook_part2` ou `cta_label`.
3. Execute o comando no terminal:
   ```bash
   python scripts/gerar_story_comunicar_melhor.py
   ```
4. A peça final será gerada instantaneamente mantendo todas as proporções, pesos e padrões estéticos da marca.
