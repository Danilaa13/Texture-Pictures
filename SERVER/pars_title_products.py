import re
import string

def parse_title(title):
    materials = [
        'ДСП', 'ЛДСП', 'ЛМДФ', 'МДФ', 'ХДФ',
        'Кромка', 'Кромка ABS', 'Кромка ПВХ',
        'ПЭТ', 'ПЭТ ПЭТ','Панель', 'Панель глянцевая', 'меламин в цвет','Уценка','новый','Плита','глянцевая',
        'кромкой', 'группа',
    ]
    size = ['19x3050x2070','18x1220x2800','18x1220x2800','16x1220x2800',]
    brands = [
        'Egger', 'KEL', 'Alvic', 'Galoplast', 'Алтайлес',
        'Slotex', 'Saviola', 'ARKOPA', 'Resista','PerfectSense','(AGTМДФ)',
        '(EVOGLOSSМДФ)','АМК-Троя'
    ]
    groups = [
        'GP', 'SPAN', 'PVC', 'ПВХ', 'ABS', 'CPL', 'HPL',
        'DUALUXE', 'RM', 'ANK','CLEAF','TSS','SMart','Smart','ETERNO','duco1','duco2','duco3','duco4'
    ]
    structures = [
        'TM9', 'TM28', 'TM37', 'TM22', 'TM',
        'ST9', 'ST15', 'ST2', 'ST30', 'ST33', 'ST10',
        'SM', 'BS', 'PG', 'PM', 'W', 'HG',
        'TM12',
    ]
    noise_phrases = ['инд. упаковка', 'двусторонняя','Турция', 'матовая','для столешниц', 'Стеновая', 'Столешница','ХДФобл',
                     'без клея','Герметик','БЕЗ ЗАВАЛА','СП'
                     ]

    all_noise = materials + brands + groups + structures + noise_phrases + size

    title = title.replace('х', 'x').replace('*', 'x').replace(',', '').strip()

    title = re.sub(r'\b\d{1,4}x\d{1,4}x\d{1,4}\b', '', title)

    title = re.sub(r'\b\d{1,4}x\d{1,4}\b', '', title)

    title = re.sub(r'\d{3,4}x\d{3,4}x\d{1,3}', '', title)
    title = re.sub(r'\bмм\b', '', title, flags=re.IGNORECASE)



    code_match = re.search(r'\b(?:[A-ZА-Я]{1,4}\d{1,5}(?:[/-]\d{1,5})?|\d{2,4}[/-]?[A-Za-z]+\d{0,2}|[A-Za-zА-Я]\d+|\d+)\b', title)

    code = code_match.group(0) if code_match else ''

    if code:
        title = title.replace(code, '')

    for word in all_noise:
        title = re.sub(r'\b' + re.escape(word) + r'\b', '', title, flags=re.IGNORECASE)

    title = re.sub(r'[\\/]', ' ', title)
    name = re.sub(r'\s+', ' ', title).strip()

    name = name.strip(string.punctuation + ' ')
    name = ' '.join([
        word for word in name.split()
        if re.fullmatch(r'[А-Яа-яЁё\-]+', word) and len(word) > 1
    ])
    if not name:
        name = ' '.join([
            word for word in title.split()
            if re.fullmatch(r'[A-Za-z0-9\-]+', word)
        ])

    full_name = f'{name}'.strip()
    full_name = full_name.strip(string.punctuation + ' ')

    if not full_name:
        full_name = 'Без названия'

    return full_name
