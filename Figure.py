class Figure:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col
        # ошибка может быть

    def get_color(self):
        return self.color

    def can_move(self, new_row, new_col): ...

    def char(self): ...


class Pawn(Figure):
    def __init__(self, row, col, color):
        super(Pawn, self).__init__(row, col, color)
        self.first_move = row
        self.direction = 1 if self.color else -1  # вектор увеличения координат

    def can_move(self, row, col):
        if self.col != col:
            return False
        if self.short_move(row) or self.big_move(row):
            return True

    def short_move(self, row):
        # ход на 1 клетку
        return self.row + self.direction == row

    def big_move(self, row):
        # ход на 2 клетку
        return self.row == self.first_move and self.row + 2 * self.direction == row

    def char(self):
        return 'P'


class Knight(Figure):
    # пока не трогаю, но можно сделать через модуль от разницы прошлой и настоящей координаты
    def can_move(self, new_row, new_col):
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


class Bishop(Knight):
    def can_move(self, new_row, new_col):
        can_move_black = self.col - self.row == new_col - new_row
        can_move_white = self.col + self.row == new_col + new_row
        if can_move_black or can_move_white:
            return True

    def char(self):
        return 'B'


class Rook(Knight):
    def can_move(self, row, col):
        if self.row == row or self.col == col:
            return True

    def char(self):
        return 'R'


class Queen(Bishop, Rook):
    def can_move(self, new_row, new_col):
        return Bishop.can_move(self, new_row, new_col) or Rook.can_move(self, new_row, new_col)



    def char(self):
        return 'Q'


class King(Figure):
    def can_move(self, new_row, new_col):
        if abs(self.row - new_row) == 1 and abs(self.col - new_col) == 1:
            return True

    def char(self):
        return 'K'
