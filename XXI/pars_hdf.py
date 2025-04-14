import re


def parse_hdf(title):

    units_of_measurement = 'лист'

    # Регулярные выражения для извлечения данных
    # Код: либо 3 или 4 цифры, либо комбинация букв и цифр
    code_pattern = re.compile(r'\b(\d{3,4}|\w{1,4}\d{1,4})\b')  # Код: 3 или 4 цифры, либо комбинация букв и цифр

    size_pattern = re.compile(r'(\d+)\*(\d+)\*(\d+)')  # Размеры (длина*ширина*толщина)

    structure_pattern = re.compile(r'\b([A-ZА-Я]{1,2})\b')   # Структура: 1 или 2 латинские заглавные буквы

    group_pattern = re.compile(r'\b(РБ|GP|SPAN|Алтайлес)\b')  # Группа заглавными латинскими буквами

    # 1. Извлекаем размеры (делаем это перед проверкой кода)
    dimensions_match = size_pattern.search(title)
    if dimensions_match:
        length, width, thickness = map(int, dimensions_match.groups())
    else:
        length = width = thickness = ''

    # 2. Извлекаем код (исключая совпадения с размерами)
    code_match = ''
    for match in re.finditer(code_pattern, title):
        potential_code = match.group(0)
        if potential_code not in map(str, [length, width, thickness]):  # Проверяем, что код ≠ размерам
            code_match = potential_code
            break

    code = code_match if code_match else ''

    # 3. Извлекаем структуру (1 или 2 латинские заглавные буквы)
    structure_match = structure_pattern.search(title)
    structure = structure_match.group(0) if structure_match else ''

    # 4. Извлекаем группу
    group_match = group_pattern.search(title)
    group = group_match.group(0) if group_match else ''

    # . Извлекаем тип материала (ЛМДФ, ХДФ, Кромка ABS, Кромка ПВХ)
    material_pattern = re.compile(r'\b(ЛДСП|ЛМДФ|ХДФ|Кромка ABS|Кромка ПВХ)\b', re.IGNORECASE)
    material_match = material_pattern.search(title)
    material = material_match.group(0) if material_match else ''


    # 5. Формируем имя: оставляем только слова (удаляем все числа и ненужные символы)
    name = title
    if code:
        name = re.sub(r'\b' + re.escape(code) + r'\b', '', name)  # Убираем код
    if structure:
        name = re.sub(r'\b' + re.escape(structure) + r'\b', '', name)  # Убираем структуру
    if group:
        name = re.sub(r'\b' + re.escape(group) + r'\b', '', name)  # Убираем группу
    if material:
        name = re.sub(r'\b' + re.escape(material) + r'\b', '', name).strip()
    name = re.sub(size_pattern, '', name)  # Убираем размеры
    name = re.sub(r'\s+', ' ', name).strip()  # Убираем лишние пробелы
    name = re.sub(r'[^а-яА-Яa-zA-Z\s]', '', name)  # Оставляем только буквы и пробелы (удаляем все остальное)

    # Убираем одиночные символы, такие как "К" и "мм"
    name = re.sub(r'\bК\b|\bмм\b', '', name).strip()  # Убираем "К" и "мм"

    full_name = f'{name} {code} {structure}'.strip()

    return full_name