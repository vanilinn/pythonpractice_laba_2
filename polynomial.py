from itertools import zip_longest

# Определение класса Polynomial
class Polynomial:
    def __init__(self, *args):
        # Инициализация объекта многочлена
        if len(args) == 1:
            arg = args[0]
            # Если передан словарь, создаем многочлен из его элементов
            if isinstance(arg, dict):
                self.cfs = [0] * (max(arg.keys()) + 1)
                for degree, coeff in arg.items():
                    self.cfs[degree] = coeff
            # Если передан список или кортеж, используем его коэффициенты
            elif isinstance(arg, (list, tuple)):
                self.cfs = list(arg)
            # Если передан другой многочлен, копируем его коэффициенты
            elif isinstance(arg, Polynomial):
                self.cfs = arg.cfs.copy()
            # В остальных случаях просто присваиваем аргумент self.cfs
            else:
                self.cfs = arg
        # Если передано несколько аргументов, просто используем их коэффициенты
        else:
            self.cfs = list(args)

    # Определение строкового представления многочлена
    def __str__(self):
        t = []
        # Обработка случая, когда многочлен представлен одним коэффициентом
        if isinstance(self.cfs, (int, float)):
            return str(self.cfs)
        # Перебор коэффициентов многочлена
        for degree, coeff in enumerate(self.cfs):
            if coeff != 0:
                sign = "+" if coeff > 0 else "-"
                coeff = abs(coeff)
                # Формирование термов многочлена
                if degree != 0:
                    if coeff == 1:
                        term = "x"
                    else:
                        term = f"{coeff}x"
                    if degree > 1:
                        term += f"^{degree}"
                    t.append(f"{sign} {term}")
                else:
                    t.append(f"{sign} {coeff}")
        # Возвращаемая строка, сконкатенированная из сформированных термов
        if not t:
            return "0"
        res = " ".join(t[::-1])
        return res if res[0] != "+" else res[1:].strip()

    # Определение строкового представления для отладки
    def __repr__(self):
        # Удаляем нулевые коэффициенты из списка
        cfs = self.cfs.copy()
        while cfs and cfs[-1] == 0:
            cfs.pop()
        return f"Многочлен {cfs}"

    # Метод для получения степени многочлена
    def degree(self):
        if self == Polynomial(0, 0, 0):
            return 0
        return len(self.cfs) - 1

    # Перегрузка оператора сложения
    def __add__(self, other):
        # Обработка операции сложения с другим многочленом
        if isinstance(other, Polynomial):
            res_coeffs = [sum(pair) for pair in zip_longest(self.cfs, other.cfs, fillvalue=0)]
            return Polynomial(*res_coeffs)
        # Обработка операции сложения с числом
        elif isinstance(other, (int, float)):
            res_coeffs = self.cfs.copy()
            res_coeffs[0] += other
            return Polynomial(*res_coeffs)
        # Вызов исключения при неподдерживаемом типе операнда
        else:
            raise TypeError(f"Неподдерживаемые типы операндов для +: 'Polynomial' and {type(other)}")

    # Перегрузка оператора вычитания
    def __sub__(self, other):
        # Аналогично методу __add__, но для операции вычитания
        if isinstance(other, Polynomial):
            res_coeffs = [pair[0] - pair[1] for pair in zip_longest(self.cfs, other.cfs, fillvalue=0)]
            return Polynomial(*res_coeffs)
        elif isinstance(other, (int, float)):
            res_coeffs = self.cfs.copy()
            res_coeffs[0] -= other
            return Polynomial(*res_coeffs)
        else:
            raise TypeError(f"Неподдерживаемые типы операндов для -: 'Polynomial' and {type(other)}")

    # Перегрузка оператора умножения
    def __mul__(self, other):
        # Обработка умножения на число или другой многочлен
        if isinstance(other, (int, float)):
            res_coeffs = [coeff * other for coeff in self.cfs]
            return Polynomial(res_coeffs)
        elif isinstance(other, Polynomial):
            # Если оба многочлена представлены целым числом, используем оптимизированный алгоритм умножения
            if isinstance(other.cfs, int) and isinstance(self.cfs, int):
                res_coeffs = [0] * (self.cfs + other.cfs)
                if len(res_coeffs):
                    for i, coeff1 in enumerate([self.cfs]):
                        for j, coeff2 in enumerate([other.cfs]):
                            res_coeffs[i + j] += coeff1 * coeff2
                else:
                    res_coeffs = [0]
            # В остальных случаях используем обычный алгоритм умножения
            elif isinstance(other.cfs, int):
                res_coeffs = [0] * (len(self.cfs) + other.cfs)
                for i, coeff1 in enumerate(self.cfs):
                    for j, coeff2 in enumerate([other.cfs]):
                        res_coeffs[i + j] += coeff1 * coeff2
            elif isinstance(self.cfs, int):
                res_coeffs = [0] * (self.cfs + len(other.cfs))
                for i, coeff1 in enumerate([self.cfs]):
                    for j, coeff2 in enumerate(other.cfs):
                        res_coeffs[i + j] += coeff1 * coeff2
            else:
                res_coeffs = [0] * (len(self.cfs) + len(other.cfs) - 1)
                for i, coeff1 in enumerate(self.cfs):
                    for j, coeff2 in enumerate(other.cfs):
                        res_coeffs[i + j] += coeff1 * coeff2
            return Polynomial(res_coeffs)

    # Перегрузка оператора равенства
    def __eq__(self, other):
        # Сравнение с числом или другим многочленом
        if isinstance(other, (int, float)):
            return self.cfs == [other]
        elif isinstance(other, Polynomial):
            return self.cfs == other.cfs
        else:
            return False

    # Перегрузка оператора унарного минуса
    def __neg__(self):
        return Polynomial(*[-coeff for coeff in self.cfs])

    # Перегрузка оператора умножения справа
    def __rmul__(self, other):
        return self.__mul__(other)

    # Перегрузка оператора сложения справа
    def __radd__(self, other):
        return self.__add__(other)

    # Перегрузка оператора вычитания справа
    def __rsub__(self, other):
        res_coeffs = [-coeff for coeff in self.cfs]
        res_coeffs[0] += other
        return Polynomial(*res_coeffs)

    # Метод для вычисления производной многочлена
    def der(self, d=1):
        if d < 0:
            raise ValueError("d должно быть неотрицательным")
        res_coeffs = self.cfs.copy()
        for x in range(d):
            res_coeffs.pop(0)
            res_coeffs = [idx * i for idx, i in enumerate(res_coeffs, start=1)]
        return Polynomial(res_coeffs)

    # Перегрузка оператора вызова ()
    def __call__(self, x):
        # Вычисление значения многочлена в точке x
        res = 0
        for degree, coeff in enumerate(self.cfs):
            res += (x ** degree) * coeff
        return res

    # Перегрузка итератора
    def __iter__(self):
        self.index = 0
        return self

    # Перегрузка метода next для итератора
    def __next__(self):
        if self.index < len(self.cfs):
            res = (self.index, self.cfs[self.index])
            self.index += 1
            return res
        raise StopIteration
