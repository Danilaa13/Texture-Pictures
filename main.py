import asyncio
from EGGER.EGGER import egger_download_images_from_page
from NORDECO.NORDECO import nordeco_download_images_from_page
from KRONOSPAN.KRONOSPAN import kronospan_download_images_from_page
from MIXIN.mixin_save import save_images
from SERVER.SERVER import fetch_category_links, server_navigate_and_scrape
from SERVER.Excel import  add_texture_column_to_excel



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


    # __SERVER__
    url = "https://www.tdserver.ru/catalog/"
    category_links = await fetch_category_links(url)
    brand_images = await server_navigate_and_scrape(category_links)

    for brand, images in brand_images.items():
        if images:
            folder_name = f"IMAGES/{brand}"
            print(f"💾 Сохраняем изображения для {brand} в папку: {folder_name}")
            await save_images(images, folder=folder_name)

    excel_path = r'E:\pythonProjectsForUniversity\WORK\PARS_PICTURES\tdserver.xlsx'
    output_path = r'E:\pythonProjectsForUniversity\WORK\PARS_PICTURES\tdserver_new.xlsx'
    image_folder =  r'E:\pythonProjectsForUniversity\WORK\PARS_PICTURES\IMAGES'

    add_texture_column_to_excel(excel_path, output_path, image_folder)


if __name__ == '__main__':
    asyncio.run(main())
