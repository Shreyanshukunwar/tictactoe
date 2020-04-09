"""Making a constructor and drawing out the board"""

# time module is used to measure the time  of evaluating game tree.
# for  distinction between basic Minmax and Minmax with alpha-beta pruning

import time


class Game:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.current_state = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]

        # Player X always plays first
        self.player_turn = "X"

    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print("{}|".format(self.current_state[i][j]), end=" ")
            print()
        print()

    # Determine if move is legal
    def is_valid(self, px, py):
        if px < 0 or px > 2 and py < 0 and py > 2:
            return False
        elif self.current_state[px][py] != ".":
            return False
        else:
            return True

    # Check if game has ended and return a winner
    def is_end(self):
        # Vertical win
        for i in range(0, 3):
            if (
                self.current_state != "."
                and self.current_state[0][i] == self.current_state[1][i]
                and self.current_state[1][i] == self.current_state[2][i]
            ):
                return self.current_state[0][i]

        # Horizontal win
        for i in range(0, 3):
            if self.current_state[i] == ["X", "X", "X"]:
                return "X"
            elif self.current_state[i] == ["Y", "Y", "Y"]:
                return "Y"

        # first diagonal win
        if (
            self.current_state[0][0] != "."
            and self.current_state[0][0] == self.current_state[1][1]
            and self.current_state[1][1] == self.current_state[2][2]
        ):
            return self.current_state[0][0]

        # second diagonal win
        if (
            self.current_state[0][2] != "."
            and self.current_state[0][2] == self.current_state[1][1]
            and self.current_state[1][1] == self.current_state[2][0]
        ):
            return self.current_state[0][2]

        # is whole board full?
        for i in range(0, 3):
            for j in range(0, 3):
                # if there is empty field, we continue
                if self.current_state[i][j] == ".":
                    return None

        # it's a tie!
        return "."

    # Player O is max, and AI
    def max(self):

        # possible values for maxv are:
        # -1 : loss
        # 0 : tie
        # 1 : win

        # we're initially setting it to -2 as that is worst than the worst possible case
        maxv = -2

        px = None
        py = None

        result = self.is_end()

        # if the game ends, the function needs
        # to return the evaluation function of the end game.

        if result == "X":
            return (-1, 0, 0)  # O loss
        elif result == "O":
            return (1, 0, 0)  # O win
        elif result == ".":
            return (0, 0, 0)  # Draw

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == ".":
                    # On the empty field, player 'O' makes a move and calls Min
                    # that's one branch of the game tree
                    self.current_state[i][j] = "O"
                    (m, min_i, min_j) = self.min()
                    # Fixing the maxv value if needed
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j

                    # Setting back the field to empty
                    self.current_state[i][j] = "."
        return (maxv, px, py)

    # Player 'X' is min, and human
    def min(self):

        # possible values for minv are:
        # -1 : win
        # 0 : tie
        # 1 : loss

        # we're initially setting it to 2 as that is worst than the worst possible case
        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        # if the game ends, the function needs
        # to return the evaluation function of the end game.

        if result == "X":
            return (-1, 0, 0)  # X win
        elif result == "O":
            return (1, 0, 0)  # X loss
        elif result == ".":
            return (0, 0, 0)  # Draw

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == ".":
                    # On the empty field, player 'X' makes a move and calls Min
                    # that's one branch of the game tree
                    self.current_state[i][j] = "X"
                    (m, max_i, max_j) = self.max()
                    # Fixing the minv value if needed
                    if m < minv:
                        maxv = m
                        qx = i
                        qy = j

                    # Setting back the field to empty
                    self.current_state[i][j] = "."
        return (minv, qx, qy)

    def play(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            # Printing the appropriate message if the game has ended
            if self.result != None:
                if self.result == "X":
                    print("The winner is X!")
                elif self.result == "Y":
                    print("The winner is Y!")
                elif self.result == ".":
                    print("It is a tie")
                else:
                    self.initialize_game()
                    return

            # if it's a players turn
            if self.player_turn == "X":

                while True:

                    start = time.time()
                    (m, qx, qy) = self.min()
                    end = time.time()
                    print("Evaluation time: {}s".format(round(end - start, 7)))
                    print("Recommended move: X={}, Y={}".format(qx, qy))

                    px = int(input("Insert the X coordinate: "))
                    py = int(input("Insert the Y coordinate: "))

                    (qx, qy) = (px, py)

                    if self.is_valid(px, py):
                        self.current_state[px][py] = "X"
                        self.player_turn = "O"
                        break
                    else:
                        print("The move is not valid, Try again")

            # If it is AI's turn
            else:
                (m, px, py) = self.max()
                self.current_state[px][py] = "O"
                self.player_turn = "X"


# starting the game
def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
