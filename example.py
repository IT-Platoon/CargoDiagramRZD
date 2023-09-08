# Характеристика 4-х осной ж/д платформы
L = 13400 # Длина пола
2870 # Ширина пола
Qv = 21 # Масса тары
wugr = 1310 # Высота пола от УГР
800 # Высота центра тяжести(ЦТ) от УГР
9720 # База платформы

cargo = [ # грузы
    {'length': 3650, 'width': 3320, 'height': 1500, 'weight': 6670 / 1000},
    {'length': 3870, 'width': 2890, 'height': 1020, 'weight': 4085 / 1000},
    {'length': 1080, 'width': 1580, 'height': 390, 'weight': 395 / 1000},
    {'length': 4100, 'width': 1720, 'height': 1150, 'weight': 1865 / 1000},
]
weightSum = sum(map(lambda x: x['weight'], cargo))

for index, item in enumerate(cargo):
    if index:
        prev = cargo[index - 1]
        item['ct'] = (item['length'] + prev['length']) / 2 + prev['ct']
    else:
        item['ct'] = item['length'] / 2




# Продольное смещение грузов в вагоне
Lc = 0.5*L - (sum(map(lambda x: x['weight'] * item['ct'], cargo)) / weightSum)

# Продольное смещение грузов с вагоном
Lcv = 0.5*L - (sum(map(lambda x: x['weight'] * item['ct'], cargo)) + Qv * L/2) / (weightSum + Qv)

# Общая высота ЦТ
H = sum(map(lambda x: x['weight'] * (x['height'] + wugr), cargo)) / weightSum
