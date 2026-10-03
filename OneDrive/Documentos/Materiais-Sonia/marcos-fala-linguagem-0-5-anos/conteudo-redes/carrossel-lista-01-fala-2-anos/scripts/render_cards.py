import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def render_all_slides():
    workspace_dir = Path(__file__).resolve().parent.parent
    templates_dir = workspace_dir / "templates-editaveis"
    output_dir = workspace_dir / "cards-publicacao"
    output_dir.mkdir(parents=True, exist_ok=True)

    slide_files = sorted([f for f in templates_dir.glob("slide-*.html")])
    if not slide_files:
        print("Nenhum template encontrado em templates-editaveis/")
        return

    print(f"Encontrados {len(slide_files)} slides para renderizar...")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Viewport exato do Instagram Portrait (1080x1350)
        page = await browser.new_page(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=1
        )

        for slide_path in slide_files:
            slide_name = slide_path.stem
            out_file = output_dir / f"{slide_name}.png"
            
            # Carregar arquivo com protocolo file://
            file_url = slide_path.as_uri()
            print(f"Renderizando {slide_name}...")
            
            await page.goto(file_url, wait_until="networkidle")
            # Esperar renderização das fontes e imagens
            await page.wait_for_timeout(600)
            
            # Captura de tela exata do slide
            await page.screenshot(
                path=str(out_file),
                clip={"x": 0, "y": 0, "width": 1080, "height": 1350}
            )
            print(f"Salvo: {out_file} (1080x1350)")

        await browser.close()

    print(f"\nSucesso! Todos os {len(slide_files)} cards foram exportados para: {output_dir}")

if __name__ == "__main__":
    asyncio.run(render_all_slides())
