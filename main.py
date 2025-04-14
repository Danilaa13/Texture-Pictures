import asyncio
from EGGER.EGGER import egger_download_images_from_page
from NORDECO.NORDECO import nordeco_download_images_from_page
from KRONOSPAN.KRONOSPAN import kronospan_download_images_from_page
from MIXIN.mixin_save import save_images

async def main():
    """Выбери один из источников, раскомментировав нужное"""

    # __EGGER__
    # url = 'https://egger-russia.ru/furniture-interior-design/'
    # image_urls = await egger_download_images_from_page(url)
    # await save_images(image_urls, folder="EGGER/EGGER_images")  ## <- указать путь / сохранения папки с картинками и название


    # __NORDECO__
    # url = 'https://nordeco.design/katalog-dekorov/filter/clear/apply/'
    # image_urls = await nordeco_download_images_from_page(url)
    # await save_images(image_urls, folder="NORDECO/NORDECO_images")

    # __KRONOSPAN__
    # url = 'https://kronospan.com/ru_RU/decors/by_collection/kronodesign/'
    # image_urls = await kronospan_download_images_from_page(url)
    # await save_images(image_urls, folder="KRONOSPAN/KRONOSPAN_images")

if __name__ == '__main__':
    asyncio.run(main())
