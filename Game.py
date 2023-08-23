from Board import Board
from const import *


class Game:
    def __init__(self):
        self.board = Board()
        # Итальянка
        self.board.make_move('e2 - e4')
        self.board.make_move('e7 - e5')
        self.board.make_move('g1 - f3')
        self.board.make_move('b8 - c6')
        self.board.make_move('f1 - b5')

    def start(self):
        while True:
            self.init_invitation()
            if (command := input()) == 'exit':
                break
            if command.split()[0] in ('move', 'm'):
                self.move(command.split()[1])

    def init_invitation(self):
        print(self.board)
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        print('Ход белых:' if self.board.is_current_player(WHITE) else 'Ход черных:')

    def move(self, cor):
        if self.board.make_move(cor):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')
