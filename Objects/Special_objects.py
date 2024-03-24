import pygame
from const import reference_square
from Objects.class_hess_object import ChessObject


class SpecialObjects(ChessObject):
    ...


class FakeField(SpecialObjects):
    def __str__(self):
        return '  '


class Pit(SpecialObjects):
    def __init__(self, row, col):
        super(Pit, self).__init__(row, col)
        self.is_eaten_figure = False

    @staticmethod
    def char() -> str:
        """Дай буквенное представление."""
        return f'⏹'

    @staticmethod
    def get_img() -> pygame.Surface | pygame.SurfaceType:
        """Дай представление в виде изображения."""
        q = pygame.surface.Surface(reference_square.size)
        q.fill((0, 0, 0))
        return q
