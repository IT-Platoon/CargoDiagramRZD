import copy
import itertools
import random

from app.schemas import CargoItem


class Optimize:
    """ Модель для оптимизации продольного смещения. """

    def __init__(self, cargo: list[CargoItem],
                 floor_length: int, floor_width: int,
                 weightSum: float, free_L_for_one_cargo: int,
                 step=1, n_iter=1000):
        """ step - точность и скорость оптимизации (чем ниже, тем точнее). От 1 до бесконечности - int.
        n_iter - кол-во повторений алгоритма для надёжности. Чем болешье, чем точнее, но медленнее.
        floor_length - длина пола.
        floor_width - ширина пола.
        weightSum - общая сумма груза.
        free_L_for_one_cargo - свободное пространство на один груз, где можем его двигать. """
        
        self.best_cargo = None
        self.score_length = float('inf')
        self.score_width = float('inf')

        self._step = step  # Чем меньше - тем лучше
        self._n_iter = n_iter  # Кол-во повторений

        # Исходные данные:
        self._floor_length = floor_length
        self._floor_width = floor_width
        self._weightSum = weightSum
        self._free_L_for_one_cargo = free_L_for_one_cargo

        self._optimize(cargo)


    def _init_delta(self, cargo: list[CargoItem]):
        """ Инициализация значений delta. Внутри создаёт новый cargo. """

        copy_cargo = [copy.deepcopy(item) for item in cargo]

        # Единственный ящик инициализирую в центре по ширине и длине.
        if len(copy_cargo) == 1:
            copy_cargo[0].delta_length = self._floor_length / 2 - copy_cargo[0].length / 2
            copy_cargo[0].delta_width = self._floor_width / 2 - copy_cargo[0].width / 2

        else:

            prev_border = 0
            for idx, item in enumerate(copy_cargo):

                copy_cargo[idx].delta_length = random.randint(prev_border, prev_border + self._free_L_for_one_cargo - 1)

                # Всегда начинаем с центра ширины.
                copy_cargo[idx].delta_width = self._floor_width / 2 - copy_cargo[idx].width / 2
    
                # Обновляем левую границу.
                prev_border = prev_border + item.length + self._free_L_for_one_cargo

        return copy_cargo

    def _get_score_length(self, cargo: list[CargoItem]):
        """ Получение метрик при движения груза продольно. """

        # Продольное смещение грузов в вагоне - в мм.
        Lc = 0.5*self._floor_length - (sum(map(lambda x: x.weight * x.delta_length, cargo)) / self._weightSum)

        return Lc

    def _get_score_width(self, cargo: list[CargoItem]):
        """ Получение метрик при движения груза поперечно. """

        # Поперечное смещение грузов в вагоне - в мм.
        Wc = 0.5*self._floor_width - (sum(map(lambda x: x.weight * x.delta_width, cargo))) / self._weightSum
        return Wc

    def _check_best_cargo(self, cargo: list[CargoItem], length_flag: bool):
        """ Проверка метрик у обновлённого delta у cargo. """

        # Для продольного смещения.
        if length_flag:
            score = self._get_score_length(cargo)
            if abs(score) < abs(self.score_length):
                self.best_cargo = cargo
                self.score_length = score
                return True

        # Для поперечного.
        else:
            score = self._get_score_width(cargo)
            if abs(score) < abs(self.score_width):
                self.best_cargo = cargo
                self.score_width = score
                return True

        return False

    def _optimize(self, cargo: list[CargoItem]):
        """ Процесс оптимизации delta. """

        for _ in range(self._n_iter):
            # Все перестановка имеющихся грузов.
            permutations_cargo = list(itertools.permutations(cargo))

            # Меняю очерёдность расположение каждого груза.
            for i in range(0, len(permutations_cargo)):
                copy_cargo = self._init_delta(permutations_cargo[i])

                # Эпохи для продольной оптимизации.
                flag_work_epoch = True
                while flag_work_epoch:
                    flag_work_epoch = False

                    # Смещаю каждый груз влево и вправо на step, затем смотрю метрики.
                    for k in range(len(copy_cargo)):

                        left_step_cargo = [copy.deepcopy(item) for item in copy_cargo]
                        left_step_cargo[k].delta_length -= self._step

                        right_step_cargo = [copy.deepcopy(item) for item in copy_cargo]
                        right_step_cargo[k].delta_length += self._step

                        # Проверки на не наложение одного груза на другой.
                        # Нулевый элемент не выходит за пределы платформы слева.
                        if k == 0:
                            if left_step_cargo[k].delta_length >= 0:
                                # проверка
                                if self._check_best_cargo(left_step_cargo, True):
                                    copy_cargo = self.best_cargo
                                    flag_work_epoch = True

                        # Последний элемент не выходит за пределы платформы справа.
                        elif k == len(copy_cargo) - 1:
                            if right_step_cargo[k].delta_length + right_step_cargo[k].length < self._floor_length:
                                # проверка
                                if self._check_best_cargo(right_step_cargo, True):
                                    copy_cargo = self.best_cargo
                                    flag_work_epoch = True

                        else:
                            # Проверка на не наложение правого груза на левый. 
                            if left_step_cargo[k].delta_length > left_step_cargo[k-1].delta_length + left_step_cargo[k-1].length:
                                if self._check_best_cargo(left_step_cargo, True):
                                    copy_cargo = self.best_cargo
                                    flag_work_epoch = True

                            # Проверка на не наложение левого груза на превый. 
                            if right_step_cargo[k].delta_length + right_step_cargo[k].length < right_step_cargo[k+1].delta_length:
                                if self._check_best_cargo(right_step_cargo, True):
                                    copy_cargo = self.best_cargo
                                    flag_work_epoch = True

                # Эпохи для поперечной оптимизации.
                flag_work_epoch = True
                while flag_work_epoch:
                    flag_work_epoch = False
    
                    # Смещаю каждый груз влево и вправо на step, затем смотрю метрики.
                    for k in range(len(copy_cargo)):
    
                        bottom_step_cargo = [copy.deepcopy(item) for item in copy_cargo]
                        bottom_step_cargo[k].delta_width += self._step

                        top_step_cargo = [copy.deepcopy(item) for item in copy_cargo]
                        top_step_cargo[k].delta_width -= self._step

                        # Проверки на то, чтобы груз не выходил на пределы платформы по бокам.
                        if bottom_step_cargo[k].delta_width >= 0 and bottom_step_cargo[k].delta_width + bottom_step_cargo[k].width < self._floor_width:
                            # проверка
                            if self._check_best_cargo(bottom_step_cargo, False):
                                copy_cargo = self.best_cargo
                                flag_work_epoch = True
 
                        if top_step_cargo[k].delta_width >= 0 and top_step_cargo[k].delta_width + top_step_cargo[k].width < self._floor_width:
                            # проверка
                            if self._check_best_cargo(top_step_cargo, False):
                                copy_cargo = self.best_cargo
                                flag_work_epoch = True
