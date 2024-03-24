# в будущем создать класс клетки (поля) для Board и переделать всю конвертацию туда
# is None переписать на piece.is_empty и возможно разделить логику на "в доске" и "вне доски"
from Objects.Figure import *
from const import *

sl = {'P': Pawn,
      'Q': Queen,
      'K': King,
      'N': Knight,
      'B': Bishop,
      'R': Rook,
      }


def chess_math(stra: str):
    cor, new_cor = stra.replace(' ', '').replace('—', '-').replace('x', '-').split('-')

    transformation_figure = None
    if '=' in new_cor and len(new_cor) > 3:
        transformation_figure = sl[new_cor[4]]

    return chess_math_cor(cor), chess_math_cor(new_cor), transformation_figure


def chess_math_cor(cor):
    cor = cor[1:] if cor.istitle() else cor
    col = ord(cor[0]) - ord('a')
    row = int(cor[1:]) - 1
    return row, col


def math_chess_cor(cor: int):
    return chr(cor + ord('a'))


def visual_chess(cor, count_col_chess):
    return (count_col_chess - (cor[1] // reference_square.size_x) - 1,
            (cor[0] // reference_square.size_y))


def little_visual_chess(cor, count_col_chess):
    return count_col_chess - cor[1] - 1, cor[0]


def little_visual_visual(cor):
    return cor[0] * reference_square.size_y,\
           cor[1] * reference_square.size_x
