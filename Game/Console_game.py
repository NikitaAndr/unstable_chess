"""Модуль с классом ConsoleGame, обеспечивающим игру в консоли

Импорты модулей проекта:
Game - класс-родитель, от которого наследует основной класс своё поведение.
check_end_game - декоратор, необходимый класса-родителя.

const.WHITE - постоянная, отображающая цвет белых,
используется в init_invitation, для генерации более красивого приглашения
"""


from Game.Game import Game, check_end_game
from const import WHITE


class ConsoleGame(Game):
    """Класс отображающий доску в консоли

    Является наследником класса Game,
    переопределяет start для игры в консоли"""

    @check_end_game
    def start(self) -> None:
        """Запусти игру"""
        self.init_invitation()
        if (command := input()) == 'exit':  # -h, -h-a
            self.game_over()
        elif command.split()[0] in ('move', 'm'):
            self.move(command.split()[1])

    def init_invitation(self) -> None:
        """Выведи приглашение сделать ход"""
        print(self._board)
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        print('Ход белых:' if self._board.is_current_player(WHITE) else 'Ход черных:')

    def move(self, cor: str) -> None:
        """Обработка хода"""
        rez, error = self._board.make_move(cor)
        print('Ход успешен' if rez else error)
