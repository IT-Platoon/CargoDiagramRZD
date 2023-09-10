import copy

from app.schemas import CalculateRequest
from .check_delta_length import *
from .model import Optimize


# Константы для вычислений.
mounting_type = 'elastic' # Тип крепления
mu = 0.5 # Коэффициент трения
slif = { # Значения удельной продольной инерционной силы
    'elastic': { # Крепление растяжками и обвязками, деревянными упорными, распорными брусками
        'a22': 1.2, 'a94': 0.97, 'a44': 1.2, 'a188': 0.86,
    },
    'hard': { # Крепление болтами, шпильками, упор в элементы конструкции вагона
        'a22': 1.9, 'a94': 1.67, 'a44': 1.9, 'a188': 1.56,
    },
}


async def calculate_centers_of_mass(body: CalculateRequest) -> dict:

    # Изменение кол-ва груза из-за поля quantity.
    update_count_cargo = []
    for item in body.cargo:
        for _ in range(item.quantity):
            tmp_cargo = copy.deepcopy(item)
            tmp_cargo.quantity = 1
            update_count_cargo.append(tmp_cargo)
    body.cargo = update_count_cargo

    # Свободное место на платформе, если расположить все грузы.
    free_L = body.floor_length - sum([item.length for item in body.cargo])
    # Свободное пространство на один груз, где можем его двигать.
    free_L_for_one_cargo = free_L // len(body.cargo)

    # Груз не влазит: error!
    if free_L < 0:
        return {'error': 'error'}

    # Сумма всех грузов - в т.
    weightSum = sum(map(lambda x: x.weight, body.cargo))

    # Поиск оптимального расположения всех грузов на платформе.

    model = Optimize(
        body.cargo, body.floor_length, body.floor_width,
        weightSum, free_L_for_one_cargo,
        step=1, n_iter=1000
    )

    # Оптимальное расположение груза.
    body.cargo = model.best_cargo

    # Пункт 1.
    # Продольное смещение грузов в вагоне - в мм.
    longitudinal_displacement_in_car = 0.5 * body.floor_length - \
        (sum(map(lambda x: x.weight * x.delta_length, body.cargo)) / weightSum)

    # Допускаемое значение продольного смещения для грузов.
    _perm_long = find_long_crit(perm_long_disp, weightSum)
    if longitudinal_displacement_in_car < _perm_long:
        longitudinal_displacement_flag = 'Продольное смещение допустимо.'
    else:
        longitudinal_displacement_flag = 'Продольное смещение не допустимо, не получилось найти оптимальное расположение.'

    # Продольное смещение грузов с вагоном - в мм.
    longitudinal_displacement_with_car = 0.5 * body.floor_length - \
        (sum(map(lambda x: x.weight * x.delta_length, body.cargo)) \
        + body.tare_weight * body.floor_length / 2) / (weightSum + body.tare_weight)

    # Поперечное смещение в вагоне - в мм.
    lateral_displacement_in_car = 0.5*body.floor_width - (sum(map(lambda x: x.weight * x.delta_width, body.cargo))) / weightSum

    # Поперечное смещение грузов с вагоном - в мм.
    lateral_displacement_with_car = 0.5*body.floor_width - \
        (sum(map(lambda x: x.weight * x.delta_width, body.cargo)) \
        + body.tare_weight * body.floor_width/2) / (weightSum + body.tare_weight)

    # Пункт 2.
    # Высота центра тяжести в вагоне - в мм.
    height_center_gravity_in_car = sum(map(lambda x: x.weight * \
        (x.height / 2 + body.floor_height_from_level_rail_heads), body.cargo)) / weightSum

    # Пункт 3.
    # Общая высота ЦТ - в мм.
    general_height_center_gravity = (sum(map(lambda x: x.weight * \
        (x.height / 2 + body.floor_height_from_level_rail_heads), body.cargo)) + \
        body.tare_weight * body.height_center_gravity_from_level_rail_heads) / (weightSum + body.tare_weight)

    # Расчет наветренной поверхности - в м2.
    # Значение 7 - константа.
    # Если < 50 м2, то платформа с грузом устойчива.
    windward_surface = sum([item.length / 1000 * item.height / 1000 for item in body.cargo]) + 7

    # Пункт 4.
    # Расчёт сил, действующих на груз.

    # Удельная продольная инерционная сила на одну тонну веса груза в тс/с
    specific_length_inertial_force_per_ton_cargo_weight = slif[mounting_type]['a22'] - \
        (weightSum * (slif[mounting_type]['a22'] - slif[mounting_type]['a94'])) / 72

    longitudinal_inertial_force = []
    wind_load = []
    friction_force_longitudinal_direction = []
    for item in body.cargo:

        # Продольная инерционная сила в тс
        item.longitudinal_inertial_force = specific_length_inertial_force_per_ton_cargo_weight * item.weight 
        longitudinal_inertial_force.append(item.longitudinal_inertial_force)

        # Ветровая нагрузка в тс
        item.wind_load = 50 * item.length / 1000 * item.height / 1000 * 0.001
        wind_load.append(item.wind_load)

        # Сила трения в продольном направлении в тс
        item.friction_force_longitudinal_direction = mu * item.weight
        friction_force_longitudinal_direction.append(item.friction_force_longitudinal_direction)

    return {
        'longitudinal_displacement_in_car': round(longitudinal_displacement_in_car, 3),  # В мм
        'longitudinal_displacement_flag': longitudinal_displacement_flag,  # text-формат.
        'longitudinal_displacement_with_car': round(longitudinal_displacement_with_car, 3),  # В мм
        'lateral_displacement_in_car': round(lateral_displacement_in_car, 3),  # в мм
        'lateral_displacement_with_car': round(lateral_displacement_with_car, 3),  # в мм
        'height_center_gravity_in_car': round(height_center_gravity_in_car, 3),  # в мм
        'general_height_center_gravity': round(general_height_center_gravity, 3),  # В мм
        'windward_surface': round(windward_surface, 3),  # в м2
        'specific_length_inertial_force_per_ton_cargo_weight': round(specific_length_inertial_force_per_ton_cargo_weight, 3),  # в тс/с
        'cargo': [
            {
                'length': item.length,    # В мм
                'width': item.width,    # В мм
                'height': item.height,    # В мм
                'quantity': item.quantity,    # В шт
                'weight': item.weight,    # В т
                'delta_length': item.delta_length,  # В мм
                'delta_width': item.delta_width,  # В мм
                'wind_load': round(item.wind_load, 3),  # В тс
                'longitudinal_inertial_force': round(item.longitudinal_inertial_force, 3),  # В тс
                'friction_force_longitudinal_direction': round(item.friction_force_longitudinal_direction, 3),  # В тс
            }
            for item in body.cargo
        ]
    }
