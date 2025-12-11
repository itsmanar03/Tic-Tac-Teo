import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

empty = ""
human = "X"
computer = "O"
score_win = 1
score_lose = -1
score_draw = 0

color_background = "#382b2b"
color_frame = "#1e1515"
color_x = "#a85d38"
color_o = "#70a498"
color_button_bg = "#5c4747"
color_highlight = "#ffd700"
color_footer_text = "#95a5a6"

color_score_label_x = color_x
color_score_label_o = color_o
color_score_label_draw = "#7f8c8d"

game_font = "Comic Sans MS"
status_font = "Comic Sans MS"

title_font_size = 18
game_font_size = 28
footer_font_size = 10
score_font_size = 14


class TicTacToe:

    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe")
        root.resizable(True, True)
        root.configure(bg=color_background)
        self.set_window_icon("logo.png")

        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        self.mode = tk.StringVar(value="Human vs Computer")
        self.difficulty = tk.StringVar(value="Hard")

        self.buttons = []

        self.create_widgets()
        self.reset_board()

    def set_window_icon(self, icon_path):
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(False, icon_photo)
        except Exception:
            pass

    def create_score_label(self, parent, text, title_color):

        frame = tk.Frame(parent, bg=color_background, padx=5, pady=0)

        label_text = tk.Label(frame, text=text, font=(
            status_font, score_font_size, "bold"), fg=title_color, bg=color_background)
        label_text.pack()

        label_value = tk.Label(frame, text="0", font=(
            status_font, score_font_size), fg="#e0e0e0", bg=color_background)
        label_value.pack()

        return frame, label_value

    def create_widgets(self):

        top_controls_frame = tk.Frame(self.root, bg=color_background, pady=10)
        top_controls_frame.pack(padx=20, pady=10, fill="x")

        mode_frame = tk.Frame(top_controls_frame, bg=color_background)
        mode_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(mode_frame, text="Select Mode:", bg=color_background, fg="#e0e0e0", font=(
            status_font, title_font_size, "bold")).pack(side=tk.LEFT, padx=5)

        modes = [("Human vs Computer", "Human vs Computer"),
                 ("Human vs Human", "Human vs Human")]
        for text, mode_val in modes:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.mode, value=mode_val, command=self.on_mode_change,
                                font=(status_font, 14), bg=color_background, fg="#e0e0e0", selectcolor=color_background,
                                activebackground=color_background, activeforeground=color_o)
            rb.pack(side=tk.LEFT, padx=10)

        difficulty_frame = tk.Frame(top_controls_frame, bg=color_background)
        difficulty_frame.pack(side=tk.RIGHT, padx=15)
        self.difficulty_label = tk.Label(difficulty_frame, text="Difficulty:", bg=color_background, fg="#e0e0e0", font=(
            status_font, title_font_size, "bold"))
        self.difficulty_label.pack(side=tk.LEFT, padx=5)

        difficulties = [("Easy", "Easy"), ("Medium",
                                           "Medium"), ("Hard", "Hard")]
        for text, diff_val in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=text, variable=self.difficulty, value=diff_val, command=self.on_difficulty_change,
                                font=(status_font, 12), bg=color_background, fg="#e0e0e0", selectcolor=color_background,
                                activebackground=color_background, activeforeground=color_o)
            rb.pack(side=tk.LEFT, padx=5)

        self.toggle_difficulty_controls(self.mode.get())

        scoreboard_frame = tk.Frame(
            self.root, bg=color_background, padx=20, pady=5, bd=0)
        scoreboard_frame.pack(pady=5, fill="x", padx=20)

        self.x_score_frame, self.x_score_label = self.create_score_label(
            scoreboard_frame, "X WINS", color_score_label_x)
        self.x_score_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=15)

        self.o_score_frame, self.o_score_label = self.create_score_label(
            scoreboard_frame, "O WINS", color_score_label_o)
        self.o_score_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=15)

        self.draw_score_frame, self.draw_score_label = self.create_score_label(
            scoreboard_frame, "DRAWS", color_score_label_draw)
        self.draw_score_frame.pack(
            side=tk.LEFT, fill="x", expand=True, padx=15)

        self.update_score()

        self.status_label = tk.Label(self.root, font=(
            status_font, 20, "bold"), bg=color_background, fg=color_highlight, pady=5)
        self.status_label.pack(pady=5, fill="x")

        self.board_frame = tk.Frame(
            self.root, bg=color_frame, bd=8, relief=tk.RIDGE)
        self.board_frame.pack(padx=20, pady=10, expand=True, fill="both")

        for r in range(3):
            row = []
            for c in range(3):
                btn = tk.Button(self.board_frame, text="",
                                width=5, height=0,
                                bg=color_button_bg,
                                font=(game_font, game_font_size, "bold"),
                                relief=tk.FLAT, bd=3,
                                activebackground=color_button_bg,
                                command=lambda rr=r, cc=c: self.on_click(rr, cc))
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                row.append(btn)
            self.buttons.append(row)

        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        footer_frame = tk.Frame(self.root, bg=color_background, pady=5)
        footer_frame.pack(padx=20, pady=(5, 10), fill="x")

        footer_text = (
            "Tip: Click OK on the pop-up to start a new game. "
            "Score resets automatically when Mode or Difficulty is changed."
        )

        tk.Label(footer_frame, text=footer_text,
                 font=(status_font, footer_font_size),
                 fg=color_footer_text,
                 bg=color_background).pack(fill="x")

    def toggle_difficulty_controls(self, current_mode):
        difficulty_frame = self.difficulty_label.master
        if current_mode == "Human vs Human":
            difficulty_frame.pack_forget()
        else:
            difficulty_frame.pack(side=tk.RIGHT, padx=15)

    def on_mode_change(self, val=None):
        self.toggle_difficulty_controls(self.mode.get())
        self.reset_score()
        self.reset_board()

    def on_difficulty_change(self):
        self.reset_score()
        self.reset_board()

    def update_score(self):
        self.x_score_label.config(text=str(self.x_wins))
        self.o_score_label.config(text=str(self.o_wins))
        self.draw_score_label.config(text=str(self.draws))

    def reset_board(self):
        self.board = [[empty]*3 for _ in range(3)]

        self.current_player = human
        self.status_label["text"] = "X's Turn"

        self.game_over = False

        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = ""
                self.buttons[r][c]["state"] = tk.NORMAL
                self.buttons[r][c]["bg"] = color_button_bg
                self.buttons[r][c]["fg"] = color_background
                self.buttons[r][c]["disabledforeground"] = color_background

    def reset_score(self):
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.update_score()

    def on_click(self, r, c):
        if self.game_over or self.board[r][c] != empty:
            return

        self.make_move(r, c, self.current_player)

        if self.check_game_end():
            return

        if self.mode.get() == "Human vs Human":
            self.current_player = computer if self.current_player == human else human
            self.status_label["text"] = f"{self.current_player}'s Turn"
        else:
            self.status_label["text"] = "Computer thinking..."
            self.root.after(300, self.computer_move)

    def make_move(self, r, c, player):
        self.board[r][c] = player
        self.buttons[r][c]["text"] = player
        color = color_x if player == human else color_o
        self.buttons[r][c]["fg"] = color
        self.buttons[r][c]["disabledforeground"] = color
        self.buttons[r][c]["state"] = tk.DISABLED

    def get_empty_cells(self, board):
        return [(r, c) for r in range(3) for c in range(3) if board[r][c] == empty]

    def computer_move(self):
        if self.game_over or self.mode.get() == "Human vs Human":
            return

        current_difficulty = self.difficulty.get()
        moves_list = self.get_empty_cells(self.board)
        best_move = None

        if current_difficulty == "Easy":
            if moves_list:
                best_move = random.choice(moves_list)

        elif current_difficulty == "Medium":
            for r, c in moves_list:
                self.board[r][c] = computer
                winner, _ = self.check_winner(self.board)
                self.board[r][c] = empty
                if winner == computer:
                    best_move = (r, c)
                    break

            if best_move is None:
                for r, c in moves_list:
                    self.board[r][c] = human
                    winner, _ = self.check_winner(self.board)
                    self.board[r][c] = empty
                    if winner == human:
                        best_move = (r, c)
                        break

            if best_move is None and moves_list:
                best_move = random.choice(moves_list)

        elif current_difficulty == "Hard":
            best_score = -float('inf')
            random.shuffle(moves_list)

            for r, c in moves_list:
                self.board[r][c] = computer
                score = self.minimax(self.board, False)
                self.board[r][c] = empty

                if score > best_score:
                    best_score = score
                    best_move = (r, c)

                if best_score == score_win:
                    break

        if best_move:
            r, c = best_move
            self.make_move(r, c, computer)
            self.check_game_end()

        if not self.game_over:
            self.current_player = human
            self.status_label["text"] = f"{human}'s Turn"

    def minimax(self, board, is_maximizing):
        winner, _ = self.check_winner(board)

        if winner == computer:
            return score_win
        elif winner == human:
            return score_lose
        elif self.is_full(board):
            return score_draw

        if is_maximizing:
            best = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == empty:
                        board[r][c] = computer
                        val = self.minimax(board, False)
                        board[r][c] = empty
                        best = max(best, val)
            return best
        else:
            best = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == empty:
                        board[r][c] = human
                        val = self.minimax(board, True)
                        board[r][c] = empty
                        best = min(best, val)
            return best

    def check_winner(self, board):
        for i in range(3):
            if board[i][0] != empty and board[i][0] == board[i][1] == board[i][2]:
                return board[i][0], [(i, 0), (i, 1), (i, 2)]
            if board[0][i] != empty and board[0][i] == board[1][i] == board[2][i]:
                return board[0][i], [(0, i), (1, i), (2, i)]

        if board[0][0] != empty and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0], [(0, 0), (1, 1), (2, 2)]

        if board[0][2] != empty and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2], [(0, 2), (1, 1), (2, 0)]

        return None, None

    def is_full(self, board):
        return all(board[r][c] != empty for r in range(3) for c in range(3))

    def highlight_winning_line(self, winning_line):
        for r, c in winning_line:
            self.buttons[r][c]["bg"] = color_highlight

    def check_game_end(self):
        winner, winning_line = self.check_winner(self.board)

        if winner or self.is_full(self.board):
            self.game_over = True

            if winner is None:
                self.draws += 1
                result_msg = "The game ended in a draw! Start a New Game?"
            else:
                if winner == human:
                    self.x_wins += 1
                    result_msg = f"Congratulations! Player {winner} wins! Start a New Game?"
                else:
                    self.o_wins += 1
                    result_msg = f"Player {winner} wins! Start a New Game?"

                if winning_line:
                    self.highlight_winning_line(winning_line)

                self.status_label["text"] = f"{winner} Wins!"

            self.update_score()
            for r in range(3):
                for c in range(3):
                    self.buttons[r][c]["state"] = tk.DISABLED

            messagebox.showinfo("Game Over", result_msg)
            self.reset_board()
            return True
        return False


def main():
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()


if __name__ == "__main__":
    main()
