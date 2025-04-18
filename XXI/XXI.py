import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from pars_ldsp import parse_ldsp
from pars_lmdf import parse_lmdf
from pars_hdf import parse_hdf
from parse_edge import parse_edge_band
from MIXIN.mixin_save import save_images  # это async функция

BASE_URL = 'https://21vekst.ru'


async def scroll_until_show_more(page):
    while True:
        await page.evaluate('window.scrollBy(0, window.innerHeight);')
        show_more_button = await page.query_selector('span.more_text_ajax.font_upper_md')
        if show_more_button:
            await show_more_button.click()
            await page.wait_for_timeout(2000)
        else:
            break


async def collect_products(page):
    data = {}

    product_elements = await page.query_selector_all(
        'div.col-lg-3.col-md-4.col-sm-6.col-xs-6.col-xxs-12.item.item-parent.catalog-block-view__item.js-notice-block.item_block'
    )

    for product in product_elements:
        product_image = await product.query_selector('a.thumb img')
        if not product_image:
            continue

        image_src = await product_image.get_attribute('data-src') or await product_image.get_attribute('src')
        if not image_src or image_src.startswith('data:image/') or 'noimage_product.svg' in image_src:
            continue

        full_url = urljoin(BASE_URL, image_src)

        product_title = await product.query_selector(
            'a.dark_link.js-notice-block__title.option-font-bold.font_sm span'
        )
        title = await product_title.inner_text() if product_title else 'Не найдено'

        if not any(keyword in title for keyword in ['GP', 'Galoplast', 'SPAN']):
            continue

        print(f'{title}')

        if '/catalog/mebelnye_plity/ldsp/' in page.url:
            parsed_data = parse_ldsp(title)
        elif '/catalog/mebelnye_plity/lmdf/' in page.url:
            parsed_data = parse_lmdf(title)
        elif '/catalog/mebelnye_plity/khdf/' in page.url:
            parsed_data = parse_hdf(title)
        elif '/catalog/kromka_pvkh/' in page.url:
            parsed_data = parse_edge_band(title)
        else:
            continue

        data[parsed_data] = full_url
        print(f'Товар: {parsed_data} добавлен в словарь')

    return data


async def main():
    total_count = 0
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                await page.goto(BASE_URL, timeout=60000)
                await page.wait_for_load_state('load')
            except Exception as e:
                print(f"[Ошибка загрузки BASE_URL]: {e}")
                return

            for link in ['/catalog/mebelnye_plity/lmdf/', '/catalog/mebelnye_plity/khdf/', '/catalog/mebelnye_plity/ldsp/']:
                full_link = BASE_URL + link
                try:
                    await page.goto(full_link, timeout=60000)
                    await page.wait_for_load_state('load')
                except Exception as e:
                    print(f"[Ошибка загрузки категории]: {full_link} — {e}")
                    continue

                kronospan_link = await page.query_selector('a.thumb[href*="kronospan"]')
                if kronospan_link:
                    await kronospan_link.click()
                    await page.wait_for_load_state('load')

                    await scroll_until_show_more(page)
                    products = await collect_products(page)
                    await save_images(products, folder="E:\\pythonProjectsForUniversity\\WORK\\PARS_PICTURES\\KRONOSPAN\\KRONOSPAN_images_1")# <- указать путь / сохранения папки с картинками и название

                    print(f"🔍 Найдено товаров в категории {link}: {len(products)}")
                    total_count += len(products)

            try:
                await page.goto(BASE_URL + '/catalog/kromka_pvkh/', timeout=60000)
                await page.wait_for_load_state('load')
                # await scroll_until_show_more(page)
                products = await collect_products(page)
                # await save_images(products, folder="XXI_кромка")# <- указать путь / сохранения папки с картинками и название

                print(f"🔍 Найдено товаров в категории кромка ПВХ: {len(products)}")
                total_count += len(products)

            except Exception as e:
                print(f"[Ошибка загрузки категории кромки]: {e}")

    except Exception as e:
        print(f"[Общая ошибка Playwright]: {e}")
    finally:
        try:
            await browser.close()
        except Exception as e:
            print(f"[Ошибка при закрытии браузера]: {e}")


# Запуск
if __name__ == '__main__':
    asyncio.run(main())

