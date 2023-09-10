move_type = 'dynamic'
perm_long_disp = { # Допускаемое продольное смещение
    'le_10t': {
        'static': 2700,
        'dynamic': 3000,
    },
    
    '15t': {
        'static': 2250,
        'dynamic': 2480,
    },
    
    '20t': {
        'static': 1950,
        'dynamic': 2160,
    },
    
    '25t': {
        'static': 1550,
        'dynamic': 1730,
    },
    
    '30t': {
        'static': 1250,
        'dynamic': 1440,
    },
    
    '35t': {
        'static': 1100,
        'dynamic': 1235,
    },
    
    '40t': {
        'static': 950,
        'dynamic': 1080,
    },
    
    '45t': {
        'static': 850,
        'dynamic': 960,
    },
    
    '50t': {
        'static': 750,
        'dynamic': 865,
    },
    
    '55t': {
        'static': 680,
        'dynamic': 785,
    },
    
    '60t': {
        'static': 600,
        'dynamic': 720,
    },
    
    '62t': {
        'static': 550,
        'dynamic': 630,
    },
    
    '67t': {
        'static': 200,
        'dynamic': 260,
    },
    
    '70t': {
        'static': 0,
        'dynamic': 60,
    },
    
    'g_70t': {
        'static': 0,
        'dynamic': 0,
    },
}

def get_index(table: dict, elem: float):
    if len(table) == 0:
        raise ValueError('Нет ключей')
    keys = list(key for key in table)
    keys = [''.join(filter(str.isdigit, key)) for key in keys]
    keys = [float(key) for key in list(set(keys))]
    keys.sort()
    if elem in keys:
        result = keys.index(elem)
    else:
        keys.append(elem)
        keys = list(set(keys))
        keys.sort()
        elem_idx = keys.index(elem)
        result = (elem_idx - 1, elem_idx) if 0 < elem_idx < len(keys) - 1 else elem_idx
    return result

def get_values_for_long_critical(table: dict, indexes):
    table_keys = list(table.keys())
    res = []
    if isinstance(indexes, int):
        indexes = (indexes, )
    for idx in indexes:
        cur_key = table_keys[idx]
        elem = table[cur_key][move_type]
        res.append({cur_key: elem})
    return res

def get_long_critical(need_values: list, weight: float):
    result = None
    if len(need_values) != 1 and len(need_values) != 2:
        raise ValueError('Некорректное количество значений')
    else:
        if len(need_values) == 1:
            for _, value in need_values[0].items():
                result = value
        if len(need_values) == 2:
            keys = []
            values = []
            for cur_val in need_values:
                for key, value in cur_val.items():
                    key = ''.join(filter(str.isdigit, key))
                    key = float(key)
                    keys.append(key)
                    values.append(value)
            result = values[0] - ((values[0] - values[1]) / keys[1] - keys[0] * (weight - keys[0]))
    return result

def find_long_crit(table: dict, weight: float):
    long_idx = get_index(table, weight)
    long_values = get_values_for_long_critical(table, long_idx)
    long_crit = get_long_critical(long_values, weight)
    return long_crit


perm_long = find_long_crit(perm_long_disp, weightSum)
print(f'Допускаемые значения продольного смещения для грузов: {perm_long}')
