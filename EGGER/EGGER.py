from urllib.parse import urljoin
from playwright.async_api import async_playwright

from MIXIN.mixin_log import log_with_time
from MIXIN.mixin_scroll import scroll_until_show_more



async def egger_download_images_from_page(url: str) -> dict[str: str]:
    async with async_playwright() as playwright:
        print(log_with_time('Запускаем браузер'))
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        print(log_with_time('Переходим на страницу'))
        await page.goto(url, timeout=60000)
        print(log_with_time('Прокручиваем страницу и нажимаем "Показать больше" до тех пор, пока кнопка не исчезнет'))
        await scroll_until_show_more(page)
        print(log_with_time('Ищем все изображения на странице'))

        image_urls = {}

        items = await page.query_selector_all('a.item.item--is_prod-example')

        for item in items:

            decor_title_el = await item.query_selector('span.d-sm-none.mb-5xs.fz-s.color-txt-2')
            decor_number_el = await item.query_selector('span.fw-500.fz-l.fz-md-m.fz-sm-s.color-txt')

            decor_title = await decor_title_el.inner_text()
            decor_number = await decor_number_el.inner_text()
            code = decor_number.split()[0]

            full_name = f"{code} {decor_title}".strip()

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

