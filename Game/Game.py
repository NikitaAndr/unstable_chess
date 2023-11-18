"""Модуль с классом-родителем Game.

Импорты стандартных библиотек:
json - используется в Game.load_gambit для загрузки из файла ../gambits.json.

Импорты модулей проекта:
Board - доска, которую отображает класс Game.

Класс Game - класс-родитель отображающих доску.

Декоратор check_end_game - обеспечивает существование игрового цикла.
"""

import json
from Board import Board


def check_end_game(start):
    """Запусти цикл игры.

    Декоратор, запускающий бесконечный цикл игры для классов-наследников Game.
    Цикл заканчивается если поставлен мат (self._board.mate) или игрок сам окончил игру (self._running)."""

    def start_new(self, *args, **kwargs):
        while not self._board.mate and self._running:
            start(self, *args, *kwargs)

    return start_new


class Game:
    """Класс-родитель отображающих доску."""

    def __init__(self) -> None:
        """Инициализирует поля.

        приватные-наследуемые:
        _board - доска которую нужно отобразить.
        _running - условие отображения игры. Изменяется в game_over."""

        self._board = Board()
        self._running = True

    def load_gambit(self, gambit='') -> None:
        """Расставь гамбит (gambit) на доске."""
        with open('./gambits.json') as js:
            gambit = json.load(js).get(gambit)
            self._board.make_moves(gambit if gambit is not None else '')

    def game_over(self) -> None:
        """Останови игру. Метод инкапсуляции running."""
        self._running = False

    @check_end_game
    def start(self) -> None:
        """Запусти игру."""
