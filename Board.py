from const import *
from Figure import *


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = [[None] * 8 for _ in range(8)]
        self.arrange_pawns()
        self.arrange_senior_figures()

    def __repr__(self):
        stra = '     +----+----+----+----+----+----+----+----+ \n'
        for row in range(7, -1, -1):  # возможно списочное выражение
            stra += f'  {row}  '
            for col in range(8):
                stra += f'| {self.get_cell(row, col)} '
            stra += '|\n     +----+----+----+----+----+----+----+----+ \n'
        stra += '        ' + '    '.join([str(col) for col in range(8)])

        return stra

    def arrange_pawns(self):
        for i in range(8):
            self.field[1][i] = Pawn(1, i, WHITE)
            self.field[6][i] = Pawn(6, i, BLACK)

    def arrange_senior_figures(self):
        for i in [(0, WHITE), (7, BLACK)]:
            self.field[i[0]][0] = Rook(i[0], 0, i[1])
            self.field[i[0]][1] = Knight(i[0], 1, i[1])
            self.field[i[0]][2] = Bishop(i[0], 2, i[1])
            self.field[i[0]][3] = Queen(i[0], 3, i[1])
            self.field[i[0]][4] = King(i[0], 4, i[1])
            self.field[i[0]][5] = Bishop(i[0], 5, i[1])
            self.field[i[0]][6] = Knight(i[0], 6, i[1])
            self.field[i[0]][7] = Rook(i[0], 7, i[1])

    @staticmethod
    def correct_coordinates(row, col) -> bool:
        """Функция проверяет, что координаты (row, col) лежат
        внутри доски"""
        return 0 <= row < 8 and 0 <= col < 8

    @staticmethod
    def convert_chess_math(stra: str):
        cor, new_cor = stra.split('-')
        col = ord(cor[0]) - ord('a')
        col1 = ord(new_cor[0]) - ord('a')
        row = int(cor[1]) - 1
        row1 = int(new_cor[1]) - 1
        return (row, col), (row1, col1)

    def make_move(self, stra: str):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""
        cor, new_cor = self.convert_chess_math(stra.replace(' ', ''))
        if not self.check_cords(cor, new_cor):
            return False

        piece = self.field[cor[0]][cor[1]]
        if not self.check_move_piece(piece, new_cor):
            return False
        self.move_piece(piece, *cor, *new_cor)

        return True

    def check_cords(self, cor, new_cor):
        if cor == new_cor:
            return False
        if not self.correct_coordinates(*cor):
            return False
        if not self.correct_coordinates(*new_cor):
            return False
        return True

    def check_move_piece(self, piece, new_cor):
        if piece is None:
            return False
        if not self.is_current_player(piece.get_color()):
            return False
        if not piece.can_move(self.field, *new_cor):
            return False
        return True

    def move_piece(self, piece, row, col, row1, col1):
        self.field[row][col] = None
        self.field[row1][col1] = piece
        piece.set_position(row1, col1)
        self.color = not self.color

    def is_under_attack(self, row, col, color):
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                if self.field[i][j] is not None:
                    if self.field[i][j].color == color:
                        if self.field[i][j].can_move(self.field, row, col):
                            return True

    def is_current_player(self, other_color):
        return self.color == other_color

    def get_cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        c = 'w' if piece.get_color() == WHITE else 'b'
        return c + piece.char()
