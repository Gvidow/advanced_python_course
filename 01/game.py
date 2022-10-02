"""
Игра крестики-нолики
"""


class PlayingField:
    """
    Игровое поле, представляющее собой двухмерный массив
    целых чисел, размера 3x3
    """
    def __init__(self):
        self.field = [[j + 3 * i for j in range(1, 4)] for i in range(3)]

    def get_in_line(self, ind):
        """
        Представим поле одним массивом из 9 элементов, тогда
        :param ind: индекс элемента, который мы хотим получить в этом массиве,
        начиная с 0
        :return: значение массива (ячейки игрового поля)
        """
        return self.field[ind // 3][ind % 3]

    def get(self, row, col):
        """
        Возвращает значенние, искомой ячейки поля
        :param row: строка
        :param col: столбец
        :return: значение
        """
        return self.field[row][col]

    def get_char(self, row, col):
        """
        Возвращает строковое значенние, искомой ячейки поля
        :param row: строка
        :param col: столбец
        :return: значение(строка)
        """
        digit = self.get(row, col)
        if digit == -1:
            return "X"
        if digit == -2:
            return "O"
        return str(digit)

    def update(self, ind, player):
        """
        Обновляет игровое поле
        :param ind: индекс поля, в массиве представленном в одну строку
        :param player: номер игрока
        """
        self.field[ind // 3][ind % 3] = -player

    def draw(self):
        """
        Отрисовывает игровое поле
        """
        for i in range(2):
            for j in range(2):
                print(self.get_char(i, j) + "│", end="")
            print(self.get_char(i, 2))
            print("─┼─┼─")
        for j in range(2):
            print(self.get_char(2, j) + "│", end="")
        print(self.get_char(2, 2))


class Game:
    """
    Консольная игра, для двух игроков
    """
    def __init__(self):
        self.field = PlayingField()
        self.num = 1

    def check_move(self, move):
        """
        проверка на возможность хода
        :param move: ход - предполагается число от 1 до 9,
        невстречающееся ранее за одну игру
        :return: True or False
        """
        if not isinstance(move, int) or move > 9 or move < 1:
            return False
        if self.field.get_in_line(move - 1) in (-1, -2):
            return False
        return True

    def event_handler(self):
        """
        Спрашивает игрока, чья очередь ходить, куда ходить,
        до тех пор пока не появится ввод, удовлетворяющий правилам игры
        :return: число от 1 до 9
        """
        if self.num % 2 != 0:
            player = "Player1: "
        else:
            player = "Player2: "
        move = -1
        while not self.check_move(move):
            try:
                move = int(input(player))
            except ValueError:
                continue
        return move

    def check_end_game(self):
        """
        проверка на конец игры
        :return: число от 0 да 3
        0 - игра не закончена
        1 - Выигрывает первый игрок
        2 - Выигрывает второй игрок
        3 - Ничья
        """
        for i in (0, 3, 6):
            if self.field.get_in_line(i) == self.field.get_in_line(i + 1) \
                    == self.field.get_in_line(i + 2):
                return -self.field.get_in_line(i)
        for i in range(3):
            if self.field.get_in_line(i) == self.field.get_in_line(i + 3) \
                    == self.field.get_in_line(i + 6):
                return -self.field.get_in_line(i)
        if self.field.get_in_line(0) == self.field.get_in_line(4) \
                == self.field.get_in_line(8):
            return -self.field.get(0, 0)
        if self.field.get_in_line(2) == self.field.get_in_line(4) \
                == self.field.get_in_line(6):
            return -self.field.get(0, 2)

        for i in range(3):
            for j in range(3):
                if self.field.get(i, j) > 0:
                    break
            else:
                continue
            break
        else:
            return 3
        return 0

    def start(self):
        """
        Запуск игры
        """
        winner = 0
        while not winner:
            self.field.draw()
            move = self.event_handler()
            self.field.update(move - 1, (self.num + 1) % 2 + 1)
            winner = self.check_end_game()
            self.num += 1
        if winner == 3:
            print("Draw")
            return
        print(f"Player{winner} win")


if __name__ == "__main__":
    game = Game()
    game.start()
