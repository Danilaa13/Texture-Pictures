import os
import aiohttp
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
from MIXIN.mixin_log import log_with_time


def safe_filename(title: str) -> str:
    forbidden = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in forbidden:
        title = title.replace(char, ' ')
    return title.strip()

async def save_images(image_urls: dict[str, str], folder: str = "images"):
    os.makedirs(folder, exist_ok=True)

    count = 0
    async with aiohttp.ClientSession() as session:
        for title, url in image_urls.items():
            parsed_url = urlparse(url)

            VALID_EXTENSIONS = ('.webp', '.jpg', '.jpeg', '.png')
            if not parsed_url.path.lower().endswith(VALID_EXTENSIONS):
                print(log_with_time(f'Пропускаем URL, так как это не изображение: {url}'))
                continue

            if "google" in parsed_url.netloc or "imgur" in parsed_url.netloc:
                print(log_with_time(f'Пропускаем сторонний источник: {url}'))
                continue

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_data = await response.read()

                        image = Image.open(BytesIO(image_data))
                        clean_title = safe_filename(title)
                        filename = os.path.join(folder, f'{clean_title}.png')
                        image.save(filename, 'PNG')
                        count += 1
                        print(log_with_time(f'✅ Сохранено {count}: {filename}'))
                    else:
                        print(log_with_time(f'Ошибка загрузки: {url} (status {response.status})'))
            except Exception as e:
                print(log_with_time(f'Ошибка при скачивании {url}: {e}'))
