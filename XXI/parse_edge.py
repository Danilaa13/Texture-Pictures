import re

def parse_edge_band(title):

    units_of_measurement = 'пог.м'

    # 1. Извлекаем размеры (длина*ширина*толщина)
    size_pattern = r'(\d+[.,]?\d*)\s*[/\*,]\s*(\d+[.,]?\d*)'  # Учитываем запятые, * и мм
    size_match = re.search(size_pattern, title)

    thickness, width = '', ''
    if size_match:
        first = float(size_match.group(1).replace(',', '.'))  # Преобразуем в float
        second = float(size_match.group(2).replace(',', '.'))  # Преобразуем в float

        # Определяем, что есть что (толщина всегда < ширины)
        thickness, width = (first, second) if first < second else (second, first)

    # Преобразуем ширину в int, если число целое
    if width and width.is_integer():
        width = int(width)

    # 2. Извлекаем код (либо 3 или 4 цифры, либо комбинация букв и цифр)
    code_pattern = re.compile(
        # r'\b(?:\d{3,4}-?[A-ZА-Я0-9]{3}|\d{3,4}|[а-яА-Яa-zA-Z]{2,}-?[A-Z0-9]{2,}|\S+-\S+|[a-zA-Z0-9.-]{5,8})\b'
          r'\b(?:[A-ZА-Я0-9]\d{3,4}-?\s?[A-ZА-Я0-9]{3}|\d{3,4}|[а-яА-Яa-zA-Z]\d{2,3}|[a-zA-Z]{1,2}\.\d{3}\.[A-Z0-9]{2,3}|[a-zA-Z0-9.-]{5,8})\b'

)  # Код: либо 3-4 цифры, либо комбинация букв и цифр
    code_match = re.search(code_pattern, title)
    code = code_match.group(0) if code_match else ''

    if  'PVC' in title:
        # Дополнительный паттерн для кода вида "К001 - 500028W"
        alt_code_pattern = re.compile(r'\b(\S+)\s*-\s*([A-Za-z0-9]+)\b')
        alt_code_match = re.search(alt_code_pattern, title)
        if alt_code_match:
            if alt_code_match.group(1) and alt_code_match.group(2):
                code = alt_code_match.group(1) + ' - ' + alt_code_match.group(2)  # Объединяем части кода

    # 3. Извлекаем структуру (например, PE, SM, BS, но без группы)
    structure_pattern = re.compile(r'\b([A-ZА-Я]{1,2})\b')    # Структура: 1 или 2 заглавных латинских буквы
    structure_match = re.search(structure_pattern, title)
    structure = structure_match.group(0) if structure_match else ''

    if structure and code and re.search(r'\b' + re.escape(structure) + r'\b', code):
        structure = ''

    # Исключаем из структуры, если это часть группы (GP, SPAN, РБ и т.д.)
    if structure in ['GP', 'SPAN', 'PVC', 'Алтайлес']:
        structure = ''


    # 4. Извлекаем группу (GP, SPAN, РБ, Алтайлес)
    group_pattern = re.compile(r'\b(PVC|GP|SPAN|Алтайлес|Galoplast)\b')  # Группа заглавными латинскими буквами
    group_match = re.search(group_pattern, title)
    group = group_match.group(0) if group_match else ''

    # . Извлекаем тип материала (ЛМДФ, ХДФ, Кромка ABS, Кромка ПВХ)
    material_pattern = re.compile(r'\b(ЛДСП|ЛМДФ|ХДФ|Кромка ABS|Кромка ПВХ|кромка)\b', re.IGNORECASE)
    material_match = material_pattern.search(title)
    material = material_match.group(0) if material_match else ''


    # 5. Формируем имя (убираем размеры, код, структуру и группу)
    name = re.sub(size_pattern, '', title).strip()  # Убираем размеры
    if code:
        name = name.replace(code, '').strip()  # Убираем код
    if structure:
        name = name.replace(structure, '').strip()  # Убираем структуру
    if group:
        name = name.replace(group, '').strip()  # Убираем группу
    if material:
        name = re.sub(r'\b' + re.escape(material) + r'\b', '', name).strip()

    # Убираем двойные пробелы
    name = re.sub(r'\s+', ' ',  name).strip()
    name = re.sub(r'\bмм\b', '', name).strip()
    name = name.rstrip(',')

    full_name = f'{code} {name}'.strip()

    return full_name