from urllib.parse import urljoin
from playwright.async_api import async_playwright

from MIXIN.mixin_log import log_with_time



async def nordeco_download_images_from_page(url: str) -> dict[str: str]:
    async with async_playwright() as playwright:
        print(log_with_time('Запускаем браузер'))
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        print(log_with_time('Переходим на страницу'))
        await page.goto(url,  timeout=60000)
        print(log_with_time('Ищем все изображения на странице'))

        image_urls = {}

        items = await page.query_selector_all('div.product-card-col.v21-product-card-col')

        for item in items:

            decor_title_el = await item.query_selector('span.product-card-title')
            decor_title = await decor_title_el.inner_text()

            full_name = f"{decor_title}".strip()
            print(full_name)

            img = await item.query_selector('img')
            if img:
                src = await img.get_attribute('src')
                if src:
                    full_url = urljoin(url, src)
                    image_urls[full_name] = full_url
                    print(log_with_time(f'🖼️ {full_name} => {full_url}'))

        await browser.close()
        print(log_with_time(f'Найдено изображений: {len(image_urls)}'))
        return image_urls