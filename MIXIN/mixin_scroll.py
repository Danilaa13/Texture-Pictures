from MIXIN.mixin_log import log_with_time




async def scroll_until_show_more(page):
    """Прокручивает страницу и нажимает 'Показать больше', пока кнопка существует."""
    while True:
        await page.evaluate('window.scrollBy(0, window.innerHeight);')
        print(log_with_time('Проверяем наличие кнопки "Показать больше"...'))
        show_more_button = await page.query_selector('button.js-page-navigation-next')
        if show_more_button:
            print(log_with_time('Кнопка найдена, кликаем и ждём...'))
            await show_more_button.click()
            await page.wait_for_timeout(2000)
        else:
            print(log_with_time('Кнопка "Показать больше" больше не найдена.'))
            break