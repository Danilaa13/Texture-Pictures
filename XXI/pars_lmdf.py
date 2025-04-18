import re


def parse_lmdf(title):

    units_of_measurement = 'лист'

    # Регулярные выражения для извлечения данных
    size_pattern = re.compile(r'(\d+)\*(\d+)\*(\d+)')  # Размеры (длина*ширина*толщина)
    code_pattern = re.compile(r'\b\d{3,4}\b')  # Код из 3 цифр
    structure_pattern = re.compile(r'\b([A-ZА-Я]{1,2})\b')  # Структура из 2 латинских букв
    group_pattern = re.compile(r'\b(SPAN|KST|Алтайлес|GP)\b')  # Группа заглавными латинскими буквами

    # 1. Извлекаем размеры
    dimensions_match = size_pattern.search(title)
    if dimensions_match:
        length = int(dimensions_match.group(1))  # Длина
        width = int(dimensions_match.group(2))  # Ширина
        thickness = int(dimensions_match.group(3))  # Толщина
    else:
        length = width = thickness = ''

    # 2. Извлекаем код (3 цифры)
    code_match = code_pattern.search(title)
    code = code_match.group(0) if code_match else ''

    # 3. Извлекаем структуру (2 латинские буквы)
    structure_match = structure_pattern.search(title)
    structure = structure_match.group(0) if structure_match else ''

    # 4. Извлекаем группу (например, "SPAN")
    group_match = group_pattern.search(title)
    group = group_match.group(0) if group_match else ''

    # . Извлекаем тип материала (ЛМДФ, ХДФ, Кромка ABS, Кромка ПВХ)
    material_pattern = re.compile(r'\b(ЛДСП|ЛМДФ|ХДФ|Кромка ABS|Кромка ПВХ)\b', re.IGNORECASE)
    material_match = material_pattern.search(title)
    material = material_match.group(0) if material_match else ''

    # 5. Формируем имя (убираем код, структуру, размеры и группу)
    name = title
    if code:
        name = re.sub(r'\b' + code + r'\b', '', name)  # Убираем код
    if structure:
        name = re.sub(r'\b' + structure + r'\b', '', name)  # Убираем структуру
    if group:
        name = re.sub(r'\b' + group + r'\b', '', name)  # Убираем группу
    if material:
        name = re.sub(r'\b' + re.escape(material) + r'\b', '', name).strip()
    name = re.sub(size_pattern, '', name)  # Убираем размеры
    name = re.sub(r'\s+', ' ', name).strip()  # Убираем лишние пробелы

    full_name = f'{code} {name}'.strip()

    return full_name
