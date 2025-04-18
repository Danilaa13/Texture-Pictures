import os
import pandas as pd


def add_texture_column_to_excel(
        excel_path,
        output_path,
        image_folder
):
    """Добавляет колонку 'Текстура' в Excel-файл, основываясь на совпадении артикулов с изображениями."""

    if not os.path.exists(excel_path):
        print(f"❌ Excel файл не найден: {excel_path}")
        return

    if not os.path.isdir(image_folder):
        print(f"❌ Папка с изображениями не найдена: {image_folder}")
        return

    print(f"📥 Загружаем данные из Excel: {excel_path}")
    data = pd.read_excel(excel_path, engine='openpyxl')

    def find_image_by_article(row):
        article = str(row['Идентификатор для синхронизации']).strip()

        for root, dirs, files in os.walk(image_folder):
            for file in files:
                if article in file and file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    relative_path = os.path.relpath(os.path.join(root, file), image_folder)
                    return f"\\IMAGES\\{relative_path}"

        return "Фото не найдено"

    print("🔎 Ищем изображения по идентификатору...")
    data['Текстура'] = data.apply(find_image_by_article, axis=1)

    data.to_excel(output_path, index=False, engine='openpyxl')
    print(f"✅ Файл успешно сохранён как: {output_path}")
