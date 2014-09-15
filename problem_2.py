# -*- coding: utf-8 -*-
__author__ = 'cpn'

import functools

# Решение задачи.

# Дана последовательность целых чисел.
# Считая их массами имеющихся в наличии предметов, определить,
# можно ли все эти предметы положить на весы так,
# чтобы весы находились в равновесии.
# Вывести вариант расположения.
# Определить, можно ли из них отобрать какое-то количество предметов
# с суммарным весом 100 (вывести yes или no, в зависимости от результата).

# Пример входных данных:
# 2 3 4 5 6

# Пример выходных данных:
# 2 3 5 - 4 6
# no


class memoized(object):
    """
        Декоратор для сохраннения промежуточных
        результатов работы рекурсивных вызовов.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            return self.func(*args)

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


@memoized
def ss(lst, amount, pos=0):
    """
        Функция вычисляющая результат.
        Args:
            lst: список веов
            amount: масса под которую нужно подобрать вес
            pos; позиция с которой начинае расчет

        Returns:
            список весов или 0 если подобрать невозможно
    """

    result_list = []

    if amount < 0 or len(lst) == 0:
        return 0

    if lst[0] == amount:
        result_list.append(pos)
        return result_list

    if len(lst) == 1:
        return 0

    sub_result_list = ss(lst[1:], amount-lst[0], pos+1)

    if sub_result_list != 0:
        sub_result_list.append(pos)
        return sub_result_list

    sub_result_list = ss(lst[1:], amount, pos+1)
    if sub_result_list != 0:
        return sub_result_list

    return 0


def main(list_input):
    """
        Главная функция подготавливающая входные и выходные данные.

        Args:
            list_input: список весов

        Returns:
            результат вычисления, кортеж из двух элементов -
                1. Результат уравновешивания весов, в виде строки,
                    например '12 7 - 18 1', иначе 'no'
                2. Результат ответа на вопрос -
                    можни ли набрать суммарный вес 100 (либо 'yes', либо 'no')

        >>> main([2, 3, 4, 5, 6])
        ('2 3 5 - 4 6', 'no')

    """
    arg_additional = 100
    res = 'no'
    res_additional = 'no'

    total_weight = sum(list_input)
    rec = ss(list_input, total_weight//2) if not total_weight % 2 else 0

    if rec:
        sub_list = (
            [str(val) for index, val in enumerate(list_input) if index in rec]
        )

        sub_list_none = (
            [str(val) for index, val in enumerate(list_input)
                if index not in rec]
        )

        res = '{} - {}'.format(' '.join(sub_list), ' '.join(sub_list_none))

    if ss(list_input, arg_additional):
        res_additional = 'yes'
    return res, res_additional,


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l',
        '--list_input',
        nargs='+',
        type=int,
        help='Список весов'
    )

    args = parser.parse_args()
    print main(args.list_input)
