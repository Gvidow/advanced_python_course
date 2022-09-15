import unittest
import unittest.mock
from game import PlayingField, Game

import sys
import io


class TestPlayingField(unittest.TestCase):
    def test_init(self):
        field = PlayingField()
        self.assertEqual(field.field, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_get_in_line(self):
        field = PlayingField()
        for i in range(9):
            self.assertEqual(field.get_in_line(i), i + 1)
        field.field[1][1] = 44
        field.field[2][0] = 67
        self.assertEqual(field.get_in_line(4), 44)
        self.assertEqual(field.get_in_line(6), 67)

    def test_get(self):
        field = PlayingField()
        for i in range(3):
            for j in range(3):
                self.assertEqual(field.get(i, j), 3 * i + j + 1)

        field.field[0][2] = -5
        self.assertEqual(field.get(0, 2), -5)

    def test_get_char(self):
        field = PlayingField()
        for i in range(3):
            for j in range(3):
                self.assertEqual(field.get_char(i, j), str(3 * i + j + 1))

        field.field[0][2] = -1
        self.assertEqual(field.get_char(0, 2), "X")

        field.field[1][0] = -2
        self.assertEqual(field.get_char(1, 0), "O")

    def test_update(self):
        field = PlayingField()
        self.assertEqual(field.field[0][0], 1)
        field.update(0, 77)
        self.assertEqual(field.field[0][0], -77)

        field.update(5, 12)
        self.assertEqual(field.field[1][2], -12)

    def test_draw(self):
        field = PlayingField()
        field.field[0][0] = -1
        field.field[0][1] = -2
        std = sys.stdout
        buf = io.StringIO()
        sys.stdout = buf
        field.draw()
        sys.stdout = std

        res = "X│O│3\n─┼─┼─\n4│5│6\n─┼─┼─\n7│8│9\n"
        self.assertEqual(buf.getvalue(), res)


class TestGame(unittest.TestCase):
    def test_init(self):
        game_test = Game()
        self.assertTrue(isinstance(game_test.field, PlayingField))
        self.assertEqual(game_test.num, 1)

    def test_check_move(self):
        game_test = Game()
        self.assertTrue(game_test.check_move(1))
        game_test.field.field[0][0] = -1
        self.assertFalse(game_test.check_move(1))

        self.assertTrue(game_test.check_move(5))
        game_test.field.field[1][1] = -2
        self.assertFalse(game_test.check_move(5))

        self.assertFalse(game_test.check_move(20))
        self.assertFalse(game_test.check_move("5"))

    def test_check_end_game(self):
        game_test = Game()

        self.assertEqual(game_test.check_end_game(), 0)

        game_test.field.field = [
            [-1, -1, -1],
            [4, 5, 6],
            [7, 8, 9],
        ]
        self.assertEqual(game_test.check_end_game(), 1)

        game_test.field.field = [
            [1, 2, 3],
            [-1, -1, -1],
            [7, 8, 9],
        ]
        self.assertEqual(game_test.check_end_game(), 1)

        game_test.field.field = [
            [1, 2, 3],
            [4, 5, 6],
            [-1, -1, -1],
        ]
        self.assertEqual(game_test.check_end_game(), 1)

        game_test.field.field = [
            [-2, -1, -1],
            [-2, 5, 6],
            [-2, 8, 9],
        ]
        self.assertEqual(game_test.check_end_game(), 2)

        game_test.field.field = [
            [-2, -2, -1],
            [-1, -2, 6],
            [-2, -2, 9],
        ]
        self.assertEqual(game_test.check_end_game(), 2)

        game_test.field.field = [
            [-2, -1, -1],
            [-2, 5, -1],
            [-1, 8, -1],
        ]
        self.assertEqual(game_test.check_end_game(), 1)

        game_test.field.field = [
            [-2, -1, -1],
            [-2, -2, 6],
            [7, 8, -2],
        ]
        self.assertEqual(game_test.check_end_game(), 2)

        game_test.field.field = [
            [-2, -1, -1],
            [-2, -1, 6],
            [-1, 8, 9],
        ]
        self.assertEqual(game_test.check_end_game(), 1)

        game_test.field.field = [
            [-2, -1, -2],
            [-2, -2, -1],
            [-1, -2, -1],
        ]
        self.assertEqual(game_test.check_end_game(), 3)

        game_test.field.field = [
            [-1, -1, -1],
            [-2, -2, -1],
            [-1, -2, -2],
        ]
        self.assertEqual(game_test.check_end_game(), 1)

    @unittest.mock.patch("game.Game.event_handler")
    @unittest.mock.patch("game.PlayingField.draw")
    def test_start(self, draw_mock, handler_mock):
        std = sys.stdout
        buf = io.StringIO()
        sys.stdout = buf

        events = [1, 5, 2, 6, 9, 4]
        game = Game()

        def handler():
            return events[game.num - 1]

        handler_mock.side_effect = handler
        game.start()
        sys.stdout = std

        self.assertEqual(buf.getvalue(), "Player2 win\n")
        self.assertEqual(handler_mock.call_count, 6)
        self.assertEqual(draw_mock.call_count, 6)

    def test_event_handler(self):
        std = sys.stdin
        buf = io.StringIO("aaa\n35\n3\n")
        sys.stdin = buf

        game = Game()
        self.assertEqual(game.event_handler(), 3)

        sys.stdin = std


if __name__ == "__main__":
    unittest.main()
