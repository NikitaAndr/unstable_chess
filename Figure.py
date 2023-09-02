import pygame.transform

from const import *


class Figure:
    def __init__(self, row, col, color: bool):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def get_color(self):
        return self.color

    def can_move(self, board, new_row, new_col):
        if board[new_row][new_col] is not None:
            return False

    @staticmethod
    def check_path_empty(self, board, new_row, new_col):
        return True

    def char(self): ...

    @staticmethod
    def get_pos_img_in_sp():
        return 1

    def get_img(self):
        return pygame.transform.scale(load_image(f'img.png').
                                      subsurface(200 * (self.get_pos_img_in_sp() - 1),
                                                 200 * int(not self.color),
                                                 200, 200),
                                      (cell_size, cell_size))


class Pawn(Figure):
    def __init__(self, row, col, color):
        super(Pawn, self).__init__(row, col, color)
        self.first_move = row
        self.direction = 1 if self.color else -1

    def can_move(self, board, row, col):
        super(Pawn, self).can_move(board, row, col)
        if self.col != col:
            return False
        if self.short_move(row) or self.big_move(row):
            return True
        return False

    def short_move(self, row):
        """Ход на 1 клетку"""
        return self.row + self.direction == row

    def big_move(self, row):
        """Ход на 2 клетки"""
        return self.row == self.first_move and self.row + 2 * self.direction == row

    def check_path_empty(self, board, new_row, new_col):
        return self.short_move(new_row)

    def char(self):
        return 'P'

    @staticmethod
    def get_pos_img_in_sp():
        return 6


class Knight(Figure):
    # пока не трогаю, но можно сделать через модуль от разницы прошлой и настоящей координаты
    def can_move(self, board, new_row, new_col):
        super(Knight, self).can_move(board, new_row, new_col)
        if ((self.row + 1 == new_row and self.col + 2 == new_col)
                or (self.row - 1 == new_row and self.col + 2 == new_col)
                or (self.row + 1 == new_row and self.col - 2 == new_col)
                or (self.row - 1 == new_row and self.col - 2 == new_col)
                or (self.row + 2 == new_row and self.col + 1 == new_col)
                or (self.row - 2 == new_row and self.col + 1 == new_col)
                or (self.row + 2 == new_row and self.col - 1 == new_col)
                or (self.row - 2 == new_row and self.col - 1 == new_col)):
            return True

    def char(self):
        return 'N'

    @staticmethod
    def get_pos_img_in_sp():
        return 4


class Bishop(Figure):
    def can_move(self, board, new_row, new_col):
        super(Bishop, self).can_move(board, new_row, new_col)
        if self.col - self.row == new_col - new_row:
            return self.check_path_empty(board, new_row, new_col)
        if self.col + self.row == new_col + new_row:
            return self.check_path_empty(board, new_row, new_col, True)
        return False

    def check_path_empty(self, board, new_row, new_col, is_primary_diagonal=False):
        direction_row = 1 if new_row - self.row > 0 else -1
        direction_col = 1 if new_col - self.col > 0 else -1
        direction_col *= 1 if is_primary_diagonal else -1
        for i in range(1,
                       abs(self.row - new_row) - 1):  # полная версия: max(abs(self.row - new_row), abs(self.col - new_col))
            checked_cor = board[self.row + i * direction_row][self.col + i * direction_col]
            if checked_cor is not None:
                return False
        return True

    def char(self):
        return 'B'

    @staticmethod
    def get_pos_img_in_sp():
        return 3


class Rook(Knight):
    def can_move(self, board, new_row, new_col):
        super(Rook, self).can_move(board, new_row, new_col)
        if self.row == new_row:
            return self.check_path_row_empty(board, new_row)
        if self.col == new_col:
            return self.check_path_col_empty(board, new_col)
        return False

    def check_path_row_empty(self, board, new_row):
        direction = 1 if self.row - new_row > 0 else -1
        for i in range(1, abs(self.row - new_row) - 1):
            if board[self.row + i * direction][self.col] is not None:
                return False
        return True

    def check_path_col_empty(self, board, new_col):
        direction = 1 if self.col - new_col > 0 else -1
        for i in range(1, abs(self.col - new_col) - 1):
            if board[self.row][self.col + i * direction] is not None:
                return False
        return True

    def char(self):
        return 'R'

    @staticmethod
    def get_pos_img_in_sp():
        return 5


class Queen(Bishop, Rook):
    def can_move(self, board, new_row, new_col):
        return Bishop.can_move(self, board, new_row, new_col) or Rook.can_move(self, board, new_row, new_col)

    def char(self):
        return 'Q'

    @staticmethod
    def get_pos_img_in_sp():
        return 2


class King(Figure):
    def can_move(self, board, new_row, new_col):
        if abs(self.row - new_row) == 1 and abs(self.col - new_col) == 1 and board[new_row][new_col] is None:
            return True

    def char(self):
        return 'K'

    @staticmethod
    def get_pos_img_in_sp():
        return 1
