class ChessObject:
    """Класс-родитель (интерфейс, абстрактный класс) фигур."""

    def __init__(self, row: int, col: int) -> None:
        """Инициализация полей.

        Публичные поля:
        row - строка, где сейчас стоит фигура
        col - колонка, где сейчас стоит фигура
        is_eaten_figure - может ли быть съеден объект"""
        self.row = row
        self.col = col
        self.is_eaten_figure = True

    def __str__(self) -> str:
        return 'n' + self.char()

    def __repr__(self) -> str:
        return f'{self.char()}-{self.row}-{self.col}-n'

    def __eq__(self, other) -> bool:
        return (type(self) == type(other) and
                self.col == other.col and
                self.row == other.row)

    def __ne__(self, other) -> bool:
        return not (type(self) == type(other) and
                    self.col == other.col and
                    self.row == other.row)

    @staticmethod
    def char() -> str:
        """Дай буквенное представление."""
        return "n"
