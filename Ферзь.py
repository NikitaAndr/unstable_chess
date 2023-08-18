class Queen:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row1, col1):
        if (self.col - self.row == col1 - row1 or self.col + self.row == col1 + row1
            or self.row == row or self.col == col) and (0 <= row1 <= 7) \
                and (0 <= col1 <= 7):
            return True
        return False

    def set_position(self, row, col):
        self.row = row
        self.col = col
        # ошибка может быть

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'


WHITE=1
BLACK=2

row0 = 0
col0 = 3
queen = Queen(row0, col0, WHITE)

print('white' if queen.get_color() == WHITE else 'black')
for row in range(7, -1, -1):
    for col in range(8):
        if row == row0 and col == col0:
            print(queen.char(), end='')
        elif queen.can_move(row, col):
            print('x', end='')
        else:
            print('-', end='')
    print()
