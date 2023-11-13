from const import *
from Figure import *
import convert


class Board:
    def __init__(self):
        self.color = WHITE
        self.mate = False

        self.board = [[None] * 8 for _ in range(8)]
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

    def backstage_print(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j])

    def arrange_pawns(self):
        for i in range(8):
            self.board[1][i] = Pawn(1, i, WHITE)
            self.board[6][i] = Pawn(6, i, BLACK)

    def arrange_senior_figures(self):
        for i in [(0, WHITE), (7, BLACK)]:
            self.board[i[0]][0] = Rook(i[0], 0, i[1])
            self.board[i[0]][1] = Knight(i[0], 1, i[1])
            self.board[i[0]][2] = Bishop(i[0], 2, i[1])
            self.board[i[0]][3] = Queen(i[0], 3, i[1])
            self.board[i[0]][4] = King(i[0], 4, i[1])
            self.board[i[0]][5] = Bishop(i[0], 5, i[1])
            self.board[i[0]][6] = Knight(i[0], 6, i[1])
            self.board[i[0]][7] = Rook(i[0], 7, i[1])

    @staticmethod
    def correct_coordinates(row, col) -> bool:
        """Функция проверяет, что координаты (row, col) лежат
        внутри доски"""
        return 0 <= row < 8 and 0 <= col < 8

    def make_moves(self, stra: str | tuple | list):
        for i in stra.split():
            if '.' not in i:  # тк иначе i[-1] - это обозначение хода по порядку
                self.make_move(i)

    def make_move(self, stra: str | tuple | list):
        cor, new_cor, transformation_figure = convert.chess_math(stra) if (type(stra) is str) else stra
        if not self.check_cords(cor, new_cor):
            return False  # можно все False заменить на raise, лучше с точки зрения архитектуры
        if not self.check_move_piece(piece := self.board[cor[0]][cor[1]], new_cor):
            return False
        self.move_piece(piece, *cor, *new_cor)
        return True

    def chess_check(self, piece):
        """Проверка шаха, если да, то фигура возвращается"""
        if isinstance(piece, King) and self.is_under_attack(piece):
            return True
        if self.is_under_attack(self.get_figure(King, self.color)[0]):  # возможны проблемы при режиме "анархия"
            return True
        return False

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
        if not (piece.can_move(self.board, *new_cor) or
                self.can_short_castling(piece.row, piece.col, *new_cor) or
                self.can_long_castling(piece.row, piece.col, *new_cor)):
            return False
        return True

    def can_short_castling(self, row, col, new_row, new_col):
        if not self.correct_coordinates(row, col + 3):
            return False

        king, rook = self.board[row][col], self.board[row][col + 3]
        if not (isinstance(king, King) and isinstance(rook, Rook) and
                king.can_castle and rook.can_castle and
                row == new_row and col + 2 == new_col and
                self.board[row][col + 1] is None and self.board[row][col + 2] is None):
            return False

        self.move_piece(rook, row, col + 3, new_row, col + 1, change_stroke=False)
        return True

    def can_long_castling(self, row, col, new_row, new_col):
        if not self.correct_coordinates(row, col - 4):
            return False

        king, rook = self.board[row][col], self.board[row][col - 4]
        if not (isinstance(king, King) and isinstance(rook, Rook) and
                king.can_castle and rook.can_castle and
                row == new_row and col - 2 == new_col and
                all(map(lambda x: self.board[row][col + x] is None, (-1, -2, -3)))):
            return False

        self.move_piece(rook, row, col - 4, new_row, col - 1, change_stroke=False)
        return True

    def move_piece(self, piece, row, col, row1, col1, change_stroke=True):
        self.board[row][col] = None
        if self.chess_check(piece):
            self.board[row][col] = piece
            return False

        self.board[row1][col1] = piece
        piece.set_position(row1, col1)  # можно вставить функцию для уязвимого хвоста пешки во время большого хода
        if change_stroke:
            self.color = not self.color
        return True

    def is_under_attack(self, figure):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] is not None:
                    if self.board[i][j].color != figure.color:
                        if self.board[i][j].can_move(self.board, figure.row, figure.col):
                            return True

    def get_figure(self, cls, color=None):  # требуется рефакторинг и возможно оптимизация
        rez = []
        for i in self.board:
            for j in i:
                if type(j) == cls:
                    if color is None:
                        rez.append(j)
                    elif j is not None and color == j.color:
                        rez.append(j)
        return rez

    def is_current_player(self, other_color):
        return self.color == other_color

    def get_cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.board[row][col]
        if piece is None:
            return '  '
        c = 'w' if piece.get_color() == WHITE else 'b'
        return c + piece.char()
