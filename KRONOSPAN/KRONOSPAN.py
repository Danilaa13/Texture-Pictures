import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright, TimeoutError
from MIXIN.mixin_log import log_with_time

async def kronospan_download_images_from_page(url: str) -> dict[str: str]:
    async with async_playwright() as playwright:
        print(log_with_time('Запускаем браузер'))
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()


        try:
            print(log_with_time(f'Открыта страница: {url}'))
            await page.goto(url, wait_until='domcontentloaded', timeout=180000)
            print(log_with_time('Страница загружена, начинаем обработку'))


            await page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
            await asyncio.sleep(2)


            collection_cards = await page.query_selector_all('div.collection-image')
            if not collection_cards:
                print(log_with_time('Не удалось найти коллекции на странице. Попробуем подождать еще немного...'))
                await asyncio.sleep(5)
                collection_cards = await page.query_selector_all('div.collection-image')
            print(log_with_time(f'Найдено {len(collection_cards)} коллекций для обработки.'))

            image_urls = {}

            for index, card in enumerate(collection_cards):
                print(log_with_time(f'👉 Кликаем по коллекции {index + 1}/{len(collection_cards)}'))
                await card.click()
                await asyncio.sleep(3)
                print(log_with_time(f'Коллекция {index + 1} открыта, начинаем сбор изображений.'))

                await page.wait_for_selector('div.collections-item.ng-scope', timeout=10000)
                decor_items = await page.query_selector_all('div.collections-item.ng-scope')

                print(log_with_time(f'Найдено {len(decor_items)} изображений декоров в коллекции.'))

                for decor in decor_items:

                    decor_number_el = await decor.query_selector('span.decor-number.ng-binding')
                    decor_title_el = await decor.query_selector('span.decor-title.ng-binding')
                    texture_els = await decor.query_selector_all('div.ng-binding.ng-scope')

                    if not decor_number_el or not decor_title_el:
                        continue

                    decor_number = await decor_number_el.inner_text()
                    decor_title = await decor_title_el.inner_text()
                    textures = [await tex.inner_text() for tex in texture_els]

                    texture_str = ''.join(textures)
                    full_name = f"{decor_number} {texture_str} {decor_title}".strip()

                    img = await decor.query_selector('img')
                    if img:
                        src = await img.get_attribute('src')
                        if src:
                            full_url = urljoin(url, src)
                            image_urls[full_name] = full_url
                            print(log_with_time(f'🖼️ {full_name} => {full_url}'))



            await browser.close()
            print(log_with_time(f'Обработка завершена. Найдено изображений: {len(image_urls)}'))
            return image_urls



        except TimeoutError:
            print(log_with_time('❌ Таймаут при загрузке страницы. Проверь соединение или доступность сайта.'))
            await browser.close()
            return []
