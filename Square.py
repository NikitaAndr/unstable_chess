class OrdinarySquare:
    def __init__(self, square_size=100):
        self.size_x = square_size
        self.size_y = square_size
        self.size = square_size, square_size

    def set_size(self, new_size_x, new_size_y=None):
        self.size_x = new_size_x
        self.size_y = new_size_x if new_size_y is None else new_size_y

        self.size = self.size_x, self.size_y


OrdinarySquare()
