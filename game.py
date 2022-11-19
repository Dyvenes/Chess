import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt

from denis import BLACK, WHITE, Pawn, King, Rook, Knight, Bishop, Queen
from ch_board import Ui_MainWindow
from denis2 import Choise_color, end_of_game


class Chess(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.main_fig = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        self.action.triggered.connect(self.new_game)
        self.action_2.triggered.connect(self.exit)

        self.rc = ()
        self.color = 1
        self.field = []
        self.ch = 0
        self.count_steps = 0
        self.attack_field = None
        self.signal_color = None
        self.new_game()

    def new_game(self):
        self.attack_field = [[()] * 8 for _ in range(8)]
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        for i in range(8):
            self.field[0][i] = self.main_fig[i](WHITE)
            self.field[1][i] = Pawn(WHITE)
            self.field[7][i] = self.main_fig[i](BLACK)
            self.field[6][i] = Pawn(BLACK)
        for r in range(8):
            for c in range(8):
                if self.field[r][c]:
                    pix_name = self.field[r][c].char()
                    eval(f'self.cell{r}{c}.setPixmap(QPixmap("{pix_name}{self.field[r][c].get_color()}.png"))')
                else:
                    eval(f'self.cell{r}{c}.clear()')
        self.rc = ()
        self.color = 1
        self.count_steps = 0

        self.statusbar.showMessage('Ход белых')

        self.clear_atfld()
        self.attack_field_func()

        #self.signal_color = Choise_color()
        #self.signal_color.show()
        #self.signal_color.color.connect(self.set_color)

    def set_color(self, color):
        if color == 'WHITE':
            pass
            # self.color = WHITE
        # self.color = BLACK

    def end_of_game(self, choise):
        if choise == 'выйти':
            self.exit()
        self.new_game()

    def game(self):
        if not self.current_player_color() == WHITE:
            self.statusBar().showMessage('Ход белых')
        else:
            self.statusBar().showMessage('Ход черных')
        coordinats = (row, col, row1, col1) = self.rc
        if not self.correct_coords(row, col) or not self.correct_coords(row1, col1):
            return
        if not self.is_castling(coordinats):
            if self.move_piece(row, col, row1, col1):
                self.rendering()
                self.clear_atfld()
                self.attack_field_func()
                dan = self.danger()
                print("dan = ", dan)
                if dan == "мат":
                    if not self.current_player_color() == WHITE:
                        self.win = end_of_game(1)
                        self.win.show()
                        self.win.choise.connect(self.end_of_game)
                        return
                    self.win = end_of_game(0)
                    self.win.show()
                    self.win.choise.connect(self.end_of_game)
                    return
            else:
                self.statusBar().showMessage('Координаты некорректны! Попробуйте другой ход!')
                return
        else:
            print("castling")
            if row == 0 and col == 4 and self.current_player_color() == WHITE and self.get_piece(0, 4) == King and \
                    self.get_piece(0, 4).poss_cast:
                print("cast 2")
                if row1 == 0 and col1 == 2 and self.get_piece(0, 0) == Rook and \
                        self.get_piece(0, 0).poss_cast:
                    print("cast 3")
                    self.castling(0, 4, 0, 2, 0, 0, 0, 3)
                elif row1 == 0 and col1 == 6 and self.get_piece(0, 7) == Rook and \
                        self.get_piece(0, 7).poss_cast:
                    self.castling(0, 4, 0, 6, 0, 7, 0, 5)
            elif row == 7 and col == 4 and self.current_player_color() == BLACK and self.get_piece(7, 4) == King and \
                    self.get_piece(7, 4).poss_cast:
                print("cast 2")
                if row1 == 7 and col1 == 2 and self.get_piece(0, 0) == Rook and \
                        self.get_piece(0, 0).poss_cast:
                    print("cast 3")
                    self.castling(7, 4, 7, 2, 7, 0, 7, 3)
                elif row1 == 7 and col1 == 6 and self.get_piece(0, 7) == Rook and \
                        self.get_piece(0, 7).poss_cast:
                    print("cast 3")
                    self.castling(7, 4, 7, 6, 7, 7, 7, 5)
            self.rendering()
        return
        # отрисовка поля в окне игры

    def rendering(self):
        for r in range(8):
            for c in range(8):
                if self.field[r][c]:
                    pix_name = self.field[r][c].char()
                    eval(f'self.cell{r}{c}.setPixmap(QPixmap("{pix_name}{self.field[r][c].get_color()}.png"))')
                else:
                    eval(f'self.cell{r}{c}.clear()')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = (event.x() - 77) // 65
            y = 7 - ((event.y() - 104) // 66)
            if self.correct_coords(x, y):
                self.rc += (y, x)
        if len(self.rc) == 4:
            self.game()
            self.rc = ()

    def exit(self):
        sys.exit(app.exec())

    def correct_coords(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_castling(self, coordinats):
        if coordinats == (0, 4, 0, 2) and \
                coordinats == (0, 4, 0, 6) and \
                coordinats == (7, 4, 7, 2) and \
                coordinats == (7, 4, 7, 6):
            return True
        return False

    def opponent(self, color):
        if color == WHITE:
            return BLACK
        return WHITE

    def current_player_color(self):
        return self.color

    def get_piece(self, row, col):
        return self.field[row][col]

    def move_piece(self, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if self.field[row][col] is None:
            return False
        piece = self.field[row][col]
        if piece.get_color() != self.color:
            return False
        dan = self.danger()
        if dan == "шах":
            self.ch = 1
        elif dan == "мат":
            return False
        else:
            self.ch = 0
        if self.field[row1][col1] is None:
            if not piece.can_move(self.field, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == self.opponent(piece.get_color()):
            if not piece.can_attack(self.field, row, col, row1, col1):
                return False
        else:
            return False
        if piece.char() == "P" and ((piece.get_color() == WHITE and row1 == 7) or
                              (piece.get_color() == BLACK and row1 == 0)):
            piece =  piece.meta_signal()
        self.field[row][col] = None
        save = self.field[row1][col1]
        self.field[row1][col1] = piece
        if self.danger() and self.ch == 1:
            self.field[row][col] = piece
            self.field[row1][col1] = save
            return False
        self.color = self.opponent(self.color)
        return True

    def castling(self, kr, kc, kr1, kc1, rr, rc, rr1, rc1):
        self.field[kr][kc] = None
        self.field[kr1][kc1] = King(self.color)
        self.field[rr][rc] = None
        self.field[rr1][rc1] = Rook(self.color)

    def attack_field_func(self):
        for r in range(8):
            for c in range(8):
                if self.field[r][c] and self.field[r][c].get_color() != self.color:
                    self.def_field = self.field[r][c].paint_field(self.field, self.def_field, None, r, c)
        for r in range(8):
            for c in range(8):
                if self.field[r][c] and self.field[r][c].get_color() != self.color:
                    self.attack_field = self.field[r][c].paint_field(self.field, self.attack_field, self.def_field, r, c)

    def clear_atfld(self):
        self.attack_field = [[0] * 8 for _ in range(8)]
        self.def_field = [[0] * 8 for _ in range(8)]

    def danger(self):
        for i in self.field:
            for j in i:
                if not j:
                    continue
                if j.get_type() == "King" and j.get_color() == self.color:
                    return j.danger(self.field, self.attack_field, self.ch)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Chess()
    game.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
