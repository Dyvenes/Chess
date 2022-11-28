import sqlite3
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt

from figures import BLACK, WHITE, Pawn, King, Rook, Knight, Bishop, Queen
from ch_board import Ui_MainWindow
from graphics import Choise_color, End_of_game, Statistic_rend, Choise_figure


class Chess(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.main_fig = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        self.action.triggered.connect(self.new_game)
        self.action_2.triggered.connect(self.exit)
        self.action_3.triggered.connect(self.statistic_rend)

        self.rc = ()
        self.rc_clone = ()
        self.color = 1
        self.field = []
        self.ch = 0
        self.count_steps = 0
        self.killedWhite = 0
        self.killedBlack = 0
        self.bckground_cells = []
        self.attack_field = None
        self.player_color = 0
        self.nickname = None
        self.show()
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

        for i in range(1, 16):
            for j in (0, 1):
                eval(f'self.killed{j}{i}.clear()')

        self.label_message.setText('Ход белых')

        self.clear_atfld()
        self.attack_field_func()

        self.signal_color = Choise_color()
        self.signal_color.show()
        self.signal_color.color.connect(self.set_color)

    def statistic_rend(self):
        self.stat_rend = Statistic_rend()
        self.stat_rend.show()

    def set_color(self, color):
        self.nickname = color[5:]
        color = color[:6]
        if color == 'WHITE':
            self.player_color = WHITE
        self.player_color = BLACK

    def statistic(self):
        con = sqlite3.connect('chess_db.db')

        cur = con.cursor()

        if self.player_color == self.color:
            win = 1
        else:
            win = 0
        sql = f"""SELECT "колличество игр", "колличество побед", "максимальное колличесвто шагов", "минимальное колличество шагов"
         From statistic Where nicks = '{self.nickname}'"""
        result = cur.execute(sql).fetchall()
        if result:
            result = result[0]
            max_steps = result[2]
            min_steps = result[3]
            if self.count_steps > int(result[2]):
                max_steps = self.count_steps
            if self.count_steps < int(result[3]):
                min_steps = self.count_steps
            count_games = result[0] + 1
            count_wins = result[1] + win
            sqlite_update_query = f"""UPDATE statistic
                SET 'колличество игр' = {count_games},
                 'колличество побед' = {count_wins},
                 '% побед' = '{round(count_wins / count_games * 100, 2)}%',
                 'максимальное колличесвто шагов' = {max_steps},
                 'минимальное колличество шагов' = {min_steps}
                WHERE nicks = '{self.nickname}'"""
            cur.execute(sqlite_update_query)
        else:
            sqlite_insert_query = f"""INSERT INTO statistic
          (nicks, 'колличество игр', 'колличество побед', '% побед',
           'максимальное колличесвто шагов', 'минимальное колличество шагов')
          VALUES
          ("{self.nickname}", 1, {win}, '{win * 100}%', {self.count_steps}, {self.count_steps})"""
            cur.execute(sqlite_insert_query)
        con.commit()
        con.close()

    def end_of_game(self, choise):
        if choise == 'выйти':
            self.exit()
        self.new_game()

    def game(self):
        coordinats = (row, col, row1, col1) = self.rc
        if not self.correct_coords(row, col) or not self.correct_coords(row1, col1):
            return
        if not self.is_castling(coordinats):
            if self.move_piece(row, col, row1, col1):
                dan = self.danger()
                self.rendering()
                self.count_steps += 1
                self.color = self.opponent(self.color)
                self.clear_atfld()
                self.attack_field_func()
                print("dan = ", dan)
                if dan == "мат":
                    self.statistic()
                    if not self.current_player_color() == WHITE:
                        self.win = End_of_game(1)
                        self.win.show()
                        self.win.choise.connect(self.end_of_game)
                        return
                    self.win = End_of_game(0)
                    self.win.show()
                    self.win.choise.connect(self.end_of_game)
                    return
            else:
                if 'НЕВОЗМОЖЕН' not in self.label_message.text():
                    self.label_message.setText(self.label_message.text() + ' || ХОД НЕВОЗМОЖЕН ||')
                return
        else:
            if row == 0 and col == 4 and self.field[row][
                col] and self.current_player_color() == WHITE and self.get_piece(0, 4).char() == 'K' and \
                    self.get_piece(0, 4).poss_cast:
                if row1 == 0 and col1 == 2 and self.field[0][0] and self.get_piece(0, 0).char() == 'R' and \
                        self.get_piece(0, 0).poss_cast and not self.field[0][3] and not self.field[0][1] and \
                        not self.field[0][2] and not self.attack_field[0][2] and not self.attack_field[0][3] and \
                        not self.attack_field[0][4]:
                    self.castling(0, 4, 0, 2, 0, 0, 0, 3)
                    self.color = self.opponent(self.color)
                elif row1 == 0 and col1 == 6 and self.field[0][7] and self.get_piece(0, 7).char() == 'R' and \
                        self.get_piece(0, 7).poss_cast and not self.field[0][5] and not self.field[0][6] and \
                        not self.attack_field[0][5] and not self.attack_field[0][6] and \
                        not self.attack_field[0][4]:
                    self.castling(0, 4, 0, 6, 0, 7, 0, 5)
                    self.color = self.opponent(self.color)
            elif row == 7 and col == 4 and self.field[row][
                col] and self.current_player_color() == BLACK and self.get_piece(7, 4).char() == 'K' and \
                    self.get_piece(7, 4).poss_cast:
                if row1 == 7 and col1 == 2 and self.field[7][0] and self.get_piece(7, 0).char() == 'R' and \
                        self.get_piece(7, 0).poss_cast and not self.field[7][3] and not self.field[7][1] and \
                        not self.field[7][2] and not self.attack_field[7][2] and not self.attack_field[7][3] and \
                        not self.attack_field[7][4]:
                    self.castling(7, 4, 7, 2, 7, 0, 7, 3)
                    self.color = self.opponent(self.color)
                elif row1 == 7 and col1 == 6 and self.field[7][7] and self.get_piece(7, 7).char() == 'R' and \
                        self.get_piece(7, 7).poss_cast and not self.field[7][5] and not self.field[7][6] and \
                        not self.attack_field[7][5] and not self.attack_field[7][6] and \
                        not self.attack_field[7][4]:
                    self.castling(7, 4, 7, 6, 7, 7, 7, 5)
                    self.color = self.opponent(self.color)
            else:
                if 'НЕВОЗМОЖЕН' not in self.label_message.text():
                    self.label_message.setText(self.label_message.text() + ' || ХОД НЕВОЗМОЖЕН ||')
                return
            self.rendering()
        if self.color == WHITE:
            self.label_message.setText('Ход белых')
        else:
            self.label_message.setText('Ход черных')
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
        crds = ()
        if event.button() == Qt.LeftButton:
            if not self.rc and self.rc_clone and self.bckground_cells:
                if self.bckground_cells[1] == 'background-color: darkCyan':
                    self.bckground_cells[1] = self.bckground_cells[0]
                eval(f"self.cell{self.rc_clone[0]}{self.rc_clone[1]}.setStyleSheet('{self.bckground_cells[0]}')")
                eval(f"self.cell{self.rc_clone[2]}{self.rc_clone[3]}.setStyleSheet('{self.bckground_cells[1]}')")
                self.bckground_cells = []
            x = (event.x() - 212) // 65
            y = 7 - ((event.y() - 104) // 66)
            if self.correct_coords(x, y):
                self.rc += (y, x)
                crds = str(y) + str(x)
            if crds:
                eval('self.bckground_cells.append(self.cell' + crds + '.styleSheet())')
                eval("self.cell" + crds + ".setStyleSheet('background-color: darkCyan')")
        if len(self.rc) == 4:
            self.game()
            self.rc_clone = self.rc
            self.rc = ()

    def exit(self):
        sys.exit(app.exec())

    def correct_coords(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_castling(self, coordinats):
        if coordinats == (0, 4, 0, 2) or \
                coordinats == (0, 4, 0, 6) or \
                coordinats == (7, 4, 7, 2) or \
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
        elif not dan:
            self.ch = 0
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == self.opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
            if self.color:
                self.killedWhite += 1
                eval(f'self.killed0{self.killedWhite}.setPixmap(self.cell{row1}{col1}.pixmap())')
            else:
                self.killedBlack += 1
                eval(f'self.killed1{self.killedBlack}.setPixmap(self.cell{row1}{col1}.pixmap())')
        else:
            return False
        if piece.char() == "P" and ((piece.get_color() == WHITE and row1 == 7) or
                                    (piece.get_color() == BLACK and row1 == 0)):
            dialog = Choise_figure()
            dialog.show()
            if dialog.exec_():
                piece = self.meta_fig(dialog.figure)
        self.field[row][col] = None
        save = self.field[row1][col1]
        self.field[row1][col1] = piece
        self.clear_atfld()
        self.attack_field_func()
        if self.danger() and self.ch == 1:
            self.clear_atfld()
            self.attack_field_func()
            for i in self.attack_field:
                print(i)
            a = self.danger()
            self.field[row][col] = piece
            self.field[row1][col1] = save
            return False
        return True

    def meta_fig(self, txt):
        if txt == 'Конь':
            piece = Knight(self.color)
        elif txt == 'Слон':
            piece = Bishop(self.color)
        elif txt == 'Ладья':
            piece = Rook(self.color)
        else:
            piece = Queen(self.color)
        return piece

    def castling(self, kr, kc, kr1, kc1, rr, rc, rr1, rc1):
        self.field[kr][kc] = None
        self.field[kr1][kc1] = King(self.color)
        self.field[rr][rc] = None
        self.field[rr1][rc1] = Rook(self.color)

    def attack_field_func(self):
        for r in range(8):
            for c in range(8):
                if self.field[r][c] and self.field[r][c].get_color() == self.color:
                    self.def_field = self.field[r][c].paint_field(self.field, self.def_field, None, r, c)
        for r in range(8):
            for c in range(8):
                if self.field[r][c] and self.field[r][c].get_color() != self.color:
                    self.attack_field = self.field[r][c].paint_field(self.field, self.attack_field, self.def_field, r,
                                                                     c)

    def clear_atfld(self):
        self.attack_field = [[0] * 8 for _ in range(8)]
        self.def_field = [[0] * 8 for _ in range(8)]

    def danger(self):
        for i in self.field:
            for j in i:
                if not j:
                    continue
                if j.get_type() == "King" and j.get_color() == self.color:
                    return j.danger(self, self.field, self.attack_field, self.ch)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Chess()
    sys.excepthook = except_hook
    sys.exit(app.exec())
