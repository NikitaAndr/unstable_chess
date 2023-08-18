WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника (х\з пригодится ли)
def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


# Распечатать доску в текстовом виде
def print_board(board):
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


# создание доски / прилюдия
def start():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


# конь
class Knight:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row1, col1):
        if ((self.row + 1 == row1 and self.col + 2 == col1)
            or (self.row - 1 == row1 and self.col + 2 == col1)
            or (self.row + 1 == row1 and self.col - 2 == col1)
            or (self.row - 1 == row1 and self.col - 2 == col1)
            or (self.row + 2 == row1 and self.col + 1 == col1)
            or (self.row - 2 == row1 and self.col + 1 == col1)
            or (self.row + 2 == row1 and self.col - 1 == col1)
            or (self.row - 2 == row1 and self.col - 1 == col1)) \
                and (0 <= row1 <= 7) and (0 <= col1 <= 7):
            return True
        else:
            return False

    def set_position(self, row, col):
        if self.can_move(row, col):
            self.row = row
            self.col = col
        # ошибка может быть

    def get_color(self):
        return self.color

    def char(self):
        return 'N'


# пешка
class Pawn:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'P'

    def get_color(self):
        return self.color

    def can_move(self, row, col):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if self.col != col:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if self.row + direction == row:
            return True

        # ход на 2 клетки из начального положения
        if self.row == start_row and self.row + 2 * direction == row:
            return True

        return False


# ладья
class Rook(Knight):
    def char(self):
        return 'R'

    def can_move(self, row, col):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if self.row != row and self.col != col:
            return False

        return True


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


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

        if not correct_coords(row, col) or not correct_coords(row1, col1):
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
        # спрашиваем у фигуры может ли она походить
        # я писал
        # if [None] * 7 not in self.field[row]:
        #     q = [k for i in enumerate(field[row][:self.col]) if type(i) != Rook or i != [None]]
        if type(piece) == Rook:
            if [None] * 7 not in self.field[row]:
                ogr_s_leva = max([*[k for k, i in enumerate(self.field[row][:col])
                                    if type(i) != Rook or i != [None]], -1])
                ogr_s_prava = min(
                    [*[k + 1 for k, i in enumerate(self.field[row][col + 1:])
                       if type(i) != Rook or i != [None]], 9])
                if not ogr_s_leva <= col1 <= ogr_s_prava:
                    return False
            sp_vertik = [self.field[i][0] for i in range(8)]
            if [None] * 7 not in sp_vertik:
                ogr_s_verx = min(
                    [*[k + 1 for k, i in enumerate(sp_vertik[row + 1:])
                       if type(i) != Rook or i != [None]], 9])
                ogr_s_niz = max([*[k for k, i in enumerate(sp_vertik[:row])
                                   if type(i) != Rook or i != [None]], -1])
                if not ogr_s_niz <= row1 <= ogr_s_verx:
                    return False
        if type(piece) == Bishop:
            sp_vertik = []
            sp_vertik1 = []
            for i in range(8):
                for j in range(8):
                    if piece.col - piece.row == j - i:
                        sp_vertik.append(self.field[i][j])
                    if piece.col + piece.row == j + i:
                        sp_vertik1.append(self.field[i][j])
            if piece.col - piece.row == col1 - row1:
                if not can_xod_Bishop(sp_vertik, row, row1):
                    return False
            if piece.col + piece.row == col1 + row1:
                if not can_xod_Bishop(sp_vertik1, row, row1):
                    return False
        if type(piece) == Queen:
            if [None] * 7 not in self.field[row]:
                ogr_s_leva = max(
                    [*[k for k, i in enumerate(self.field[row][:col])
                       if type(i) != Queen or i != [None]], -1])
                ogr_s_prava = min(
                    [*[k + 1 for k, i in enumerate(self.field[row][col + 1:])
                       if type(i) != Queen or i != [None]], 9])
                if not ogr_s_leva <= col1 <= ogr_s_prava:
                    return False
            sp_vertik = [self.field[i][0] for i in range(8)]
            if [None] * 7 not in sp_vertik:
                ogr_s_verx = min(
                    [*[k + 1 for k, i in enumerate(sp_vertik[row + 1:])
                       if type(i) != Queen or i != [None]], 9])
                ogr_s_niz = max([*[k for k, i in enumerate(sp_vertik[:row])
                                   if type(i) != Queen or i != [None]], -1])
                if not ogr_s_niz <= row1 <= ogr_s_verx:
                    return False
            sp_vertik = []
            sp_vertik1 = []
            for i in range(8):
                for j in range(8):
                    if piece.col - piece.row == j - i:
                        sp_vertik.append(self.field[i][j])
                    if piece.col + piece.row == j + i:
                        sp_vertik1.append(self.field[i][j])
            if piece.col - piece.row == col1 - row1:
                if not can_xod_Bishop(sp_vertik, row, row1):
                    return False
            if piece.col + piece.row == col1 + row1:
                if not can_xod_Bishop(sp_vertik1, row, row1):
                    return False
        if type(piece) == King:
            if self.field[row1][col1] != [None]:
                return False

        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        self.color = opponent(self.color)
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


# слон
class Bishop(Knight):
    def can_move(self, row1, col1):
        if (self.col - self.row == col1 - row1 or self.col + self.row == col1 + row1) \
                and (0 <= row1 <= 7) and (0 <= col1 <= 7):
            return True
        return False

    def char(self):
        return 'B'


# ферзь
class Queen(Knight):
    def can_move(self, row1, col1):
        if (self.col - self.row == col1 - row1 or self.col + self.row == col1 + row1
            or self.row == row1 or self.col == col1) and (0 <= row1 <= 7) \
                and (0 <= col1 <= 7):
            return True
        return False

    def char(self):
        return 'Q'


# король
class King(Knight):
    def can_move(self, row1, col1):
        if (0 <= row1 <= 7) and (0 <= col1 <= 7):
            return True
        return False

    def char(self):
        return 'K'


board = Board()

board.field = [([None] * 8) for i in range(8)]
board.field[4][7] = Queen(4, 7, BLACK)
board.field[3][2] = Bishop(3, 2, BLACK)
board.field[5][1] = Rook(5, 1, BLACK)
board.field[1][6] = Knight(1, 6, WHITE)
board.field[1][2] = Bishop(1, 2, WHITE)
w_coords = ((1, 6), (1, 2))
b_coords = ((4, 7), (3, 2), (5, 1))


board = Board()

board.field = [([None] * 8) for i in range(8)]
board.field[4][7] = Queen(4, 7, BLACK)
board.field[3][2] = Bishop(3, 2, BLACK)
board.field[5][1] = Rook(5, 1, BLACK)
board.field[1][6] = Knight(1, 6, WHITE)
board.field[1][2] = Bishop(1, 2, WHITE)
w_coords = ((1, 6), (1, 2))
b_coords = ((4, 7), (3, 2), (5, 1))

print('White:')
for row in range(7, -1, -1):
    for col in range(8):
        if (row, col) in w_coords:
            print('W', end='')
        elif board.is_under_attack(row, col, WHITE):
            print('x', end='')
        else:
            print('-', end='')
    print()
print()

print('Black:')
for row in range(7, -1, -1):
    for col in range(8):
        if (row, col) in b_coords:
            print('B', end='')
        elif board.is_under_attack(row, col, BLACK):
            print('x', end='')
        else:
            print('-', end='')
    print()