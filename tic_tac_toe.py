import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

EMPTY = ""
HUMAN = "X"
COMPUTER = "O"
SCORE_WIN = 1
SCORE_LOSE = -1
SCORE_DRAW = 0

COLOR_BACKGROUND = "#382b2b" 
COLOR_FRAME = "#1e1515" 
COLOR_X = "#a85d38" 
COLOR_O = "#70a498" 
COLOR_BUTTON_BG = "#5c4747" 
COLOR_HIGHLIGHT = "#ffd700"
COLOR_FOOTER_TEXT = "#95a5a6" 

COLOR_SCORE_LABEL_X = COLOR_X
COLOR_SCORE_LABEL_O = COLOR_O
COLOR_SCORE_LABEL_DRAW = "#7f8c8d" 

GAME_FONT = "Comic Sans MS" 
STATUS_FONT = "Comic Sans MS"

TITLE_FONT_SIZE = 18
GAME_FONT_SIZE = 28 
FOOTER_FONT_SIZE = 10 
SCORE_FONT_SIZE = 14

class TicTacToe:
    
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe")
        root.resizable(True, True) 
        root.configure(bg=COLOR_BACKGROUND)
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
        
        frame = tk.Frame(parent, bg=COLOR_BACKGROUND, padx=5, pady=0)
        
        label_text = tk.Label(frame, text=text, font=(STATUS_FONT, SCORE_FONT_SIZE, "bold"), fg=title_color, bg=COLOR_BACKGROUND)
        label_text.pack()
        
        label_value = tk.Label(frame, text="0", font=(STATUS_FONT, SCORE_FONT_SIZE), fg="#e0e0e0", bg=COLOR_BACKGROUND)
        label_value.pack()
        
        return frame, label_value

    def create_widgets(self):
        
        top_controls_frame = tk.Frame(self.root, bg=COLOR_BACKGROUND, pady=10)
        top_controls_frame.pack(padx=20, pady=10, fill="x")

        mode_frame = tk.Frame(top_controls_frame, bg=COLOR_BACKGROUND)
        mode_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(mode_frame, text="Select Mode:", bg=COLOR_BACKGROUND, fg="#e0e0e0", font=(STATUS_FONT, TITLE_FONT_SIZE, "bold")).pack(side=tk.LEFT, padx=5)

        modes = [("Human vs Computer", "Human vs Computer"), ("Human vs Human", "Human vs Human")]
        for text, mode_val in modes:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.mode, value=mode_val, command=self.on_mode_change, 
                                font=(STATUS_FONT, 14), bg=COLOR_BACKGROUND, fg="#e0e0e0", selectcolor=COLOR_BACKGROUND, 
                                activebackground=COLOR_BACKGROUND, activeforeground=COLOR_O)
            rb.pack(side=tk.LEFT, padx=10)
        
        difficulty_frame = tk.Frame(top_controls_frame, bg=COLOR_BACKGROUND)
        difficulty_frame.pack(side=tk.RIGHT, padx=15)
        self.difficulty_label = tk.Label(difficulty_frame, text="Difficulty:", bg=COLOR_BACKGROUND, fg="#e0e0e0", font=(STATUS_FONT, TITLE_FONT_SIZE, "bold"))
        self.difficulty_label.pack(side=tk.LEFT, padx=5)
        
        difficulties = [("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")]
        for text, diff_val in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=text, variable=self.difficulty, value=diff_val, command=self.on_difficulty_change, 
                                font=(STATUS_FONT, 12), bg=COLOR_BACKGROUND, fg="#e0e0e0", selectcolor=COLOR_BACKGROUND, 
                                activebackground=COLOR_BACKGROUND, activeforeground=COLOR_O)
            rb.pack(side=tk.LEFT, padx=5)
        
        self.toggle_difficulty_controls(self.mode.get())

        scoreboard_frame = tk.Frame(self.root, bg=COLOR_BACKGROUND, padx=20, pady=5, bd=0)
        scoreboard_frame.pack(pady=5, fill="x", padx=20)

        self.x_score_frame, self.x_score_label = self.create_score_label(scoreboard_frame, "X WINS", COLOR_SCORE_LABEL_X)
        self.x_score_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=15)

        self.o_score_frame, self.o_score_label = self.create_score_label(scoreboard_frame, "O WINS", COLOR_SCORE_LABEL_O)
        self.o_score_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=15)

        self.draw_score_frame, self.draw_score_label = self.create_score_label(scoreboard_frame, "DRAWS", COLOR_SCORE_LABEL_DRAW)
        self.draw_score_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=15)

        self.update_score()

        self.status_label = tk.Label(self.root, font=(STATUS_FONT, 20, "bold"), bg=COLOR_BACKGROUND, fg=COLOR_HIGHLIGHT, pady=5)
        self.status_label.pack(pady=5, fill="x")

        self.board_frame = tk.Frame(self.root, bg=COLOR_FRAME, bd=8, relief=tk.RIDGE)
        self.board_frame.pack(padx=20, pady=10, expand=True, fill="both")
        
        for r in range(3):
            row = []
            for c in range(3):
                btn = tk.Button(self.board_frame, text="", 
                                width=5, height=0,
                                bg=COLOR_BUTTON_BG, 
                                font=(GAME_FONT, GAME_FONT_SIZE, "bold"),
                                relief=tk.FLAT, bd=3,
                                activebackground=COLOR_BUTTON_BG,
                                command=lambda rr=r, cc=c: self.on_click(rr, cc))
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew") 
                row.append(btn)
            self.buttons.append(row)
            
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1) 
            self.board_frame.grid_columnconfigure(i, weight=1)
            
        footer_frame = tk.Frame(self.root, bg=COLOR_BACKGROUND, pady=5)
        footer_frame.pack(padx=20, pady=(5, 10), fill="x")
        
        footer_text = (
            "Tip: Click OK on the pop-up to start a new game. "
            "Score resets automatically when Mode or Difficulty is changed."
        )
        
        tk.Label(footer_frame, text=footer_text, 
                 font=(STATUS_FONT, FOOTER_FONT_SIZE), 
                 fg=COLOR_FOOTER_TEXT, 
                 bg=COLOR_BACKGROUND).pack(fill="x")


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
        self.board = [[EMPTY]*3 for _ in range(3)]
        
        self.current_player = HUMAN
        self.status_label["text"] = "X's Turn"

        self.game_over = False
        
        for r in range(3):
            for c in range(3):
                self.buttons[r][c]["text"] = ""
                self.buttons[r][c]["state"] = tk.NORMAL
                self.buttons[r][c]["bg"] = COLOR_BUTTON_BG
                self.buttons[r][c]["fg"] = COLOR_BACKGROUND 
                self.buttons[r][c]["disabledforeground"] = COLOR_BACKGROUND

    def reset_score(self):
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.update_score()

    def on_click(self, r, c):
        if self.game_over or self.board[r][c] != EMPTY:
            return

        self.make_move(r, c, self.current_player)
        
        if self.check_game_end():
            return

        if self.mode.get() == "Human vs Human":
            self.current_player = COMPUTER if self.current_player == HUMAN else HUMAN
            self.status_label["text"] = f"{self.current_player}'s Turn"
        else:
            self.status_label["text"] = "Computer thinking..."
            self.root.after(300, self.computer_move)

    def make_move(self, r, c, player):
        self.board[r][c] = player
        self.buttons[r][c]["text"] = player
        color = COLOR_X if player == HUMAN else COLOR_O
        self.buttons[r][c]["fg"] = color
        self.buttons[r][c]["disabledforeground"] = color
        self.buttons[r][c]["state"] = tk.DISABLED

    def get_empty_cells(self, board):
        return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]

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
                self.board[r][c] = COMPUTER
                winner, _ = self.check_winner(self.board)
                self.board[r][c] = EMPTY
                if winner == COMPUTER:
                    best_move = (r, c)
                    break
            
            if best_move is None:
                for r, c in moves_list:
                    self.board[r][c] = HUMAN
                    winner, _ = self.check_winner(self.board)
                    self.board[r][c] = EMPTY
                    if winner == HUMAN:
                        best_move = (r, c)
                        break
            
            if best_move is None and moves_list:
                best_move = random.choice(moves_list)

        elif current_difficulty == "Hard":
            best_score = -float('inf')
            random.shuffle(moves_list) 

            for r, c in moves_list:
                self.board[r][c] = COMPUTER
                score = self.minimax(self.board, False) 
                self.board[r][c] = EMPTY 
                
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                
                if best_score == SCORE_WIN:
                    break

        if best_move:
            r, c = best_move
            self.make_move(r, c, COMPUTER)
            self.check_game_end()
        
        if not self.game_over:
            self.current_player = HUMAN
            self.status_label["text"] = f"{HUMAN}'s Turn"

    def minimax(self, board, is_maximizing):
        winner, _ = self.check_winner(board)
        
        if winner == COMPUTER:
            return SCORE_WIN 
        elif winner == HUMAN:
            return SCORE_LOSE 
        elif self.is_full(board):
            return SCORE_DRAW 

        if is_maximizing:
            best = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == EMPTY:
                        board[r][c] = COMPUTER
                        val = self.minimax(board, False)
                        board[r][c] = EMPTY
                        best = max(best, val)
            return best
        else:
            best = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == EMPTY:
                        board[r][c] = HUMAN
                        val = self.minimax(board, True) 
                        board[r][c] = EMPTY
                        best = min(best, val)
            return best

    def check_winner(self, board):
        for i in range(3):
            if board[i][0] != EMPTY and board[i][0] == board[i][1] == board[i][2]:
                return board[i][0], [(i, 0), (i, 1), (i, 2)]
            if board[0][i] != EMPTY and board[0][i] == board[1][i] == board[2][i]:
                return board[0][i], [(0, i), (1, i), (2, i)]

        if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0], [(0, 0), (1, 1), (2, 2)]
        
        if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2], [(0, 2), (1, 1), (2, 0)]
            
        return None, None 

    def is_full(self, board):
        return all(board[r][c] != EMPTY for r in range(3) for c in range(3))

    def highlight_winning_line(self, winning_line):
        for r, c in winning_line:
            self.buttons[r][c]["bg"] = COLOR_HIGHLIGHT

    def check_game_end(self):
        winner, winning_line = self.check_winner(self.board)
        
        if winner or self.is_full(self.board):
            self.game_over = True
            
            if winner is None:
                self.draws += 1
                result_msg = "The game ended in a draw! Start a New Game?"
            else:
                if winner == HUMAN:
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