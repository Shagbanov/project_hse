import copy
import bisect


class Matrix:
    """Класс матрица:
       1) Операторы: +(++) -(++) *(++) **-1(++) ~(++) *n(++) [](++)
       2)Удаление(++) и перестановка строк и столбцов(++), получение ранга матрицы(++),
        получение размерности(++), преобразование к списку(++), транспонирование(++)
       3) Иерархия исключений

       Не одна их функция не изменят матрицу а возвращает новый экземпляр
       """

    def __init__(self, matrix):
        """
            Создание матрицы
            Можно ввести как список списков и также как сжатое хранение строкой
        """
        if type(matrix[-1]) == int:  # Если матрица уже преобразовано в вид сжатой строки
            self.m = matrix
            return
        row_index = [0]  # строки
        column_index = []  # Столбцы
        values = []  # значения в матрице
        count = 0
        for i in range(len(matrix)):
            if len(matrix[i]) != len(matrix[0]):  # проверка на прямоугольность
                raise ValueError("Разное количество элементов в строках")
            for j in range(len(matrix[0])):
                if matrix[i][j] != 0:
                    count += 1
                    column_index.append(j)
                    values.append(matrix[i][j])
            row_index.append(count)
        self.m = [row_index, column_index, values, len(matrix[0])]

    def matrix(self):
        """
        Возвращает матрицу в виде сжатого хранения строкой
        :return: матрицу(сжатое хранение строкой)
        """
        return self.m

    def to_matrix(self):
        """
        Возвращает матрицу в виде списка списков
        :return: матрицу(список списков)
        """
        matrix = self.m
        matrix_tabl = [[0] * matrix[3] for _ in range(len(matrix[0]) - 1)]
        for i in range(1, len(matrix[0])):  # перебор строк от одного до количества строк(потому что список строк начинается все с 0)
            for j in range(matrix[0][i-1], matrix[0][i]):
                matrix_tabl[i - 1][matrix[1][j]] = matrix[2][j]
        return matrix_tabl

    def __add__(self, other):
        """
        Сложение двух матриц
        :param other: вторая матрица
        :return: возвращает новую матрицу, полученную в результате суммы двух матриц
        """
        matrix = copy.deepcopy(self.m)
        matrix_o = copy.deepcopy(other.m)
        if len(matrix[0]) != len(matrix_o[0]) or matrix[3] != matrix_o[3]: # проверка на размер
            raise IndexError("Матрицы разных размеров")
        for i in range(1, len(matrix[0])):
            count = 0
            column1 = matrix[1][matrix[0][i - 1]:matrix[0][i]]
            column2 = matrix_o[1][matrix_o[0][i - 1]:matrix_o[0][i]]

            for j in range(len(column2)):
                if column2[j] not in column1:  # так как нули мы в списках не обозначаем то нужнр проверить есть ли элемент в matrix_1 на определенном столцбе
                    ind = bisect.bisect(column1, column2[j])  # находим где должен стоять элемент
                    count += 1  # считаем чтобы после приюавить к количеству элементов в этой строке
                    column1.insert(ind, column2[j])
                    matrix[2].insert(ind + matrix[0][i - 1], matrix_o[2][matrix_o[0][i - 1]:matrix_o[0][i]][j])
                    # добавляем в matrix_1 в values элемент из matrix_2 так как его там нет, то есть мы складываем его с 0
                else:
                    matrix[2][column1.index(column2[j]) + matrix[0][i - 1]] += matrix_o[2][j + matrix_o[0][i - 1]]
                    # если элемент есть в matrix_1, то мы просто их складываем
            matrix[1][matrix[0][i - 1]:matrix[0][i]] = column1  # так как мы добавляли в список column_index значения из другой матрицы то мы сейчас перезаписываем этот кусок списка
            for k in range(i, len(matrix[0])): # добавляем к каждому элементу Count как так число наших значения в матрице могло измениться
                matrix[0][k] += count
        return Matrix(matrix)

    def __sub__(self, other):
        """
        Все то же самое, что и в функции __add__
        Разность двух матриц
        :param other: вторая матрица
        :return: возвращает новую матрицу, полученную в результате разности двух матриц
        """
        matrix = copy.deepcopy(self.m)
        matrix_o = copy.deepcopy(other.m)
        if len(matrix[0]) != len(matrix_o[0]) or matrix[3] != matrix_o[3]:
            raise IndexError("Матрицы разных размеров")
        for i in range(1, len(matrix[0])):
            count = 0
            column1 = matrix[1][matrix[0][i - 1]:matrix[0][i]]
            column2 = matrix_o[1][matrix_o[0][i - 1]:matrix_o[0][i]]

            for j in range(len(column2)):
                if column2[j] not in column1:
                    ind = bisect.bisect(column1, column2[j])
                    count += 1
                    column1.insert(ind, column2[j])
                    matrix[2].insert(ind + matrix[0][i - 1], 0 - matrix_o[2][matrix_o[0][i - 1]:matrix_o[0][i]][j])
                else:
                    matrix[2][column1.index(column2[j]) + matrix[0][i - 1]] -= matrix_o[2][j + matrix_o[0][i - 1]]
            matrix[1][matrix[0][i - 1]:matrix[0][i]] = column1
            for k in range(i, len(matrix[0])):
                matrix[0][k] += count
        return Matrix(matrix)

    def __mul__(self, other):  # написать комменатрии
        """
        Произведение двух матриц или умножение матрица на число
        :param other: вторая матрица или число
        :return: возвращает новую матрицу, полученную в результате произведения двух матриц или матрица на число
        """
        matrix = copy.deepcopy(self.m)
        if type(other) == int or type(other) == float:
            for i in range(len(matrix[2])):
                matrix[2][i] *= other
            matrix_answ = matrix
        else:
            matrix2 = copy.deepcopy(other.transposition().m)  # транспонируем, чтобы перемножать строка на строку
            if matrix[3] != matrix2[3]:
                raise IndexError("Количество столбцов не равно количеству строк")
            matrix_answ = [[0] * len(matrix[0]), [], [], len(matrix2[0])-1]
            for i in range(1, len(matrix[0])):
                matrix_answ[0][i] += matrix_answ[0][i - 1]

                column = 0
                column1 = matrix[1][matrix[0][i - 1]:matrix[0][i]]
                values1 = matrix[2][matrix[0][i - 1]:matrix[0][i]]

                for j in range(1, len(matrix2[0])):
                    value = 0
                    column2 = matrix2[1][matrix2[0][j - 1]:matrix2[0][j]]
                    values2 = matrix2[2][matrix2[0][j - 1]:matrix2[0][j]]

                    for k in range(len(column1)):
                        if column1[k] in column2:
                            value += values1[k] * values2[column2.index(column1[k])]

                    if value != 0:
                        matrix_answ[0][i] += 1
                        matrix_answ[1].append(column)
                        matrix_answ[2].append(value)

                    column += 1

        return Matrix(matrix_answ)

    def __rmul__(self, other):
        return self * other

    def __getitem__(self, item):
        """
        Получение строки или столбца номером item(matrix[:][0] - первый столбец)
        :param item: номер столбца или строки
        :return: список
        """
        matrix = copy.deepcopy(Matrix(self.m))
        if item == slice(None, None, None):
            matrix = matrix.transposition()
        else:
            if not isinstance(item, int):
                raise TypeError("Индекс должен быть целым числом")
            if item > len(matrix.matrix()[0]) - 2:
                raise IndexError("Индекс все списка")
        return matrix.to_matrix()[item]

    def transposition(self):
        """
        Транспонирование матрицы
        :return: новую матрицу
        """
        matrix = copy.deepcopy(self.m)
        matrix_answ = [[0] * (matrix[3] + 1), [], [], len(matrix[0])-1]
        for count in range(matrix[3]):
            matrix_answ[0][count + 1] += matrix_answ[0][count]
            for j in range(len(matrix[1])):
                if matrix[1][j] == count:
                    matrix_answ[0][count + 1] += 1
                    matrix_answ[1].append(bisect.bisect(matrix[0], j) - 1) # 0 строка переходит в 0 столбец, 1 строка в 1 столбец и тд
                    matrix_answ[2].append(matrix[2][j])
        return Matrix(matrix_answ)

    def delete(self, line, column):
        """
        Удаляет строку номером line и столбец номером column
        :param line: номер строки
        :param column: номер столбца
        :return: новая матрица
        """
        matrix = copy.deepcopy(self.m)
        if line > len(matrix[0]) - 1:
            raise IndexError("Индекс вне списка(строка)")
        elif column > matrix[3]:
            raise IndexError("Индекс вне списка(столбец)")

        del matrix[1][matrix[0][line - 1]:matrix[0][line]]
        del matrix[2][matrix[0][line - 1]:matrix[0][line]]
        count = matrix[0][line] - matrix[0][line - 1]
        for i in range(line + 1, len(matrix[0])):
            matrix[0][i] -= count
        del matrix[0][line]

        columns_arr = []
        for i in range(1, len(matrix[0])):
            columns_arr.append(matrix[1][matrix[0][i - 1]:matrix[0][i]])  # Разделает столбцы по строкам

        for i in range(len(columns_arr)):
            if (column - 1) in columns_arr[i]:
                for j in range(columns_arr[i].index(column - 1) + 1, len(columns_arr[i])):
                    matrix[1][j + matrix[0][i]] -= 1
                for j in range(i + 1, len(matrix[0])):
                    matrix[0][j] -= 1

                del matrix[1][matrix[0][i] + columns_arr[i].index(column - 1)]
                del matrix[2][matrix[0][i] + columns_arr[i].index(column - 1)]
                continue
            else:
                for j in range(len(columns_arr[i])):
                    if columns_arr[i][j] > column - 1:
                        matrix[1][j + matrix[0][i]] -= 1
        matrix[3] -= 1
        return Matrix(matrix)

    def __invert__(self):
        """
        Определитель матрицы (~matrix)
        :return: число
        """
        count = 0
        matrix = copy.deepcopy(self.m)
        if len(matrix[0]) - 1 != matrix[3]:
            raise IndexError("Не квадратная матрица")
        if len(matrix[0]) == 2 and len(matrix[2]) > 0:
            return matrix[2][0]
        elif len(matrix[2]) == 0:
            return 0
        else:
            for i in range(matrix[3]):
                m = Matrix(matrix).delete(1, i + 1)
                if i in matrix[1][matrix[0][0]:matrix[0][1]]:
                    count += matrix[2][matrix[1][matrix[0][0]:matrix[0][1]].index(i)] * ~m * (-1) ** (i + 2)
        return count

    def size(self):
        """
        Размер матрицы
        :return: строка
        """
        return f"{len(self.m[0]) - 1} на {self.m[3]}"

    def permutation(self, line_column: str, number_i, number_j):  # Сложно
        """
        Перестановка строк и столбцов (matrix.permutation("строка", 1, 2) - переставляем 1 строку и 2 строку)
        :param line_column: что переставляем: строку или столбец
        :param number_i: номер первой строки или первого столбца
        :param number_j: номер второй строки или второго столбца
        :return: новую матрицу
        """
        line_column = line_column.lower()
        matrix = copy.deepcopy(self.m)
        if line_column == "строка" and (number_i > len(matrix[0]) -1 or number_j > len(matrix[0])-1):
            raise IndexError("Индекс вне списка(строка)")
        elif line_column == "столбец" and (number_i > matrix[3] or number_j > matrix[3]):
            raise IndexError("Индекс вне списка(столбец)")
        if number_i > number_j:
            number_i, number_j = number_j, number_i

        if line_column == "строка":
            matrix[1][matrix[0][number_j - 1]:matrix[0][number_j]], matrix[1][matrix[0][number_i - 1]:matrix[0][number_i]] = matrix[1][matrix[0][number_i - 1]:matrix[0][number_i]], matrix[1][matrix[0][number_j - 1]:matrix[0][number_j]]
            matrix[2][matrix[0][number_j - 1]:matrix[0][number_j]], matrix[2][matrix[0][number_i - 1]:matrix[0][number_i]] = matrix[2][matrix[0][number_i - 1]:matrix[0][number_i]], matrix[2][matrix[0][number_j - 1]:matrix[0][number_j]]
            count_i = matrix[0][number_i] - matrix[0][number_i - 1]
            count_j = matrix[0][number_j] - matrix[0][number_j - 1]
            matrix[0][number_i] = matrix[0][number_i - 1] + count_j
            for i in range(number_i + 1, number_j):
                matrix[0][i] += count_j - count_i
            matrix[0][number_j] = matrix[0][number_j - 1] + count_i
        elif line_column == "столбец":
            number_i -= 1
            number_j -= 1
            for i in range(1, len(matrix[0])):
                if number_i in matrix[1][matrix[0][i - 1]:matrix[0][i]] and number_j in matrix[1][matrix[0][i - 1]:matrix[0][i]]:
                    t = matrix[2][matrix[0][i - 1]:matrix[0][i]]
                    t[matrix[1][matrix[0][i - 1]:matrix[0][i]].index(number_i)], t[matrix[1][matrix[0][i - 1]:matrix[0][i]].index(number_j)] = t[matrix[1][matrix[0][i - 1]:matrix[0][i]].index(number_j)], t[matrix[1][matrix[0][i - 1]:matrix[0][i]].index(number_i)]
                    matrix[2][matrix[0][i - 1]:matrix[0][i]] = t

                    t = matrix[1][matrix[0][i - 1]:matrix[0][i]]
                    t[matrix[1][matrix[0][i - 1]:matrix[0][i]].index(number_i)], t[matrix[1][matrix[0][i - 1]:matrix[0][i]].index(number_j)] = t[matrix[1][matrix[0][i - 1]:matrix[0][i]].index(number_j)], t[matrix[1][matrix[0][i - 1]:matrix[0][i]].index(number_i)]
                    t.sort()
                    matrix[1][matrix[0][i - 1]:matrix[0][i]] = t

                elif number_i in matrix[1][matrix[0][i - 1]:matrix[0][i]]:
                    t = matrix[1][matrix[0][i - 1]:matrix[0][i]]
                    t.insert(bisect.bisect(t, number_j), number_j)
                    del t[t.index(number_i)]
                    matrix[1][matrix[0][i - 1]:matrix[0][i]] = t

                elif number_j in matrix[1][matrix[0][i - 1]:matrix[0][i]]:
                    t = matrix[1][matrix[0][i - 1]:matrix[0][i]]
                    t.insert(bisect.bisect(t, number_i), number_i)
                    del t[t.index(number_j)]
                    matrix[1][matrix[0][i - 1]:matrix[0][i]] = t

        return Matrix(matrix)

    def __pow__(self, power, modulo=None):
        """
        Вычисляет обратную матрицу (matrix**(-1))
        :param power: в какую степень возводим
        :return: новая матрица
        """
        if power == -1:
            if ~Matrix(self.m) == 0:
                raise ZeroDivisionError("Обратная матрицы не существует")
            elif len(self.m[0]) - 1 != self.m[3]:
                raise IndexError("Матрица не квадратная")
            matrix = copy.deepcopy(self.m)
            matrix2 = [[0 for _ in range(len(matrix[0]))], [], [], matrix[3]]
            for i in range(1, matrix[3] + 1):
                matrix2[0][i] += matrix2[0][i - 1]
                for j in range(matrix[3]):
                    count = ~(Matrix(matrix).delete(i, j + 1)) * (-1) ** (i + j - 1)
                    if count != 0:
                        matrix2[0][i] += 1
                        matrix2[1].append(j)
                        matrix2[2].append(count)
            matrix2 = (Matrix(matrix2).transposition() * (1 / (~Matrix(matrix))))
            return matrix2


    def rang(self):
        matrix = copy.deepcopy(self.m)
        if matrix[3] <= 1 and len(matrix[2]) <= 1:
            return 1

        my_min = min(len(matrix[0]) - 1, matrix[3])
        for i in range(0, len(matrix[0]) - my_min):

            for j in range(0, matrix[3] - my_min + 1):
                matrix_answ = [[0]*(my_min+1), [], [], my_min]
                line = 0
                for k in range(len(matrix[1])):
                    line = bisect.bisect(matrix[0], k) - i
                    if j <= matrix[1][k] < j + my_min and 0 <= line - 1 < my_min:
                        matrix_answ[1].append(matrix[1][k]-j)
                        matrix_answ[2].append(matrix[2][k])
                        matrix_answ[0][line] += 1
                        if bisect.bisect(matrix[0], k+1) - i > line:
                            matrix_answ[0][line] += matrix_answ[0][line-1]
                if ~Matrix(matrix_answ) != 0:
                    return my_min

        m1 = Matrix(matrix_answ).delete(1, 1)
        m2 = Matrix(matrix_answ).delete(1, matrix[3])
        m3 = Matrix(matrix_answ).delete(len(matrix[0]) - 1, 1)
        m4 = Matrix(matrix_answ).delete(len(matrix[0]) - 1, matrix[3])

        return max(m1.rang(), m2.rang(), m3.rang(), m4.rang())

    # def rang(self):
    #     """
    #     Ранг матрица
    #     :return: число
    #     """
    #     matrix = copy.deepcopy(self.m)
    #     if matrix[3] == 1 and len(matrix[2]) <= 1:
    #         return 1
    #
    #     my_min = min(len(matrix[0]) - 1, matrix[3])
    #     count = 0
    #     for i in range(0, len(matrix[0]) - my_min):
    #         count += matrix[0][i]
    #         for j in range(0, matrix[3] - my_min + 1):
    #             matrix_answ = [matrix[0][i:my_min+1+i], [], [], my_min]
    #             matrix_answ[1] = matrix[1][matrix_answ[0][0]:matrix_answ[0][-1]]
    #             matrix_answ[2] = matrix[2][matrix_answ[0][0]:matrix_answ[0][-1]]
    #             for k in range(len(matrix_answ[0])):
    #                 matrix_answ[0][k] -= count
    #             print(matrix_answ)
    #             if ~Matrix(matrix_answ) != 0:
    #                 return my_min
    #
    #     m1 = Matrix(matrix_answ).delete(1, 1)
    #     m2 = Matrix(matrix_answ).delete(1, matrix[3])
    #     m3 = Matrix(matrix_answ).delete(len(matrix[0]) - 1, 1)
    #     m4 = Matrix(matrix_answ).delete(len(matrix[0]) - 1, matrix[3])
    #
    #     return max(m1.rang(), m2.rang(), m3.rang(), m4.rang())


m1 = Matrix([[0, 1, 0, 1, 0], [0, 0, 0, 3, 0], [0, 4, 0, 5, 0], [0, 6, 7, 8, 0], [9, 0, 0, 0, 0]])
m2 = Matrix([[0, 0, 2, 3, 3], [1, 2, 3, 0, 0], [0, 0, 0, 3, 0], [1, 2, 0, 7, 0], [2, 2, 0, 0, 0]])
m3 = Matrix([[0, 1, 0], [1, 0, 2], [0, 0, 2]])
m4 = Matrix([[1, -2, 3], [0, 4, -1], [5, 0, 0]])
m5 = Matrix([[0.5, 0, -1], [1, 0, 2], [2.3, 0, 17]])
m6 = Matrix([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])

m7 = Matrix([[1,2],[3,4],[5,6]])
m8 = Matrix([[1,2,3],[4,5,6],[7,8,9]])

m9 = Matrix([[0,0,-1,3],[1,1,0,2],[-1,-4,1,0]])
m10 = Matrix([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
m10.rang()
# print(m3.permutation("столбец",1,3).to_matrix())
