import convert
from Board import Board
from const import *
import pygame
import json


def check_end_game(start):
    """Запуск цикла игры"""
    def start_new(self, *args, **kwargs):
        while not self._board.mate and self._running:
            start(self, *args, *kwargs)

    return start_new


class Game:
    """Класс-родитель отображающих доску"""
    def __init__(self) -> None:
        self._board = Board()
        self._running = True

    def load_gambit(self, gambit='') -> None:
        """
        Расставляет гамбит под именем gambit на доске
        Если gambit не передаётся или передаётся гамбит, которого нет в базе,
        То не реагирует
        """

        with open('gambits.json') as js:
            gambit = json.load(js).get(gambit)
            self._board.make_moves(gambit if gambit is not None else '')

    def game_over(self) -> None:
        """Метод для остановки игры. Метод инкапсуляции running"""
        self._running = False

    def start(self) -> None: ...


class ConsoleGame(Game):
    """Класс отображающий доску в консоли"""
    @check_end_game
    def start(self) -> None:
        """Запуск игры"""
        self.init_invitation()
        if (command := input()) == 'exit':
            self.game_over()
        elif command.split()[0] in ('move', 'm'):
            self.move(command.split()[1])

    def init_invitation(self) -> None:
        """Вывод приглашения сделать ход"""
        print(self._board)
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        print('Ход белых:' if self._board.is_current_player(WHITE) else 'Ход черных:')

    def move(self, cor: str) -> None:
        """Метод обработки хода"""
        print('Ход успешен' if self._board.make_move(cor)
              else 'Координаты некорректны! Попробуйте другой ход!')


class VisualGame(Game):
    def __init__(self):
        super(VisualGame, self).__init__()
        self._screen = pygame.display.set_mode(size)

        self._selected_square = (-1, -1)

    @check_end_game
    def start(self) -> None:
        """Запуск игры"""
        self.event_handling()
        self.render()
        pygame.display.flip()
        clock.tick(FPS)

    def event_handling(self) -> None:
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.event_handling_mouse()

    def event_handling_mouse(self) -> None:
        """Обработка событий, связанных с нажатием левой кнопки мыши"""
        pos = convert.visual_chess(pygame.mouse.get_pos())
        if self._selected_square == (-1, -1):
            self._selected_square = pos
        elif not self._board.make_move((self._selected_square, pos, None)):
            self._selected_square = (-1, -1)

    def render(self) -> None:
        """Нарисовать доску"""
        # могут возникнуть БОЛЬШИЕ проблемы при переходе на доску с переменным количеством строк и столбцов
        for i in range(8):
            for j in range(8):
                self.draw_square(i, j)
                self.draw_figure(i, j)

    def draw_square(self, i: int, j: int) -> None:
        """Нарисовать квадратик доски по координатам (от 1 до 8) i-той строки, j-того столбца"""
        # хорошо б сделать проверку на дурака
        color = [200, 200, 200] if (i % 2 == j % 2) else [100, 100, 100]
        if self._selected_square == convert.little_visual_chess((i, j)):
            color[2] += 50
        self._screen.fill(color, (*convert.little_visual_visual((i, j)), 200, 200))

    def draw_figure(self, i: int, j: int) -> None:
        """Нарисовать фигуру стоящую по координатам (от 1 до 8) i-той строки, j-того столбца"""
        # хорошо б сделать проверку на дурака
        i_chess, j_chess = convert.little_visual_chess((i, j))
        if (figure := self._board.board[i_chess][j_chess]) is not None:
            self._screen.blit(figure.get_img(), convert.little_visual_visual((i, j)))
