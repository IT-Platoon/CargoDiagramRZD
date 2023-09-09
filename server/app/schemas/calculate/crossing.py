""" Модуль с реализацией генетического оператора скрещивания. """


import random


class Crossing:
    """ Cкрещивание. """

    def __init__(self, p: float, strategy: str):
        # Вероятность скрещивания.
        self.p = p
        self.strategy = strategy  # s | u

    def crossing(self, population: list[list]) -> list[list]:
        """ Скрещивание осуществляется с определённой вероятностью. """

        count_population = len(population)

        crossing_population = []
        for _ in range(count_population // 2):
            tmp_count_population = len(population) - 1

            # Случайный выбор 2 генотипов.
            idx_rand1 = random.randint(0, tmp_count_population)
            genotip1 = population.pop(idx_rand1)

            idx_rand2 = random.randint(0, tmp_count_population-1)
            genotip2 = population.pop(idx_rand2)

            # Скрещивание происходит в вероятноью p.
            if random.random() < self.p:

                if self.strategy == "s":
                    two_childs = self._singlePointCrossing(genotip1, genotip2)

                else:
                    two_childs =  self._uniformCrossing(genotip1, genotip2)

            else:
                two_childs = [genotip1, genotip2]

            # Добавление потомков в новое поколение.
            for child in two_childs:
                crossing_population.append(child)

        return crossing_population

    def _singlePointCrossing(self, genotip1: list, genotip2: list) -> list[list, list]:
        """ Одноточечное скрещивание. """

        count_variables = len(genotip1)

        two_childs = [[] for _ in range(2)]
        for i in range(count_variables):
            lenght = len(genotip1[i])
            point = random.randint(1, lenght-1)

            one_param_child1 = genotip1[i][:point] + genotip2[i][point:]
            one_param_child2 = genotip2[i][:point] + genotip1[i][point:]

            two_childs[0].append(one_param_child1)
            two_childs[1].append(one_param_child2)

        return two_childs

    def _uniformCrossing(self, genotip1: list, genotip2: list) -> list[list, list]:
        """ Равномерное скрещивание. """

        count_variables = len(genotip1)

        two_childs = [[] for _ in range(2)]
        for i in range(count_variables):
            lenght = len(genotip1[i])

            one_param_child1 = [random.choice([genotip1[i][k], genotip2[i][k]]) for k in range(lenght)]
            one_param_child2 = [random.choice([genotip1[i][k], genotip2[i][k]]) for k in range(lenght)]

            two_childs[0].append(one_param_child1)
            two_childs[1].append(one_param_child2)

        return two_childs


if __name__ == "__main__":

    crossing = Crossing(0.9, "u")

    population = [
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1],
    ]
    print(crossing.crossing(population))

    # population = [
    #     [[0, 0, 1, 0, 0, 1], [1, 1, 1, 0, 1, 1], [1, 1, 1, 0, 1, 1]],
    #     [[1, 1, 1, 0, 0, 1], [0, 1, 1, 0, 0, 0], [1, 1, 1, 0, 1, 1]],
    #     [[0, 1, 1, 0, 1, 1], [0, 0, 1, 1, 0, 0], [1, 1, 1, 0, 1, 1]],
    #     [[1, 0, 0, 1, 1, 1], [0, 0, 0, 0, 1, 1], [1, 1, 1, 0, 1, 1]],
    #     [[1, 1, 1, 1, 0, 0], [1, 0, 0, 0, 0, 1], [1, 1, 1, 0, 1, 1]],
    #     [[1, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0], [1, 1, 1, 0, 1, 1]],
    # ]
    # # print(crossing.crossing(population))
    # for i in crossing.crossing(population):
    #     print(i)
