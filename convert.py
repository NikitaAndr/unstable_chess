from const import *


def chess_math(stra: str):
    print(stra)
    cor, new_cor = stra.replace(' ', '').split('-')
    col = ord(cor[0]) - ord('a')
    col1 = ord(new_cor[0]) - ord('a')
    row = int(cor[1]) - 1
    row1 = int(new_cor[1]) - 1
    return (row, col), (row1, col1)


def visual_chess(cor):
    return 7 - (cor[1] - left) // cell_size, \
           (cor[0] - top) // cell_size


def chess_visual(cor):
    return left + cell_size * cor[1], \
           top + cell_size * cor[0]


def visual_little_visual(cor):
    return (cor[0] - left) // cell_size, \
           (cor[1] - top) // cell_size


def chess_little_visual(cor):
    return 7 - cor[1], cor[0]


def little_visual_chess(cor):
    return 7 - cor[1], cor[0]


def little_visual_visual(cor):
    return cor[0] * cell_size + top, cor[1] * cell_size + left
