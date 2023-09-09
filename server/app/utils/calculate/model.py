import random

import copy


class Optimize:
    """ Модель для оптимизации расположения n-групов на 
    ж/д платформе. """

    def __init__(self, cargo: list[CargoItem], floor_length: int,
                 weightSum: float, free_L_for_one_cargo: int,
                 step=1, border_epsilon_step=1, count_early_stop=10):
        """ step - шаг влево/вправо для delta.
        floor_length - длина пола.
        weightSum - общая сумма груза.
        free_L_for_one_cargo - свободное пространство на один груз, где можем его двигать.
        step - точность и скорость оптимизации (чем ниже, тем точнее, но немного медленнее).
        border_epsilon_step - случайное макс. добавление к step.
        count_early_stop - ранняя остановка, если оптимизация не улучшается. """

        self.best_cargo = None
        self.score = float('inf')

        self._step = step
        self._border_epsilon_step = border_epsilon_step  # Рандомное значение добавляется к step.
        self._count_early_stop = count_early_stop

        # Исходные данные:
        self._floor_length = floor_length
        self._weightSum = weightSum
        self._free_L_for_one_cargo = free_L_for_one_cargo

        self._optimize(cargo)

    def _init_delta(self, cargo: list[CargoItem], start_idx=0):
        """ Инициализация значений delta. Внутри создаёт новый cargo.
        Функция инициализирует расположение грузов для дальнейшей оптимизации. """

        copy_cargo = [copy.deepcopy(item) for item in cargo]

        # Меняю очерёдность грузов на платформе.
        copy_cargo = copy_cargo[start_idx:] + copy_cargo[:start_idx]

        if len(copy_cargo) == 1:
            copy_cargo[0].delta = self._floor_length / 2 - copy_cargo[0].length / 2

        else:

            prev_border = 0
            for idx, item in enumerate(copy_cargo):

                copy_cargo[idx].delta = random.randint(prev_border, prev_border + self.free_L_for_one_cargo - 1)

                # Обновляем левую границу.
                prev_border = prev_border + item.length + self._free_L_for_one_cargo
    
        return copy_cargo

    def _get_score(self, cargo: list[CargoItem]) -> float:
        """ Получение метрик при изменённом delta у одного груза.
        Метрикой считается Продольное смещение грузов в вагоне. """

        # Продольное смещение грузов в вагоне - в мм.
        longitudinal_displacement_cargo_in_car = 0.5 * self._floor_length - \
            (sum(map(lambda x: x.weight * x.delta, cargo)) / self.weightSum)

        return longitudinal_displacement_cargo_in_car

    def _check_best_cargo(self, cargo: list[CargoItem]) -> bool:
        """ Проверка метрик у обновлённого delta у cargo. """

        score = self._get_score(cargo)
        if abs(score) < abs(self.score):
            self.best_cargo = cargo
            self.score = score
            return True

        return False

    def _optimize(self, cargo: list[CargoItem]) -> None:
        """ Процесс оптимизации продольного смещения.
        Изменяется координата центра тяжести вагона относительно торцевого борта,
        чтобы продольное смещение стремилось к нулю. """

        # Меняю очерёдность расположение каждого груза.
        for i in range(0, len(cargo)):
            print(f'Началась оптимизация, где первый груз с индексом {i}')
            copy_cargo = self._init_delta(cargo, i)

            # Эпохи:
            counter = 0
            while counter < self._count_early_stop:

                # Смещаю каждый груз влево и вправо на step, затем смотрю метрики.
                for k in range(len(copy_cargo)):

                    left_step_cargo = [copy.deepcopy(item) for item in copy_cargo]
                    new_step = self._step + random.randint(0, self._border_epsilon_step)
                    left_step_cargo[k].delta -= new_step

                    right_step_cargo = [copy.deepcopy(item) for item in copy_cargo]
                    new_step = self._step + random.randint(0, self._border_epsilon_step)
                    right_step_cargo[k].delta += new_step

                    # Проверки на не наложение одного груза на другой.
                    # Нулевый элемент не выходит за пределы платформы слева.
                    if k == 0:
                        if left_step_cargo[k].delta >= 0:
                            # проверка
                            if self._check_best_cargo(left_step_cargo):
                                counter = 0
                                copy_cargo = self.best_cargo
    
                    # Последний элемент не выходит за пределы платформы справа.
                    elif k == len(copy_cargo) - 1:
                        if right_step_cargo[k].delta + right_step_cargo[k].length < self._floor_length:
                            # проверка
                            if self._check_best_cargo(right_step_cargo):
                                counter = 0
                                copy_cargo = self.best_cargo

                    else:
                        # Проверка на не наложение правого груза на левый. 
                        if left_step_cargo[k].delta > left_step_cargo[k-1].delta + left_step_cargo[k-1].length:
                            if self._check_best_cargo(left_step_cargo):
                                counter = 0
                                copy_cargo = self.best_cargo

                        # Проверка на не наложение левого груза на превый. 
                        if right_step_cargo[k].delta + right_step_cargo[k].length < right_step_cargo[k+1].delta:
                            if self._check_best_cargo(right_step_cargo):
                                counter = 0
                                copy_cargo = self.best_cargo

                # После каждой эпохи увеличиваю.
                counter += 1
