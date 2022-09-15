class PlayingField:
    def __init__(self):
        self.field = [[j + 3 * i for j in range(1, 4)] for i in range(3)]

    def get_in_line(self, ind):
        return self.field[ind // 3][ind % 3]

    def get(self, row, col):
        return self.field[row][col]

    def get_char(self, row, col):
        c = self.get(row, col)
        if c == -1:
            return "X"
        elif c == -2:
            return "O"
        return str(c)

    def update(self, ind, player):
        ind -= 1
        self.field[ind // 3][ind % 3] = -player

    def draw(self):
        for i in range(2):
            for j in range(2):
                print(self.get_char(i, j) + "│", end="")
            print(self.get_char(i, 2))
            print("─┼─┼─")
        for j in range(2):
            print(self.get_char(2, j) + "│", end="")
        print(self.get_char(2, 2))


class Game:
    def __init__(self):
        self.field = PlayingField()
        self.num = 1

    def check_move(self, move):
        if type(move) != int or move > 9 or move < 1:
            return False
        if self.field.get_in_line(move - 1) in (-1, -2):
            return False
        return True

    def event_handler(self):
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
        #  0 - game continues
        # -1 - Player1 win
        # -2 - Player2 win
        # -3 - no winner
        for i in (0, 3, 6):
            if self.field.get_in_line(i) == self.field.get_in_line(i + 1) \
                    == self.field.get_in_line(i + 2):
                return self.field.get_in_line(i)
        for i in range(3):
            if self.field.get_in_line(i) == self.field.get_in_line(i + 3) \
                    == self.field.get_in_line(i + 6):
                return self.field.get_in_line(i)
        if self.field.get_in_line(0) == self.field.get_in_line(4) \
                == self.field.get_in_line(8):
            return self.field.get(0, 0)
        if self.field.get_in_line(2) == self.field.get_in_line(4) \
                == self.field.get_in_line(6):
            return self.field.get(0, 2)

        for i in range(3):
            for j in range(3):
                if self.field.get(i, j) > 0:
                    break
            else:
                continue
            break
        else:
            return -3
        return 0

    def start(self):
        winner = 0
        while not winner:
            self.field.draw()
            move = self.event_handler()
            self.field.update(move, (self.num + 1) % 2 + 1)
            winner = self.check_end_game()
            self.num += 1
        if winner == -3:
            print("Draw")
            return
        print(f"Player{-winner} win")


if __name__ == "__main__":
    game = Game()
    game.start()
