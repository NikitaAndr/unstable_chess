import unittest
from parameterized import parameterized

from Objects.Board import Board
from Objects.Figure import *


class TestBoard(unittest.TestCase):
    def test_arrange_pawns(self):
        board = Board(arrange_figure=False)
        board.arrange_pawns()
        self.assertTrue(all(map(lambda x: isinstance(x, Pawn), board.board[1] + board.board[-2])))

    def test_arrange_senior_figures(self):
        ...

    def test_correct_coordinates_true(self):
        board = Board()
        for i in range(board.count_col):
            for j in range(board.count_row):
                self.assertTrue(board.correct_coordinates(i, j))
        self.assertFalse(board.correct_coordinates(board.count_col + 1, board.count_row + 1))
        self.assertFalse(board.correct_coordinates(-1, -1))

    @parameterized.expand([
        ('e2-e4', ''),
        ('b1-c3', ''),
        (((1, 4), (3, 4), None), ''),
        ('e2-e6', 'Фигура не может сходить на это поле'),
        ('e3-e2', 'Вы берёте не существующую фигуру'),
        ('e2-e2', 'Нельзя просто поднять фигуру и поставить её на тоже самое место'),
        ('e17-e4', 'Координаты фигуры за пределами доски'),
        ('e2-e17', 'Нельзя ставить фигуру за пределы доски'),
        ('e7-e5', 'Вы не можете взять фигуру другого игрока'),
    ])
    def test_make_move(self, cor, rez):
        board = Board()
        error = board.make_move(cor)
        if error[0]:
            self.assertTrue(rez in ('', 'Ok', 'not error'))
        else:
            self.assertEqual(error[1], rez)

    @parameterized.expand([
        (Pawn(0, 0, True), King(1, 1, False), True),
        (Pawn(0, 0, True), King(1, 0, False), False),
        (Pawn(0, 0, True), King(1, 1, True), False),
    ])
    def test_is_under_attack_true_king(self, attack: Figure, protection: Figure, rez):
        board = Board(arrange_figure=False)
        board.board[attack.row][attack.col] = attack
        board.board[protection.row][protection.col] = protection
        self.assertEqual(board.is_under_attack(protection), rez)

    def test_is_current_player(self):
        board = Board()
        self.assertTrue(board.is_current_player(True))
        board.make_move('e2-e4')
        self.assertFalse(board.is_current_player(True))

    @parameterized.expand([
        (Pawn(0, 0, True), King(1, 1, False), [Pawn(0, 0, True)]),
        (Pawn(0, 0, True), King(1, 0, True), [Pawn(0, 0, True)]),
        (Pawn(0, 0, True), Pawn(1, 1, True), [Pawn(0, 0, True), Pawn(1, 1, True)]),
    ])
    def test_get_figure(self, true_figure: Figure, other_figure: Figure, rez: list):
        board = Board(arrange_figure=False)
        board.board[true_figure.row][true_figure.col] = true_figure
        board.board[other_figure.row][other_figure.col] = other_figure
        self.assertEqual(board.get_figure(type(true_figure), true_figure.color), rez)


class TestFigure(unittest.TestCase):
    @parameterized.expand([
        (Pawn(1, 1, True), 'wP'),
        (Pawn(1, 1, False), 'bP'),
        (Rook(1, 1, True), 'wR'),
        (Figure(1, 1, True), 'wF'),
        (Figure(1, 1, Figure), 'bF'),
    ])
    def test_str(self, figure, rez):
        self.assertEqual(str(figure), rez)

    @parameterized.expand([
        (Figure(0, 1, True), Figure(0, 1, True), True),
        (Figure(0, 1, True), Figure(1, 1, True), False),
        (Figure(0, 1, True), Pawn(0, 1, True), False),
        (Figure(0, 1, True), Figure(1, 1, False), False),
    ])
    def test_eq_nq(self, figure, other_figure, rez):
        self.assertEqual(figure == other_figure, rez)
        self.assertEqual(figure != other_figure, not rez)

    @parameterized.expand([
        (Figure(0, 1, True), Figure(0, 1, True), False),
        (Figure(0, 1, True), Figure(1, 1, True), False),
        (Figure(0, 1, True), Pawn(0, 1, True), True),
        (Figure(0, 1, True), Figure(1, 1, False), False),
    ])
    def test_lt_ge(self, figure, other_figure, rez):
        self.assertEqual(figure < other_figure, rez)
        self.assertEqual(figure >= other_figure, not rez)

    @parameterized.expand([
        (Figure(0, 1, True), Figure(0, 1, True), False),
        (Figure(0, 1, True), Figure(1, 1, True), False),
        (Figure(0, 1, True), Pawn(0, 1, True), False),
        (Figure(0, 1, True), Figure(1, 1, False), False),
        (King(0, 1, True), Figure(1, 1, False), True),
    ])
    def test_gt_le(self, figure, other_figure, rez):
        self.assertEqual(figure > other_figure, rez)
        self.assertEqual(figure <= other_figure, not rez)

    @parameterized.expand([
        (Figure(0, 1, True), 1, sp_figure[1](0, 1, True)),
        (Figure(0, 1, True), 4, sp_figure[4](0, 1, True)),
        (Figure(0, 1, True), len(sp_figure) + 1, sp_figure[1](0, 1, True)),
        (Pawn(0, 1, True), 1, sp_figure[sp_figure.index(Pawn) + 1](0, 1, True)),
    ])
    def test_add(self, figure, term, rez):
        self.assertEqual(figure + term, rez)
        self.assertEqual(term + figure, rez)
        figure += term
        self.assertEqual(figure, rez)

    @parameterized.expand([
        (King(0, 1, True), 1, sp_figure[-2](0, 1, True)),
        (King(0, 1, True), 4, sp_figure[-5](0, 1, True)),
        (King(0, 1, True), len(sp_figure) - 1, sp_figure[0](0, 1, True)),
        (Pawn(0, 1, True), 1, sp_figure[sp_figure.index(Pawn) - 1](0, 1, True)),
    ])
    def test_sub(self, figure, term, rez):
        self.assertEqual(figure - term, rez)
        self.assertEqual(term - figure, rez)
        figure -= term
        self.assertEqual(figure, rez)

    @parameterized.expand([
        (Figure(1, 1, True), 2, 2),
    ])
    def test_set_position(self, figure: Figure, new_row: int, new_col: int):
        figure.set_position(new_row, new_col)
        self.assertEqual(figure.row, new_row)
        self.assertEqual(figure.col, new_col)

    @parameterized.expand([
        (Figure(0, 1, True), Figure(0, 1, True), False),
        (Figure(0, 1, True), Figure(1, 1, True), False),
        (Figure(0, 1, True), None, False),
        (Figure(0, 1, True), Figure(1, 1, False), True),
    ])
    def test_is_enemy(self, figure: Figure, enemy: Figure | None, rez: bool):
        self.assertEqual(figure.is_enemy(enemy), rez)

    @parameterized.expand([
        (Figure(0, 1, True), Figure(0, 1, True), True),
        (Figure(0, 1, True), Figure(1, 1, True), True),
        (Figure(0, 1, True), None, True),
        (Figure(0, 1, True), Figure(1, 1, False), False),
    ])
    def test_can_move(self, figure: Figure, enemy: Figure | None, rez: bool):
        self.assertNotEqual(figure.is_enemy(enemy), rez)


class TestPawn(unittest.TestCase):
    @parameterized.expand([
        (1, 1, True),
        (2, 1, True),
        (3, 1, False),
        (1, 2, False),
        (2, 2, False),
        (1, 2, True, Pawn(1, 2, False)),
        (1, 2, False, Pawn(1, 2, True)),
    ])
    def test_move(self, row, col, rez, other_figure=None):
        bb = Board(arrange_figure=False)
        board = bb.board
        board[0][1] = Pawn(0, 1, True)
        if other_figure:
            board[other_figure.row][other_figure.col] = other_figure
        self.assertEqual(board[0][1].can_move(board, row, col), rez)


class TestKnight(unittest.TestCase):
    @parameterized.expand([
        (1, 2, True),
        (1, 3, False),
        (2, 1, True),
        (2, 2, False),
    ])
    def test_move(self, row, col, rez, other_figure=None):
        board = Board(arrange_figure=False).board
        board[0][0] = Knight(0, 0, True)
        if other_figure:
            board[other_figure.row][other_figure.col] = other_figure
        self.assertEqual(board[0][0].can_move(board, row, col), rez)


class TestBishop(unittest.TestCase):
    @parameterized.expand([
        (0, 0, True),
        (1, 7, True),
        (7, 1, True),
        (7, 7, True),
        (6, 7, False),
        (5, 0, False),
        (7, 7, False, Pawn(6, 6, True)),
        (7, 7, False, Pawn(6, 6, False)),
        (6, 6, True, Pawn(7, 7, False)),
    ])
    def test_move(self, row, col, rez, other_figure=None):
        bb = Board(arrange_figure=False)
        board = bb.board
        board[4][4] = Bishop(4, 4, True)
        if other_figure:
            board[other_figure.row][other_figure.col] = other_figure
        self.assertEqual(board[4][4].can_move(board, row, col), rez)


class TestRock(unittest.TestCase):
    @parameterized.expand([
        (4, 0, True),
        (0, 4, True),
        (7, 4, True),
        (4, 7, True),
        (6, 7, False),
        (6, 6, False),
        (4, 0, False, Pawn(4, 1, True)),
        (4, 0, False, Pawn(4, 1, False)),
        (4, 1, True, Pawn(0, 1, False)),
    ])
    def test_move(self, row, col, rez, other_figure=None):
        bb = Board(arrange_figure=False)
        board = bb.board
        board[4][4] = Rook(4, 4, True)
        if other_figure:
            board[other_figure.row][other_figure.col] = other_figure
        self.assertEqual(board[4][4].can_move(board, row, col), rez)


class TestQueen(unittest.TestCase):
    @parameterized.expand([
        (4, 0, True),
        (0, 4, True),
        (7, 4, True),
        (4, 7, True),
        (6, 7, False),
        (4, 0, False, Pawn(4, 1, True)),
        (4, 0, False, Pawn(4, 1, False)),
        (4, 1, True, Pawn(0, 1, False)),
        (0, 0, True),
        (1, 7, True),
        (7, 1, True),
        (7, 7, True),
        (6, 7, False),
        (7, 7, False, Pawn(6, 6, True)),
        (7, 7, False, Pawn(6, 6, False)),
        (6, 6, True, Pawn(7, 7, False)),
    ])
    def test_move(self, row, col, rez, other_figure=None):
        bb = Board(arrange_figure=False)
        board = bb.board
        board[4][4] = Queen(4, 4, True)
        if other_figure:
            board[other_figure.row][other_figure.col] = other_figure
        self.assertEqual(board[4][4].can_move(board, row, col), rez)


class TestKing(unittest.TestCase):
    @parameterized.expand([
        (1, 0, True),
        (1, 1, True),
        (0, 1, True),
        (1, 2, False),
    ])
    def test_move(self, row, col, rez):
        bb = Board(arrange_figure=False)
        board = bb.board
        board[0][0] = King(0, 0, True)
        print(bb)
        self.assertEqual(board[0][0].can_move(board, row, col), rez)