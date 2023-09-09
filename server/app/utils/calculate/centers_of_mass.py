from app.schemas import CalculateRequest


async def calculate_centers_of_mass(body: CalculateRequest) -> dict:
    

    for index, item in enumerate(body.cargo):
        if index:
            prev = body.cargo[index - 1]
            item.center_gravity = (item.length + prev.length) / 2 \
                + prev.center_gravity + item.coordinate_center_gravity_load_relative_end_board
        else:
            item.center_gravity = item.length / 2 + item.coordinate_center_gravity_load_relative_end_board

    # Пункт 1.
    # Сумма всех грузов - в т.
    weightSum = sum(map(lambda x: x.weight, body.cargo))

    # Продольное смещение грузов в вагоне - в мм.
    longitudinal_displacement_in_car = 0.5 * body.floor_length - \
        (sum(map(lambda x: x.weight * x.center_gravity, body.cargo)) / weightSum)

    # Продольное смещение грузов с вагоном - в мм.
    longitudinal_displacement_with_car = 0.5 * body.floor_length - \
        (sum(map(lambda x: x.weight * x.center_gravity, body.cargo)) \
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


