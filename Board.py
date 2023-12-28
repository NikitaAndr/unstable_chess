"""Модуль шахматной доски

Импорты модулей проекта:
const: WHITE, BLACK - импорты цветов фигур
Figure: Bishop, King, Knight, Pawn, Figure, Queen, Rook - все возможные фигуры
Figure: copy - функция для копирования фигур
convert: chess_math, math_chess_cor - функции перевода из математической в шахматную и наоборот
Errors: IncorrectCoordinates - ошибка, сообщающая, что пользователь выдал не верные координаты

try_error - Декоратор обрабатывающий ошибки выдаваемые классом доски в функции make_move

Board - сам класс доски"""

from const import WHITE, BLACK
from Figure import Bishop, King, Knight, Pawn, Figure, Queen, Rook, copy
from convert import chess_math, math_chess_cor
from Errors import IncorrectCoordinates


def try_error(make_move):
    def new_make_move(*args, **kwargs) -> tuple[bool, str]:
        try:
            make_move(*args, **kwargs)
            return True, ''
        except IncorrectCoordinates as error:
            print(str(error.msg))
            return False, str(error.msg)

    return new_make_move


class Board:
    """Класс доски, на которой происходит действие игры.

    Запуск игры происходит через главную функцию make_moves.
    В make_moves может вызываться ошибка IncorrectCoordinates,
     которая сигнализирует о некорректности координат (см класс ошибки)"""

    def __init__(self, count_col=8, count_row=8, arrange_figure=True):
        """Инициализация полей.

        Публичные поля:
        count_col, count_row - количество колонок и строк доски,
        color - цвет, за который можно сходить,
        mate - флаг мата,
        board - сама доска.

        Приватные поля:
        _ald_board - доска до совершения хода, обновляется каждый ход в make_move."""

        self.count_col = count_col
        self.count_row = count_row
        self.color = WHITE
        self.mate = False
        self.stalemate = False

        self.board = [[None] * count_col for _ in range(count_row)]
        if arrange_figure:
            self.arrange_pawns()
            self.arrange_senior_figures()

        self._ald_board = self.board

    def __repr__(self):
        """Вывод доски в шахматном представлении с названиями полей."""
        stra = '     +----+----+----+----+----+----+----+----+ \n'
        for row in range(self.count_row - 1, -1, -1):
            stra += f'  {row + 1}  '
            for col in range(self.count_col):
                stra += f'| {"  " if (figure := self.board[row][col]) is None else figure} '
            stra += '|\n     +----+----+----+----+----+----+----+----+ \n'
        stra += '        ' + '    '.join([math_chess_cor(col) for col in range(self.count_col)])

        return stra

    def arrange_pawns(self):
        """Расставь пешки."""
        for i in range(8):
            self.board[1][i] = Pawn(1, i, WHITE)
            self.board[6][i] = Pawn(6, i, BLACK)

    def arrange_senior_figures(self):
        """Расставь старшие фигуры."""
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
    def correct_coordinates(row: int, col: int) -> bool:
        """Функция проверяет, что координаты (row, col) лежат
        внутри доски."""
        return 0 <= row < 8 and 0 <= col < 8

    def make_moves(self, stra: str | tuple | list) -> None:
        """Проиграть партию до определённого момента."""
        for i in stra.split():
            if '.' not in i:  # тк иначе i[-1] - это обозначение хода по порядку
                self.make_move(i)

    @try_error
    def make_move(self, stra: str | tuple | list) -> None:
        """Сделать ход по координатам stra

        Формат кода:
        str: координаты поля в формате PGN в полной форме, например: e2-e4,
        tuple или list: координаты в формате <row: int><col: int>."""

        self._ald_board = self.board
        cor, new_cor, transformation_figure = chess_math(stra) if (type(stra) is str) else stra
        self._check_cords(cor, new_cor)
        self._check_piece(cor, new_cor)
        self._move_piece(*cor, *new_cor)
        self._chess_check()
        self._update(transformation_figure=transformation_figure)

    def is_under_attack(self, figure: Figure):
        """Проверь, находится ли поле под атакой."""
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if (self.board[i][j] is not None
                        and self.board[i][j].color != figure.color
                        and self.board[i][j].can_move(self.board, figure.row, figure.col)):
                    return True
        return False

    def is_current_player(self, other_color: bool) -> bool:
        """Проверь, является ли цвет, которые был передан (other_color) цветом игрока."""
        return self.color == other_color

    def get_figure(self, cls=None, color=None) -> list:  # возможна оптимизация
        """Выдай фигуру класса cls и цвета color, если они не указаны, то выдаются все возможные."""
        rez = []
        for i in self.board:
            for j in i:
                if (cls is None) or isinstance(j, cls):
                    if (color is None) or (j is not None and color == j.color):
                        rez.append(j)
        return rez

    @staticmethod
    def _read_move(cor, new_cor, transformation_figure):
        with open('last_consignment', mode='a') as file:
            file.write(f'{cor} {new_cor} {transformation_figure} \n')

    def _check_cords(self, cor: tuple[int, int], new_cor: tuple[int, int]) -> None:
        """Проверка координат на корректность."""
        if cor == new_cor:
            raise IncorrectCoordinates('Нельзя просто поднять фигуру и поставить её на тоже самое место')
        if not self.correct_coordinates(*cor):
            raise IncorrectCoordinates('Координаты фигуры за пределами доски')
        if not self.correct_coordinates(*new_cor):
            raise IncorrectCoordinates('Нельзя ставить фигуру за пределы доски')

    def _check_piece(self, cor: tuple[int, int], new_cor: tuple[int, int]) -> None:
        """Проверка, может ли фигура по выбранным координатам сходить на новые."""
        if (piece := self.board[cor[0]][cor[1]]) is None:
            raise IncorrectCoordinates('Вы берёте не существующую фигуру')
        if not self.is_current_player(piece.get_color()):
            raise IncorrectCoordinates('Вы не можете взять фигуру другого игрока')
        if not (piece.can_move(self.board, *new_cor) or
                self._can_short_castling(*cor, *new_cor) or
                self._can_long_castling(*cor, *new_cor)):
            raise IncorrectCoordinates('Фигура не может сходить на это поле')

    def _can_short_castling(self, row: int, col: int, new_row: int, new_col: int) -> bool:
        """Проверь, может ли игрок совершить длинную рокировку. И если да, то двинь ладью на новое место."""
        if not self.correct_coordinates(row, col + 3):
            return False

        king, rook = self.board[row][col], self.board[row][col + 3]
        if not (isinstance(king, King) and isinstance(rook, Rook) and
                king.can_castle and rook.can_castle and
                row == new_row and col + 2 == new_col and
                self.board[row][col + 1] is None and self.board[row][col + 2] is None):
            return False

        self._move_piece(row, col + 3, new_row, col + 1)
        return True

    def _can_long_castling(self, row: int, col: int, new_row: int, new_col: int):
        """Проверь, может ли игрок совершить длинную рокировку. И если да, то двинь ладью на новое место."""
        if not self.correct_coordinates(row, col - 4):
            return False

        king, rook = self.board[row][col], self.board[row][col - 4]
        if not (isinstance(king, King) and isinstance(rook, Rook) and
                king.can_castle and rook.can_castle and
                row == new_row and col - 2 == new_col and
                all(map(lambda x: self.board[row][col + x] is None, (-1, -2, -3)))):
            return False

        self._move_piece(row, col - 4, new_row, col - 1)
        return True

    def _move_piece(self, row: int, col: int, row1: int, col1: int):
        """Двинь фигуру с координат row, col на row1, col1 БЕЗ ПРОВЕРОК."""
        piece = self.board[row][col]
        self.board[row][col] = None
        self.board[row1][col1] = piece
        piece.set_position(row1, col1)
        # можно вставить функцию для уязвимого хвоста пешки во время большого хода

    def _chess_check(self):
        """Проверь шах, если да, то верни доску в прежнее состояние."""
        if self.is_under_attack(self.get_figure(King, self.color)[0]):
            self.board = self._ald_board
            raise IncorrectCoordinates('Шах')

    def _update(self, change_stroke=True, transformation_figure: Figure | None = Queen):
        """Обнови фигуры после хода

        change_stroke - требуется ли передача хода
        transformation_figure - в какую фигуру превратить пешки"""

        if change_stroke:
            self.color = not self.color
        self._transform_pawn(transformation_figure)
        if len(self.get_figure()) == 2:
            self.stalemate = True

    def _transform_pawn(self, transformation_figure: Figure | None = Queen):
        """Преврати все пешки на последних линиях в фигуру (transformation_figure)."""
        transformation_figure = transformation_figure if transformation_figure is not None else Queen
        for i in (0, -1):
            for j in range(len(self.board[i])):
                if isinstance(self.board[i][j], Pawn):
                    self.board[i][j] = copy(self.board[i][j], transformation_figure)
