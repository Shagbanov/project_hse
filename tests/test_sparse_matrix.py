import pytest
from sparse_matrix import Matrix

m1 = Matrix([[0, 1, 0, 1, 0], [0, 0, 0, 3, 0], [0, 4, 0, 5, 0], [0, 6, 7, 8, 0], [9, 0, 0, 0, 0]])
m2 = Matrix([[0, 0, 2, 3, 3], [1, 2, 3, 0, 0], [0, 0, 0, 3, 0], [1, 2, 0, 7, 0], [2, 2, 0, 0, 0]])
m3 = Matrix([[0, 1, 0], [1, 0, 2], [0, 0, 2]])
m4 = Matrix([[1, -2, 3], [0, 4, -1], [5, 0, 0]])
m5 = Matrix([[0.5, 0, -1], [1, 0, 2], [2.3, 0, 17]])
m6 = Matrix([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])


def test_add():
    assert (m1 + m2).to_matrix() == [[0, 1, 2, 4, 3], [1, 2, 3, 3, 0], [0, 4, 0, 8, 0], [1, 8, 7, 15, 0],
                                     [11, 2, 0, 0, 0]]
    assert (m3 + m4).to_matrix() == [[1, -1, 3], [1, 4, 1], [5, 0, 2]]
    assert (m4 + m5).to_matrix() == [[1.5, -2, 2], [1, 4, 1], [7.3, 0, 17]]
    with pytest.raises(IndexError):
        assert m1 + m4


def test_sub():
    assert (m1 - m2).to_matrix() == [[0, 1, -2, -2, -3], [-1, -2, -3, 3, 0], [0, 4, 0, 2, 0], [-1, 4, 7, 1, 0],
                                     [7, -2, 0, 0, 0]]
    assert (m3 - m4).to_matrix() == [[-1, 3, -3], [1, -4, 3], [-5, 0, 2]]
    assert (m4 - m5).to_matrix() == [[0.5, -2, 4], [-1, 4, -3], [2.7, 0, -17]]
    with pytest.raises(IndexError):
        assert m1 - m4


def test_mul():
    assert (m1 * m2).to_matrix() == [[2, 4, 3, 7, 0], [3, 6, 0, 21, 0], [9, 18, 12, 35, 0], [14, 28, 18, 77, 0],
                                     [0, 0, 18, 27, 27]]
    assert (m3 * m4).to_matrix() == [[0, 4, -1], [11, -2, 3], [10, 0, 0]]
    assert (m4 * m3).to_matrix() == [[-2, 1, 2], [4, 0, 6], [0, 5, 0]]
    assert (m3 * 2).to_matrix() == [[0, 2, 0], [2, 0, 4], [0, 0, 4]]
    with pytest.raises(IndexError):
        assert m1 * m4


def test_slice():
    assert m1[0] == [0, 1, 0, 1, 0]
    assert m2[0] == [0, 0, 2, 3, 3]
    assert m3[0] == [0, 1, 0]
    assert m4[:][0] == [1, 0, 5]
    assert m4[:][2] == [3, -1, 0]
    with pytest.raises(TypeError):
        assert m1[1.2]
    with pytest.raises(TypeError):
        assert m1['a']
    with pytest.raises(IndexError):
        assert m1[6]


def test_transposition():
    assert m1.transposition().to_matrix() == [[0, 0, 0, 0, 9], [1, 0, 4, 6, 0], [0, 0, 0, 7, 0], [1, 3, 5, 8, 0],
                                              [0, 0, 0, 0, 0]]
    assert m3.transposition().to_matrix() == [[0, 1, 0], [1, 0, 0], [0, 2, 2]]
    assert m4.transposition().to_matrix() == [[1, 0, 5], [-2, 4, 0], [3, -1, 0]]


def test_delete():
    assert m1.delete(1, 2).to_matrix() == [[0, 0, 3, 0], [0, 0, 5, 0], [0, 7, 8, 0], [9, 0, 0, 0]]
    assert m3.delete(3, 3).to_matrix() == [[0, 1], [1, 0]]
    assert m4.delete(3, 1).to_matrix() == [[-2, 3], [4, -1]]
    with pytest.raises(IndexError):
        assert m1.delete(1, 6)
    with pytest.raises(IndexError):
        assert m3.delete(4, 1)


def test_determinant():  # ~
    assert ~m1 == 0
    assert ~m2 == -54
    assert ~m3 == -2
    with pytest.raises(IndexError):
        assert ~m6


def test_size():
    assert m1.size() == f"{len(m1.matrix()[0]) - 1} на {m1.matrix()[3]}"
    assert m2.size() == f"{len(m2.matrix()[0]) - 1} на {m2.matrix()[3]}"
    assert m3.size() == f"{len(m3.matrix()[0]) - 1} на {m3.matrix()[3]}"
    assert m4.size() == f"{len(m4.matrix()[0]) - 1} на {m4.matrix()[3]}"


def test_permutation():
    assert m1.permutation("строка", 1, 2).to_matrix() == [[0, 0, 0, 3, 0], [0, 1, 0, 1, 0], [0, 4, 0, 5, 0],
                                                          [0, 6, 7, 8, 0],
                                                          [9, 0, 0, 0, 0]]
    assert m3.permutation("столбец", 1, 3).to_matrix() == [[0, 1, 0], [2, 0, 1], [2, 0, 0]]
    assert m4.permutation("строка", 1, 2).to_matrix() == [[0, 4, -1], [1, -2, 3], [5, 0, 0]]
    with pytest.raises(IndexError):
        assert m1.permutation("Строка", 1, 6)
    with pytest.raises(IndexError):
        assert m3.permutation("Строка", 4, 1)


def test_reverse():  # **(-1)
    # assert m1
    assert (m2 ** (-1)).to_matrix() == [[0, 0, 2.333333333333333, -1.0, 1.0], [0, 0, -2.333333333333333, 1.0, -0.5],
                                        [0, 0.3333333333333333, 0.7777777777777777, -0.3333333333333333, 0],
                                        [0, 0, 0.3333333333333333, 0, 0],
                                        [0.3333333333333333, -0.2222222222222222, -0.8518518518518519,
                                         0.2222222222222222, 0]]
    assert (m3 ** (-1)).to_matrix() == [[0, 1.0, -1.0], [1.0, 0, 0], [0, 0, 0.5]]
    assert (m4 ** (-1)).to_matrix() == [[0, 0, 0.2], [0.1, 0.3, -0.02], [0.4, 0.2, -0.08]]
    with pytest.raises(ZeroDivisionError):
        assert m1 ** (-1)
    with pytest.raises(IndexError):
        assert m6 ** (-1)


def test_rang():
    assert m1.rang() == 4
    assert m2.rang() == 5
    assert m3.rang() == 3


def test_to_matrix():
    assert m1.to_matrix() == [[0, 1, 0, 1, 0], [0, 0, 0, 3, 0], [0, 4, 0, 5, 0], [0, 6, 7, 8, 0], [9, 0, 0, 0, 0]]
    assert m2.to_matrix() == [[0, 0, 2, 3, 3], [1, 2, 3, 0, 0], [0, 0, 0, 3, 0], [1, 2, 0, 7, 0], [2, 2, 0, 0, 0]]
    assert m3.to_matrix() == [[0, 1, 0], [1, 0, 2], [0, 0, 2]]
