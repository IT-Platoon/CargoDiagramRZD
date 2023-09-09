from app.schemas import CalculateRequest
from .model import Optimize


async def calculate_centers_of_mass(body: CalculateRequest) -> dict:
    
    # Свободное место на платформе, если расположить все грузы.
    free_L = body.floor_length - sum([item.length for item in body.cargo])
    # Даём пустое пространство на один груз, где можем его двигать.
    free_L_for_one_cargo = free_L // len(body.cargo)

    # Груз не влазит: error!
    if free_L < 0:
        return {'error': 'error'}

    # Поиск оптимального расположения всех грузов на платформе.
    best_score = float('inf')
    best_cargo = None
    weightSum = sum(map(lambda x: x.weight, body.cargo))
    for _ in range(10):
        model = Optimize(body.cargo, body.floor_length, weightSum, free_L_for_one_cargo, step=1, border_epsilon_step=1, count_early_stop=10)
        if abs(model.score) < abs(best_score):
            best_score = model.score
            best_cargo = model.best_cargo

    # Оптимальное расположение груза.
    body.cargo = best_cargo

    # Пункт 1.
    # Сумма всех грузов - в т.
    weightSum = sum(map(lambda x: x.weight, body.cargo))

    # Продольное смещение грузов в вагоне - в мм.
    longitudinal_displacement_in_car = 0.5 * body.floor_length - \
        (sum(map(lambda x: x.weight * x.delta, body.cargo)) / weightSum)

    # Продольное смещение грузов с вагоном - в мм.
    longitudinal_displacement_with_car = 0.5 * body.floor_length - \
        (sum(map(lambda x: x.weight * x.delta, body.cargo)) \
        + body.tare_weight * body.floor_length / 2) / (weightSum + body.tare_weight)

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

    return {
        'longitudinal_displacement_in_car': longitudinal_displacement_in_car,
        'longitudinal_displacement_with_car': longitudinal_displacement_with_car,
        'general_height_center_gravity': general_height_center_gravity,
    }
