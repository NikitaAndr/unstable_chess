from Board import Board
from const import *
import pygame


class Game:
    def __init__(self):
        self.board = Board()
        # Итальянка
        self.board.make_move('e2 - e4')
        self.board.make_move('e7 - e5')
        self.board.make_move('g1 - f3')
        self.board.make_move('b8 - c6')
        self.board.make_move('f1 - b5')

    def start(self): ...

    def init_invitation(self): ...

    def move(self, cor): ...


class ConsoleGame(Game):
    def start(self):
        while True:
            self.init_invitation()
            if (command := input()) == 'exit':
                break
            elif command.split()[0] in ('move', 'm'):
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


class VisualGame(Game):
    def __init__(self):
        super(VisualGame, self).__init__()
        self.screen = pygame.display.set_mode(size)
        self.left = 0
        self.top = 0
        self.cell_size = 100

    def start(self):
        running = True
        while (not self.board.mate) and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.render()
            pygame.display.flip()
            clock.tick(FPS)

    def render(self):
        for i in range(8):
            for j in range(8):
                if self.board.field[i][j] is not None:
                    self.screen.blit(self.board.field[i][j].get_img(),
                                     (self.left + self.cell_size * j,
                                      self.top + self.cell_size * i))
