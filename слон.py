class Bishop:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row1, col1):
        if (self.col - self.row == col1 - row1 or self.col + self.row == col1 + row1) \
                and (0 <= row1 <= 7) and (0 <= col1 <= 7):
            return True
        return False

    def set_position(self, row, col):
        self.row = row
        self.col = col
        # ошибка может быть

    def get_color(self):
        return self.color

    def char(self):
        return 'B'
