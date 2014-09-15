
# -*-coding: utf-8 -*-

__author__ = 'cpn'

import collections as col

# Решение задачи.
# 1. Пересекающиеся прямоугольники
# Дан набор прямоугольников,
# заданных двумерными координатами пары противоположных вершин
# (левой нижней и правой верхней).
# Стороны прямоугольников параллельны осям координат.
# Прямоугольники могут пересекаться друг с другом.
# Найдите общую площадь, которую покрывают эти прямоугольники.

# Пример входных данных:
# 0 1 3 3
# 2 2 6 4
# 1 0 3 5

# Пример выходных данных:
# 18


def preprocessing(tuple_input):
    """
        Функция предварительой обработки.

        Args:
            tuple_input: кортеж кортежей(например ((0, 1, 3, 3), (2, 2, 6, 4),)

        Returns:
            Кортеж состоящий из двух элементов:
                список отстортированных x-координат

                список именованных кортежей с полями
                    (type start finish y), отсортированные по y
    """
    matrix_y = col.namedtuple('vertical', 'type start finish y')
    result_x = []
    result_y = []

    for i in tuple_input:
        result_x.extend([i[0], i[2]])
        result_y.extend([
            matrix_y(y=i[1], type=1, start=i[0], finish=i[2]),
            matrix_y(y=i[3], type=-1, start=i[0], finish=i[2]),
            ]
        )

    result_x.sort()
    result_y.sort(key=lambda x: x.y)

    return result_x, result_y,


def main(tuple_rangle):
    """
        Основная функция вычисляющая площадь объединения прямоугольников.

        Args:
            tuple_range: кортеж кортежей координат прямоугольников
                (например ((0, 1, 3, 3), (2, 2, 6, 4),)

        Returns:
            Площадь объединения прямоугольников, int

    >>> main(((0, 1, 3, 3), (2, 2, 6, 4), (1, 0, 3, 5)))
    18

    """
    result_x, result_y = preprocessing(tuple_rangle)
    result_total = 0
    for i in xrange(1, len(result_x)):
        delta_x = result_x[i] - result_x[i-1]
        cnt = 0
        for j in xrange(0, len(result_y)):
            if (result_y[j].finish <= result_x[i-1]
                    or result_y[j].start >= result_x[i]):
                continue
            if cnt == 0:
                start = result_y[j].y
            cnt += result_y[j].type
            if cnt == 0:
                result_total += (result_y[j].y - start)*delta_x

    return result_total


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-r',
        '--rangle',
        nargs='+',
        type=int,
        help='Координаты прямоугольников'
    )

    args = parser.parse_args()

    if len(args.rangle) % 4 != 0:
        print 'Неверные входные данные'

    else:
        print main(
            tuple([
                tuple(
                    args.rangle[i:i+4]) for i in xrange(0, len(args.rangle), 4)
                ]
            )
        )
