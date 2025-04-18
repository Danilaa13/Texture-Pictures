from playwright.async_api import async_playwright
from collections import defaultdict
from MIXIN.mixin_save import save_images
from SERVER.pars_title_products import parse_title


async def scroll_until_show_more(page):
    """Прокручивает страницу и нажимает 'Показать ещё', пока кнопка существует."""
    while True:
        await page.evaluate('window.scrollBy(0, window.innerHeight);')
        print('Проверяем наличие кнопки "Показать ещё"...')
        show_more_button = await page.query_selector('a.js-ax-show-more-pagination')
        if show_more_button:
            print('Кнопка найдена, кликаем и ждём...')
            await show_more_button.click()
            await page.wait_for_timeout(2000)
        else:
            print('Кнопка "Показать ещё" больше не найдена.')
            break


async def fetch_category_links(url):
    TARGET_NAMES = [
        "Egger Perfect Sense/Perfect Mat",
        "Декоративные панели на основе МДФ",
        "Плиты TSS",
        "Столешницы Slotex (Слотекс)",
        "Столешницы АМК-Троя",
        "Плинтус для столешниц",
        "Планки для мебельных щитов",
        "Кромка ABS для столешниц",
        "ХДФ",
        "Кромка ПВХ Galoplast"
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Ждем, пока элементы подкатегорий загрузятся
        await page.wait_for_selector("div.category")

        # Извлекаем ссылки на подкатегории
        filtered_links = await page.evaluate(f"""
                    () => {{
                        const targets = {TARGET_NAMES};
                        const links = [];
                        const items = document.querySelectorAll('.category-products-list li a');
                        items.forEach(item => {{
                            const text = item.innerText.trim();
                            const href = item.getAttribute('href');
                            if (
                                href &&
                                href.split('/').filter(x => x).length > 2 &&
                                targets.includes(text)
                            ) {{
                                links.push({{ name: text, url: 'https://www.tdserver.ru' + href }});
                            }}
                        }});
                        return links;
                    }}
                """)

        await browser.close()
        print("📁 Найдено ссылок:", len(filtered_links))
        return filtered_links



async def fetch_product_data(page):

    await page.wait_for_selector(".product")

    print("🔍Начинаем извлечение данных о товарах...")

    raw_products = await page.evaluate("""
        () => {
             const results = [];
            const items = document.querySelectorAll('.product');

            items.forEach(item => {
                const title = item.querySelector('a.product_title')?.innerText.trim() || 'Без названия';
                const code = item.querySelector('div.product_code strong.value')?.innerText.trim() || 'Без кода';
                const img = item.querySelector('img.item_img')?.getAttribute('src') || '';
                
                if (img) {
                    results.push({
                        code: code,
                        title: title,
                        name: title,
                        image: 'https://www.tdserver.ru' + img
                    });
                }
            });

            return results;
        }
    """)
    products = []
    for product in raw_products:
        parsed_name = parse_title(product['name'])
        print(parsed_name)
        products.append({
            'title': product['title'],
            'name': f"{product['code']} - {parsed_name}",
            'image': product['image']
        })

    print(f"✅Извлечено товаров: {len(products)}")
    return products



async def server_navigate_and_scrape(category_links):
    brand_dicts = {
        "AGT": {},
        "АМК-Троя": {},
        "ARKOPA": {},
        "CLEAF": {},
        "Egger": {},
        "ETERNO": {},
        "EVOGLOSS": {},
        "Galoplast": {},
        "Slotex": {},
        "SMart": {},
        "Thermoplast": {},
        "ХДФ": {},
        "Прочее": {}
    }


    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for category in category_links:
            print(f"Собираем данные с подкатегории: {category['name']} → {category['url']}")
            await page.goto(category['url'])
            await page.wait_for_selector('.product')

            # Проверяем, есть ли кнопка "Показать ещё"
            show_more_button = await page.query_selector('a.js-ax-show-more-pagination')
            if show_more_button:
                await scroll_until_show_more(page)
            else:
                print('Кнопки "Показать ещё" нет — собираем всё с первой страницы.')

            products = await fetch_product_data(page)

            for product in products:
                name = product.get("name")
                img = product.get("image")
                title = product.get("title", "")
                matched = False

                for brand in brand_dicts:
                    if brand != "Прочее" and brand.lower() in title.lower():
                        brand_dicts[brand][name] = img
                        matched = True
                        break

                if not matched:
                    brand_dicts["Прочее"][name] = img


        await browser.close()

    return brand_dicts
