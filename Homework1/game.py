class Game:
    def __init__(self):
        self.pole = [[j + 3 * i for j in range(1, 4)] for i in range(3)]
        self.num = 1

    def get_in_line(self, ind):
        return self.pole[ind // 3][ind % 3]

    def get_char(self, row, col):
        c = self.pole[row][col]
        if c == -1:
            return "X"
        elif c == -2:
            return "O"
        return str(c)

    def draw(self):
        for i in range(2):
            for j in range(2):
                print(self.get_char(i, j) + "│", end="")
            print(self.get_char(i, 2))
            print("─┼─┼─")
        for j in range(2):
            print(self.get_char(2, j) + "│", end="")
        print(self.get_char(2, 2))

    def check_move(self, move):
        if type(move) != int or move > 9 or move < 1:
            return False
        if self.get_in_line(move - 1) in (-1, -2):
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
            if self.get_in_line(i) == self.get_in_line(i + 1) == self.get_in_line(i + 2):
                return self.get_in_line(i)
        for i in range(3):
            if self.get_in_line(i) == self.get_in_line(i + 3) == self.get_in_line(i + 6):
                return self.get_in_line(i)
        if self.get_in_line(0) == self.get_in_line(4) == self.get_in_line(8):
            return self.pole[0][0]
        if self.get_in_line(2) == self.get_in_line(4) == self.get_in_line(6):
            return self.pole[0][2]

        for i in range(3):
            for j in range(3):
                if self.pole[i][j] > 0:
                    break
            else:
                continue
            break
        else:
            return -3
        return None

    def update(self, ind, player):
        ind -= 1
        self.pole[ind // 3][ind % 3] = -player

    def start(self):
        winner = 0
        while not winner:
            self.draw()
            move = self.event_handler()
            self.update(move, (self.num + 1) % 2 + 1)
            winner = self.check_end_game()
            self.num += 1
        if winner == -3:
            print("Draw")
            return
        print(f"Player{-winner} win")


if __name__ == "__main__":
    game = Game()
    game.start()
