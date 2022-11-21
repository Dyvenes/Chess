WHITE = 1
BLACK = 0

from denis2 import Choise_figure


class Figure:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        pass

    def can_move(self, board, row, col, row1, col1):
        pass

    def correct_coords(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def paint_field(self, board, attack_field, def_field,  r, c):
        pass

    def get_type(self):
        return None


class Queen(Figure):
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if not self.correct_coords(row, col):
            return False

        if abs(row - row1) != abs(col - col1) and row != row1 and col != col1:
            return False
        if row != row1 and col != col1:
            step = 1 if (row1 >= row) else -1
            step2 = 1 if (col1 >= col) else -1
            c = col
            for r in range(row + step, row1, step):
                c += step2
                if not (board[r][c] is None):
                    return False
        else:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                if not (board[r][col] is None):
                    return False

            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                if not (board[row][c] is None):
                    return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def paint_field(self, board, attack_field, def_field, r, c):
        coef = 1
        rz = r
        cz = c
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                r = rz
                c = cz
                while True:
                    r += i
                    c += j
                    if not self.correct_coords(r, c):
                        break
                    elif def_field and def_field[r][c] != 0:
                        coef = 0
                    elif not (board[r][c] is None):
                        if board[r][c].get_color() != self.color:
                            attack_field[r][c] = coef
                            if board[r][c].char() == "K":
                                attack_field[r][c] = 1
                        break
                    attack_field[r][c] = coef
        c = cz
        for i in range(-1, 2, 2):
            r = rz
            while True:
                r += i
                if not self.correct_coords(r, c):
                    break
                elif def_field and def_field[r][c] != 0:
                    coef = 0
                elif not (board[r][c] is None):
                    print(board[r][c], self.color)
                    if board[r][c].get_color() != self.color:
                        attack_field[r][c] = coef
                        if board[r][c].char() == "K":
                            attack_field[r][c] = 1
                    break
                attack_field[r][c] = coef
        r = rz
        for i in range(-1, 2, 2):
            c = cz
            while True:
                c += i
                if not self.correct_coords(r, c):
                    break
                elif def_field and def_field[r][c] != 0:
                    coef = 0
                elif not (board[r][c] is None):
                    if board[r][c].get_color() != self.color:
                        attack_field[r][c] = coef
                        if board[r][c].char() == "K":
                            attack_field[r][c] = 1
                    break
                attack_field[r][c] = coef
        return attack_field


class Pawn(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.meta_fig = None
        self.choise_fig = None
        self.chess = None

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if col != col1 or row == row1:
            return False

        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if row + direction == row1:
            return True

        if row == start_row and row + 2 * direction == row1:
            return True

        return False

    def meta_signal(self, chess):
        chess.choise_fig = Choise_figure()
        chess.choise_fig.show()
        chess.choise_fig.figure.connect(self.metamorphose)
        return self.meta_fig

    def metamorphose(self, choise_fig, chess):
        print("metamorphose")
        if choise_fig == 'Bishop':
            chess.meta_fig = Bishop(self.color)
        elif choise_fig == 'Knight':
            chess.meta_fig = Knight(self.color)
        elif choise_fig == 'Rook':
            chess.meta_fig = Rook(self.color)
        else:
            chess.meta_fig = Queen(self.color)

    def can_attack(self, board, row, col, row1, col1):
        if col == col1 or row == row1:
            return False

        if self.color == WHITE:
            direction = 1
        else:
            direction = -1

        if row + direction == row1 and abs(col - col1) == 1:
            return True

        return False

    def paint_field(self, board, attack_field, def_field, r, c):
        if self.color == BLACK:
            if r != 0 and c == 0:
                attack_field[r - 1][c + 1] = 1
            elif r != 0 and c == 7:
                attack_field[r - 1][c - 1] = 1
            elif r != 0:
                attack_field[r - 1][c - 1] = 1
                attack_field[r - 1][c + 1] = 1
        else:
            if r != 7 and c == 0:
                attack_field[r + 1][c + 1] = 1
            elif r != 7 and c == 7:
                attack_field[r + 1][c - 1] = 1
            elif r != 7:
                attack_field[r + 1][c - 1] = 1
                attack_field[r + 1][c + 1] = 1
        return attack_field


class Rook(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.poss_cast = True

    def char(self):
        return "R"

    def can_move(self, board, row, col, row1, col1):
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            if not (board.get_piece(row, c) is None):
                return False
        self.poss_cast = False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def paint_field(self, board, attack_field, def_field, r, c):
        rz = r
        cz = c
        coef = 1
        for i in range(-1, 2, 2):
            r = rz
            while True:
                r += i
                if not self.correct_coords(r, c):
                    break
                elif def_field and def_field[r][c] != 0:
                    coef = 0
                elif not (board[r][c] is None):
                    if board[r][c].get_color() != self.color:
                        attack_field[r][c] = coef
                        if board[r][c].char() == "K":
                            attack_field[r][c] = 1
                    break
                attack_field[r][c] = coef
        r = rz
        for i in range(-1, 2, 2):
            c = cz
            while True:
                c += i
                if not self.correct_coords(r, c):
                    break
                elif def_field and def_field[r][c] != 0:
                    coef = 1
                elif not (board[r][c] is None):
                    if board[r][c].get_color() != self.color:
                        attack_field[r][c] = coef
                        if board[r][c].char() == "K":
                            attack_field[r][c] = 1
                    break
                attack_field[r][c] = coef
        return attack_field


class Knight(Figure):
    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        if not self.correct_coords(row, col):
            return False
        if (abs(row1 - row) == 1 and abs(col1 - col) == 2) or (abs(
                row1 - row) == 2 and abs(col1 - col) == 1):
            return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def paint_field(self, board, attack_field, def_field, r, c):
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) - abs(j) == 0 or i == 0 or j == 0:
                    continue
                if self.correct_coords(r + i, c + j):
                    attack_field[r + i][c + j] = 1
        return attack_field


class Bishop(Figure):
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if not self.correct_coords(row, col):
            return False
        if abs(col - col1) == abs(row - row1):
            return True

        step = 1 if (row1 >= row) else -1
        step2 = 1 if (col1 >= col) else -1
        c = col
        for r in range(row + step, row1, step):
            c += step2
            if not (board.get_piece(r, c) is None):
                return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def paint_field(self, board, attack_field, def_field, r, c):
        coef = 1
        rz = r
        cz = c
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                r = rz
                c = cz
                while True:
                    r += i
                    c += j
                    if not self.correct_coords(r, c):
                        break
                    elif def_field and def_field[r][c] != 0:
                        coef = 0
                    elif not (board[r][c] is None):
                        if board[r][c].get_color() != self.color:
                            attack_field[r][c] = coef
                            if board[r][c].char() == "K":
                                attack_field[r][c] = 1
                        break
                    attack_field[r][c] = coef
        return attack_field


class King(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.poss_cast = True
        self.color = color
        if self.color == WHITE:
            self.coords = (0, 4)
        else:
            self.coords = (7, 4)

    def char(self):
        return "K"

    def can_move(self, board, row, col, row1, col1):
        self.poss_cast = False
        if not self.correct_coords(row, col):
            return False
        print(row, col, row1, col1)
        if abs(row1 - row) != 1 and abs(col1 - col) != 1:
            return False
        else:
            self.coords = (row1, col1)
            return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def paint_field(self, board, attack_field, def_field, r, c):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not self.correct_coords(r + i, c + j):
                    break
                elif not (board[r + i][c + j] is None):
                    break
                attack_field[r + i][c + j] = 1
        return attack_field

    def danger(self, board, attack_field, ch):
        r = self.coords[0]
        c = self.coords[1]
        if ch == 1 and attack_field[r][c] != 0:
            return True
        if attack_field[r][c] != 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.correct_coords(r + i, c + j) and \
                            attack_field[r + i][c + j] == 0 and \
                            board[r + i][c + j] is None:
                        return "шах"
            return "мат"
        return False

    def get_type(self):
        return "King"

