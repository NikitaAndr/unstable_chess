from const import *
from Figure import *


# расстановка фигур
class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        for i in range(8):
            self.field[1][i] = Pawn(1, i, WHITE)
            self.field[6][i] = Pawn(6, i, BLACK)
        for i in [(0, WHITE), (7, BLACK)]:
            self.field[i[0]][0] = Rook(i[0], 0, i[1])
            self.field[i[0]][1] = Knight(i[0], 1, i[1])
            self.field[i[0]][2] = Bishop(i[0], 2, i[1])
            self.field[i[0]][3] = Queen(i[0], 3, i[1])
            self.field[i[0]][4] = King(i[0], 4, i[1])
            self.field[i[0]][5] = Bishop(i[0], 5, i[1])
            self.field[i[0]][6] = Knight(i[0], 6, i[1])
            self.field[i[0]][7] = Rook(i[0], 7, i[1])

    def __repr__(self):
        stra = '     +----+----+----+----+----+----+----+----+ \n'

        for row in range(7, -1, -1):  # возможно списочное выражение
            stra += f'  {row}  '
            for col in range(8):
                stra += f'| {self.cell(row, col)} '
            stra += '|\n     +----+----+----+----+----+----+----+----+ \n'

        stra += '        ' + '    '.join([str(col) for col in range(8)])

        return stra

    @staticmethod
    def correct_coordinates(row, col):
        """Функция проверяет, что координаты (row, col) лежат
        внутри доски"""
        return 0 <= row < 8 and 0 <= col < 8

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        if not self.correct_coordinates(row, col) or not self.correct_coordinates(row1, col1):
            return False
        # проверка на не вылезают ли за пределы доски
        if row == row1 and col == col1:
            return False
        # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        # тут ничего нет
        if piece.get_color() != self.color:
            return False
        # куда без очереди ходишь
        if not piece.can_move(row1, col1):
            return False
        # # спрашиваем у фигуры может ли она походить
        # # я писал
        # # if [None] * 7 not in self.field[row]:
        # #     q = [k for i in enumerate(field[row][:self.col]) if type(i) != Rook or i != [None]]
        # if type(piece) == Rook:
        #     if [None] * 7 not in self.field[row]:
        #         ogr_s_leva = max([*[k for k, i in enumerate(self.field[row][:col])
        #                             if type(i) != Rook or i != [None]], -1])
        #         ogr_s_prava = min(
        #             [*[k + 1 for k, i in enumerate(self.field[row][col + 1:])
        #                if type(i) != Rook or i != [None]], 9])
        #         if not ogr_s_leva <= col1 <= ogr_s_prava:
        #             return False
        #     sp_vertik = [self.field[i][0] for i in range(8)]
        #     if [None] * 7 not in sp_vertik:
        #         ogr_s_verx = min(
        #             [*[k + 1 for k, i in enumerate(sp_vertik[row + 1:])
        #                if type(i) != Rook or i != [None]], 9])
        #         ogr_s_niz = max([*[k for k, i in enumerate(sp_vertik[:row])
        #                            if type(i) != Rook or i != [None]], -1])
        #         if not ogr_s_niz <= row1 <= ogr_s_verx:
        #             return False
        # if type(piece) == Bishop:
        #     sp_vertik = []
        #     sp_vertik1 = []
        #     for i in range(8):
        #         for j in range(8):
        #             if piece.col - piece.row == j - i:
        #                 sp_vertik.append(self.field[i][j])
        #             if piece.col + piece.row == j + i:
        #                 sp_vertik1.append(self.field[i][j])
        #     if piece.col - piece.row == col1 - row1:
        #         if not can_xod_Bishop(sp_vertik, row, row1):
        #             return False
        #     if piece.col + piece.row == col1 + row1:
        #         if not can_xod_Bishop(sp_vertik1, row, row1):
        #             return False
        # if type(piece) == Queen:
        #     if [None] * 7 not in self.field[row]:
        #         ogr_s_leva = max(
        #             [*[k for k, i in enumerate(self.field[row][:col])
        #                if type(i) != Queen or i != [None]], -1])
        #         ogr_s_prava = min(
        #             [*[k + 1 for k, i in enumerate(self.field[row][col + 1:])
        #                if type(i) != Queen or i != [None]], 9])
        #         if not ogr_s_leva <= col1 <= ogr_s_prava:
        #             return False
        #     sp_vertik = [self.field[i][0] for i in range(8)]
        #     if [None] * 7 not in sp_vertik:
        #         ogr_s_verx = min(
        #             [*[k + 1 for k, i in enumerate(sp_vertik[row + 1:])
        #                if type(i) != Queen or i != [None]], 9])
        #         ogr_s_niz = max([*[k for k, i in enumerate(sp_vertik[:row])
        #                            if type(i) != Queen or i != [None]], -1])
        #         if not ogr_s_niz <= row1 <= ogr_s_verx:
        #             return False
        #     sp_vertik = []
        #     sp_vertik1 = []
        #     for i in range(8):
        #         for j in range(8):
        #             if piece.col - piece.row == j - i:
        #                 sp_vertik.append(self.field[i][j])
        #             if piece.col + piece.row == j + i:
        #                 sp_vertik1.append(self.field[i][j])
        #     if piece.col - piece.row == col1 - row1:
        #         if not can_xod_Bishop(sp_vertik, row, row1):
        #             return False
        #     if piece.col + piece.row == col1 + row1:
        #         if not can_xod_Bishop(sp_vertik1, row, row1):
        #             return False
        # if type(piece) == King:
        #     if self.field[row1][col1] != [None]:
        #         return False

        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        self.color = not self.color
        return True

    def is_under_attack(self, row, col, color):
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if not self.field[i][j] is None:
                    if self.field[i][j].color == color:
                        if self.field[i][j].can_move(row, col):
                            return True


def can_xod_Bishop(sp_troektoriy, row, row1):
    ogr_s_niz = max([*[k for k, i in enumerate(sp_troektoriy[:row])
                       if type(i) != Bishop and i is not None], -1])
    # только и только потому что нули у списака и матрицы cовпадают
    ogr_s_verh = min([*[k for k, i in enumerate(sp_troektoriy[row:])
                        if type(i) != Bishop and i is not None], len(sp_troektoriy) + 1])
    if not ogr_s_niz < row1 < ogr_s_verh:
        return False
    return True


def can_xod_Queen(sp_troektoriy, row, row1):
    ogr_s_niz = max([*[k for k, i in enumerate(sp_troektoriy[:row])
                       if type(i) != Queen and i is not None], -1])
    # только и только потому что нули у списака и матрицы cовпадают
    ogr_s_verh = min(
        [*[k for k, i in enumerate(sp_troektoriy[row:])
           if type(i) != Queen and i is not None], len(sp_troektoriy) + 1])
    if not ogr_s_niz < row1 < ogr_s_verh:
        return False
    return True