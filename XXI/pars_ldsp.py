import re

def parse_ldsp(title):

    units_of_measurement = 'лист'

    # 1. Извлекаем размеры (2800*2070*10)
    size_pattern = r'(\d+)[\*,](\d+)[\*,](\d+)\s*мм?'
    size_match = re.search(size_pattern, title)

    length, width, thickness = '', '', ''
    if size_match:
        length, width, thickness = map(int, size_match.groups())

    # 2. Извлекаем код (например, К358 или 8622)
    code_pattern = r'\b(?:\d{3,4}|[а-яА-Яa-zA-Z]{1,2}\d{2,5})\b'  # Ищем 3-4 значное число с возможной буквой "К"
    code_match = re.search(code_pattern, title)
    code = code_match.group(0) if code_match else ''

    # 3. Извлекаем структуру (например, PR, М, SM, GP, или две заглавные буквы)
    structure_pattern =r'\b([А-ЯA-Z]{1,2})(?:/([А-ЯA-Z]{1,2}))?\b'  # Ищем две заглавные буквы (латинские или кириллические)
    structure_match = re.search(structure_pattern, title)
    structure = structure_match.group(0) if structure_match else ''

    # 4. Извлекаем группу (например, 7гр, SPAN, РБ)
    group_pattern = r'\b(7гр|РБ|GP|SPAN)\b'
    group_match = re.search(group_pattern, title)
    group = group_match.group(0) if group_match else ''

    # . Извлекаем тип материала (ЛМДФ, ХДФ, Кромка ABS, Кромка ПВХ)
    material_pattern = re.compile(r'\b(ЛДСП|ЛМДФ|ХДФ|Кромка ABS|Кромка ПВХ)\b', re.IGNORECASE)
    material_match = material_pattern.search(title)
    material = material_match.group(0) if material_match else ''

    # 5. Формируем имя (убираем код, структуру, размеры и группу)
    name = re.sub(size_pattern, '', title)
    name = re.sub(code_pattern, '', name).strip()
    if structure:
        name = name.replace(structure, '').strip()
    if group:
        name = name.replace(group, '').strip()
    if material:
        name = re.sub(r'\b' + re.escape(material) + r'\b', '', name).strip()

    # Удаляем лишние пробелы и скобки
    name = re.sub(r'\s+', ' ', name).strip()  # Убираем двойные пробелы
    name = re.sub(r'\(\s*\)', '', name).strip()  # Убираем пустые скобки

    full_name = f'{code} {name}'.strip()

    return full_name
