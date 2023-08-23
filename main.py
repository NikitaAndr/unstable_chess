from Board import Board
from const import *


def main():
    board = Board()
    # Итальянка
    board.make_move('e2 - e4')
    board.make_move('e7 - e5')
    board.make_move('g1 - f3')
    board.make_move('b8 - c6')
    board.make_move('f1 - b5')
    while True:
        print(board)
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        if board.is_current_player(WHITE):
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()
        if command == 'exit':
            break
        move_type, move_cor = command.split()
        if board.move_piece(*board.convert_chess_math(move_cor)):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


if __name__ == '__main__':
    main()
