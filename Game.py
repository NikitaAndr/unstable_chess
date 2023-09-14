import convert
from Board import Board
from const import *
import pygame


class Game:
    def __init__(self):
        self.board = Board()
        # Итальянка
        # self.board.make_move('e2 - e4')
        # self.board.make_move('e7 - e5')
        # self.board.make_move('g1 - f3')
        # self.board.make_move('b8 - c6')
        # self.board.make_move('f1 - b5')

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

        self.selected_square = (-1, -1)

    def start(self):
        running = True
        while (not self.board.mate) and running:
            running = self.event_handling()
            self.render()
            pygame.display.flip()
            clock.tick(FPS)

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = convert.visual_chess(pygame.mouse.get_pos())
                if self.selected_square == (-1, -1):
                    self.selected_square = pos
                elif not self.board.make_move((self.selected_square, pos)):
                    self.selected_square = (-1, -1)

        return True

    def render(self):
        for i in range(8):
            for j in range(8):
                self.draw_square(i, j)
                self.draw_figure(i, j)

    def draw_square(self, i, j):
        color = [200, 200, 200] if (i % 2 == j % 2) else [100, 100, 100]
        if self.selected_square == convert.little_visual_chess((i, j)):
            color[2] += 50
        self.screen.fill(color, (*convert.little_visual_visual((i, j)), 200, 200))

    def draw_figure(self, i, j):
        cor = convert.little_visual_chess((i, j))
        if (figure := self.board.field[cor[0]][cor[1]]) is not None:  # сделать обращение по индексу к доске
            self.screen.blit(figure.get_img(), convert.little_visual_visual((i, j)))
