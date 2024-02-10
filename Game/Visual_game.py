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
from const import size, reference_square, clock, FPS, instability
from random import choice
import convert


class VisualGame(Game):
    """Интерфейс доски для разработчика или упрощённая версия для пользователя (PyGame)."""

    def __init__(self):
        """Расширяет поля класса-родителя.

        приватные:
        _screen - основной интерфейс взаимодействия с пользователем,
        _selected_square - координаты поля, которые выбрал пользователь в event_handling_mouse."""
        super(VisualGame, self).__init__()
        self._screen = pygame.display.set_mode(size, pygame.RESIZABLE)

        self._selected_square = (-1, -1)

        self.sp_unstable_event = [
            self._board.add_right_col,
            self._board.add_left_col,
            self._board.add_top_row,
            self._board.add_down_row,
            self._board.subtract_down_row,
            self._board.subtract_top_row,
            self._board.subtract_right_col,
            self._board.subtract_left_col,
        ]

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
        pos = convert.visual_chess(pygame.mouse.get_pos(), self._board.count_row)
        if self._selected_square == (-1, -1):
            self._selected_square = pos
        else:
            self._board.make_move((self._selected_square, pos, None))
            self.unstable_event_handling()
            self._selected_square = (-1, -1)

    def unstable_event_handling(self):
        if self._board.count_make_move % instability == 0:
            self.start_unstable_event()

        reference_square.set_size(
            min(self._screen.get_size()) //
            max(self._board.count_col, self._board.count_row))

    def start_unstable_event(self):
        choice(self.sp_unstable_event)()

    def render(self) -> None:
        """Нарисуй доску."""
        self._screen.fill((0, 0, 0))
        for i in range(self._board.count_col):
            for j in range(self._board.count_row):
                self.draw_square(i, j)
                self.draw_figure(i, j)

    def draw_square(self, i: int, j: int) -> None:
        """Нарисуй квадрат доски по координатам (от 1 до 8) i-той строки, j-того столбца."""
        # хорошо б сделать проверку на дурака
        color = [200, 200, 200] if (i % 2 == j % 2) else [100, 100, 100]
        if self._selected_square == convert.little_visual_chess((i, j), self._board.count_row):
            color[2] += 50
        self._screen.fill(color, (*convert.little_visual_visual((i, j)), *reference_square.size))

    def draw_figure(self, i: int, j: int) -> None:
        """Нарисуй фигуру стоящую по координатам (от 1 до 8) i-той строки, j-того столбца."""
        # хорошо б сделать проверку на дурака
        i_chess, j_chess = convert.little_visual_chess((i, j), self._board.count_row)
        if (figure := self._board.board[i_chess][j_chess]) is not None:
            self._screen.blit(figure.get_img(), convert.little_visual_visual((i, j)))  # изменить размеры клетки
