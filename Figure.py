"""Модуль всех фигур.

Импорты сторонних библиотек:
pygame - в классе каждой из фигур есть функция get_img, которая выдаёт изображение этой фигуры в типе pygame-а,

Импорты модулей проекта:
const: load_image, cell_size - также требуются для создания изображения в get_img,


can_move_parent - декоратор проверяющий может ли на то поле сходить родитель,
copy - копирование 2 фигур,

Figure - класс-родитель всех фигур,
Pawn - класс Пешки,
Knight - класс Коня,
Bishop - класс Слона,
Rook - класс Ладьи,
Queen - класс Королевы,
King - класс Короля."""

import pygame.transform
from const import load_image, cell_size


def can_move_parent(can_move):
    def can_move_new(*args, **kwargs):
        if not Figure.can_move(*args, *kwargs):
            return False

        return can_move(*args, *kwargs)

    return can_move_new


class Figure:
    """Класс-родитель (интерфейс, абстрактный класс) фигур."""

    def __init__(self, row, col, color: bool):
        """Инициализация полей.

        Публичные поля:
        row - строка, где сейчас стоит фигура
        col - колонка, где сейчас стоит фигура
        color - цвет фигуры."""
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row: int, col: int):
        """Измени координаты фигуры на строку row и колонку col (не рекомендуется вылезать за доску)."""
        self.row = row
        self.col = col

    def get_color(self):
        """Дай цвет фигуры."""
        return self.color

    def is_enemy(self, figure):
        """Проверь, вот эта (figure) фигура для меня враг?"""
        if figure is None:
            return False
        return figure.get_color() != self.get_color()

    def can_move(self, board, new_row, new_col):
        """Проверь, могу ли я сходить на поле по координатам row, col доски board."""
        move_place = board[new_row][new_col]
        return not (self.is_enemy(move_place) or None)

    @staticmethod
    def check_path_empty(board, new_row, new_col):
        """Проверь, свободен ли путь для хода на координаты new_row, new_col доски board."""
        return True

    def char(self):
        """Дай буквенное представление."""

    def get_img(self):
        """Дай представление в виде изображения."""
        return pygame.transform.scale(load_image(f'img.png').
                                      subsurface(200 * (self.get_pos_img_in_sp() - 1),
                                                 200 * int(not self.color),
                                                 200, 200),
                                      (cell_size, cell_size))

    @staticmethod
    def get_pos_img_in_sp():
        """Верни порядковый номер среди изображений."""
        return 1


class Pawn(Figure):
    """Класс пешки."""

    def __init__(self, row, col, color):
        """Расширить инициализацию полей.

        Приватные:
        _first_move - хранит исходное положение пешки,
        _direction - хранит направление пешки."""

        super(Pawn, self).__init__(row, col, color)
        self._first_move = row
        self._direction = 1 if self.color else -1

    def can_move(self, board, row, col):
        move_place = board[row][col]
        if self.can_eat(move_place, row, col):
            return True
        if self.short_move(move_place, row, col) or self.big_move(move_place, row, col):
            return True
        return False

    def short_move(self, move_place, row, col):
        """Передвинь пешку на поле move_place с координатами row col на расстоянии 1 клетки."""
        return (move_place is None and
                self.col == col and
                self.row + self._direction == row)

    def big_move(self, move_place, row, col):
        """Передвинь пешку на поле move_place с координатами row col на расстоянии 2 клетки."""
        return (move_place is None and
                self.col == col and
                self.row == self._first_move and self.row + 2 * self._direction == row)

    def can_eat(self, move_place, row, col):
        """Проверь, могу ли я съесть фигуру на поле move_place, которое расположено по координатам row, col."""
        if (self.is_enemy(move_place) and
                self.row == row - self._direction and
                (self.col + 1 == col or self.col - 1 == col)):
            return True
        return False

    def check_path_empty(self, board, new_row, new_col):
        return self.short_move(board[new_row][new_col], new_row, new_col)

    def char(self):
        return 'P'

    @staticmethod
    def get_pos_img_in_sp():
        return 6


class Knight(Figure):
    """Класс коня."""

    # пока не трогаю, но можно сделать через модуль от разницы прошлой и настоящей координаты
    @can_move_parent
    def can_move(self, board, new_row, new_col):
        if ((self.row + 1 == new_row and self.col + 2 == new_col)
                or (self.row - 1 == new_row and self.col + 2 == new_col)
                or (self.row + 1 == new_row and self.col - 2 == new_col)
                or (self.row - 1 == new_row and self.col - 2 == new_col)
                or (self.row + 2 == new_row and self.col + 1 == new_col)
                or (self.row - 2 == new_row and self.col + 1 == new_col)
                or (self.row + 2 == new_row and self.col - 1 == new_col)
                or (self.row - 2 == new_row and self.col - 1 == new_col)):
            return True
        return False

    def char(self):
        return 'N'

    @staticmethod
    def get_pos_img_in_sp():
        return 4


class Bishop(Figure):
    """Класс слона."""

    @can_move_parent
    def can_move(self, board, new_row, new_col):
        if ((self.col - self.row == new_col - new_row) or
                (self.col + self.row == new_col + new_row)):
            return self.check_path_empty(board, new_row, new_col)
        return False

    def check_path_empty(self, board, new_row, new_col):
        direction_row = 1 if new_row - self.row > 0 else -1
        direction_col = 1 if new_col - self.col > 0 else -1
        for i in range(1, abs(self.row - new_row)):
            checked_cor = board[self.row + i * direction_row][self.col + i * direction_col]
            if checked_cor is not None:
                return False
        return True

    def char(self):
        return 'B'

    @staticmethod
    def get_pos_img_in_sp():
        return 3


class Rook(Figure):
    """Класс ладьи."""

    def __init__(self, row, col, color: bool):
        """Расширить инициализацию

        Публичное поле:
        can_castle - способность ладьи к рокировке, убирается при первом ходе."""

        super(Rook, self).__init__(row, col, color)
        self.can_castle = True

    def set_position(self, row, col):
        super(Rook, self).set_position(row, col)
        self.can_castle = False

    @can_move_parent
    def can_move(self, board, new_row, new_col):
        if (self.row == new_row) or (self.col == new_col):
            return self.check_path_empty(board, new_row, new_col)
        return False

    def check_path_empty(self, board, new_row, new_col):
        return self.check_path_row_empty(board, new_col) or self.check_path_col_empty(board, new_col)

    def check_path_col_empty(self, board, new_row):
        """Проверь, свободен ли путь по горизонтали под номером new_row доски board."""
        direction = 1 if self.row - new_row < 0 else -1
        for i in range(1, abs(self.row - new_row)):
            if board[self.row + i * direction][self.col] is not None:
                return False
        return True

    def check_path_row_empty(self, board, new_col):
        """Проверь, свободен ли путь по вертикали под номером new_row доски board."""
        direction = 1 if self.col - new_col < 0 else -1
        for i in range(1, abs(self.col - new_col)):
            if board[self.row][self.col + i * direction] is not None:
                return False
        return True

    def char(self):
        return 'R'

    @staticmethod
    def get_pos_img_in_sp():
        return 5


class Queen(Figure):
    """Класс королевы (ферзя, визиря)."""
    def can_move(self, board, new_row, new_col):
        if ((self.col - self.row == new_col - new_row) or
                (self.col + self.row == new_col + new_row) or
                (self.row == new_row) or
                (self.col == new_col)):
            return self.check_path_empty(board, new_row, new_col)

    def check_path_empty(self, board, new_row, new_col):
        return (self.check_path_col_empty(board, new_row) or
                self.check_path_row_empty(board, new_col) or
                self.check_path_diagonal_empty(board, new_row, new_col))

    def check_path_col_empty(self, board, new_row):
        """Проверь, свободен ли путь по горизонтали под номером new_row доски board."""
        direction = 1 if self.row - new_row < 0 else -1
        for i in range(1, abs(self.row - new_row)):
            if board[self.row + i * direction][self.col] is not None:
                return False
        return True

    def check_path_row_empty(self, board, new_col):
        """Проверь, свободен ли путь по вертикали под номером new_row доски board."""
        direction = 1 if self.col - new_col < 0 else -1
        for i in range(1, abs(self.col - new_col)):
            if board[self.row][self.col + i * direction] is not None:
                return False
        return True

    def check_path_diagonal_empty(self, board, new_row, new_col):
        """Проверь, свободен ли путь по диагонали до координаты new_row, new_col доски board."""
        direction_row = 1 if new_row - self.row > 0 else -1
        direction_col = 1 if new_col - self.col > 0 else -1
        for i in range(1, abs(self.row - new_row)):
            checked_cor = board[self.row + i * direction_row][self.col + i * direction_col]
            if checked_cor is not None:
                return False
        return True

    def char(self):
        return 'Q'

    @staticmethod
    def get_pos_img_in_sp():
        return 2


class King(Figure):
    """Класс короля (шаха)."""
    def __init__(self, row, col, color: bool):
        """Расширить инициализацию

        Публичное поле:
        can_castle - способность ладьи к рокировке, убирается при первом ходе."""
        super(King, self).__init__(row, col, color)
        self.can_castle = True

    def set_position(self, row, col):
        super(King, self).set_position(row, col)
        self.can_castle = False

    @can_move_parent
    def can_move(self, board, new_row, new_col):
        if abs(self.row - new_row) <= 1 and abs(self.col - new_col) <= 1:
            return True

    def char(self):
        return 'K'

    @staticmethod
    def get_pos_img_in_sp():
        return 1


def copy(copy_obj: Figure, cls: type):
    """Функция копирования copy_obj в cls.

    copy_obj - копируемый объект
    cls - тип скопированного объекта."""
    return cls(copy_obj.row, copy_obj.col, copy_obj.color)
