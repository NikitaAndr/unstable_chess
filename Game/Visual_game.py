"""Модуль с классом VisualGame, обеспечивающим игру в базовом интерфейсе

Импорты сторонних модулей:
pygame - библиотека с инструментами для отображения доски.


Импорты модулей проекта:
Game - класс-родитель, от которого наследует основной класс своё поведение,
check_end_game - декоратор, необходимый класса-родителя;

size - размеры экрана,
clock - постоянная для измерения времени,
FPS - количество кадров в секунду."""

import pygame

from Game.Game import Game, check_end_game
from const import size, clock, FPS
import convert


class VisualGame(Game):
    """Интерфейс доски для разработчика или упрощённая версия для пользователя (PyGame)."""

    def __init__(self):
        """Расширяет поля класса-родителя.

        приватные:
        _screen - основной интерфейс взаимодействия с пользователем,
        _selected_square - координаты поля, которые выбрал пользователь в event_handling_mouse."""
        super(VisualGame, self).__init__()
        self._screen = pygame.display.set_mode(size)

        self._selected_square = (-1, -1)

    @check_end_game
    def start(self) -> None:
        """Запусти игру."""
        self.event_handling()
        self.render()
        pygame.display.flip()
        clock.tick(FPS)

    def event_handling(self) -> None:
        """Обработай события."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.event_handling_mouse()

    def event_handling_mouse(self) -> None:
        """Обработай события, связанные с нажатием левой кнопки мыши."""
        pos = convert.visual_chess(pygame.mouse.get_pos())
        if self._selected_square == (-1, -1):
            self._selected_square = pos
        elif not self._board.make_move((self._selected_square, pos, None))[0]:
            self._selected_square = (-1, -1)

    def render(self) -> None:
        """Нарисуй доску."""
        # могут возникнуть БОЛЬШИЕ проблемы при переходе на доску с переменным количеством строк и столбцов
        for i in range(8):
            for j in range(8):
                self.draw_square(i, j)
                self.draw_figure(i, j)

    def draw_square(self, i: int, j: int) -> None:
        """Нарисуй квадрат доски по координатам (от 1 до 8) i-той строки, j-того столбца."""
        # хорошо б сделать проверку на дурака
        color = [200, 200, 200] if (i % 2 == j % 2) else [100, 100, 100]
        if self._selected_square == convert.little_visual_chess((i, j)):
            color[2] += 50
        self._screen.fill(color, (*convert.little_visual_visual((i, j)), 200, 200))

    def draw_figure(self, i: int, j: int) -> None:
        """Нарисуй фигуру стоящую по координатам (от 1 до 8) i-той строки, j-того столбца."""
        # хорошо б сделать проверку на дурака
        i_chess, j_chess = convert.little_visual_chess((i, j))
        if (figure := self._board.board[i_chess][j_chess]) is not None:
            self._screen.blit(figure.get_img(), convert.little_visual_visual((i, j)))
