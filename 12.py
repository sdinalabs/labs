import tkinter as tk
from tkinter import messagebox
import random

class Ship:
    def __init__(self, size):
        self.size = size
        self.positions = []
        self.hits = 0

    def is_sunk(self):
        return self.hits == self.size

class BattleshipGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Морской бой")
        self.root.geometry("800x600")
        self.ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.game_over_called = False
        self.create_ship_placement_window()
    def create_ship_placement_window(self):
        self.clear_window()
        tk.Label(self.root, text="РАССТАНОВКА КОРАБЛЕЙ", font=("Arial", 18, "bold")).pack(pady=10)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Случайная расстановка", command=self.random_place_player_ships,
                  font=("Arial", 12), bg="lightgreen").pack(side=tk.LEFT, padx=5)
        self.start_btn = tk.Button(btn_frame, text="Начать игру", command=self.start_battle,
                                   font=("Arial", 12), state=tk.DISABLED)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)
        self.preview_buttons = [[None] * 10 for z in range(10)]
        for i in range(10):
            for j in range(10):
                btn = tk.Button(board_frame, width=2, height=1, bg="white", state=tk.DISABLED)
                btn.grid(row=i, column=j, padx=1, pady=1)
                self.preview_buttons[i][j] = btn
    def random_place_player_ships(self):
        self.player_board = [[0] * 10 for z in range(10)]
        self.player_ships = []
        if not self.place_ships_randomly(self.player_board, self.player_ships):
            messagebox.showerror("Ошибка", "Не удалось разместить корабли. Попробуйте ещё раз.")
            return
        for i in range(10):
            for j in range(10):
                self.preview_buttons[i][j].config(bg="lightblue" if self.player_board[i][j] == 1 else "white")
        self.start_btn.config(state=tk.NORMAL)
    def place_ships_randomly(self, board, ships_list):
        board[:] = [[0] * 10 for z in range(10)]
        ships_list.clear()
        for size in sorted(self.ship_sizes, reverse=True):
            placed = False
            for z in range(500):
                orient = random.choice(["h", "v"])
                x = random.randint(0, 9 if orient == "h" else 10 - size)
                y = random.randint(0, 10 - size if orient == "h" else 9)
                positions = [(x + (i if orient == "v" else 0), y + (i if orient == "h" else 0)) for i in range(size)]
                if all(
                    0 <= r < 10 and 0 <= c < 10 and board[r][c] == 0 and
                    all(board[r + dr][c + dc] == 0 for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                        if 0 <= r + dr < 10 and 0 <= c + dc < 10)
                    for r, c in positions
                ):
                    ship = Ship(size)
                    for r, c in positions:
                        board[r][c] = 1
                        ship.positions.append((r, c))
                    ships_list.append(ship)
                    placed = True
                    break
            if not placed:
                return False
        return True
    def start_battle(self):
        if not hasattr(self, 'player_board'):
            messagebox.showwarning("Внимание", "Сначала расставьте корабли!")
            return
        self.setup_bot_ships()
        self.clear_window()
        self.game_started = True
        tk.Label(self.root, text="БОЙ НАЧАЛСЯ!", font=("Arial", 18, "bold")).pack(pady=10)
        boards_frame = tk.Frame(self.root)
        boards_frame.pack(pady=20)
        self.create_battle_board(boards_frame, "Ваше поле", self.player_board, 0, False)
        self.create_battle_board(boards_frame, "Поле бота", self.bot_board, 1, True)
        self.status_label = tk.Label(self.root, text="Ваш ход!", font=("Arial", 14), fg="green")
        self.status_label.pack(pady=10)
        self.player_turn = True
        self.bot_hunt_stack = []
        self.bot_last_hit = None
        self.bot_hit_sequence = [] 
    def setup_bot_ships(self):
        self.bot_board = [[0] * 10 for z in range(10)]
        self.bot_ships = []
        self.place_ships_randomly(self.bot_board, self.bot_ships)
    def create_battle_board(self, parent, title, board, column, interactive):
        frame = tk.Frame(parent)
        frame.grid(row=0, column=column, padx=20)
        tk.Label(frame, text=title, font=("Arial", 12, "bold")).pack()
        coords_frame = tk.Frame(frame)
        coords_frame.pack()
        tk.Label(coords_frame, width=3).grid(row=0, column=0)
        for j in range(10):
            tk.Label(coords_frame, text=chr(65 + j), width=3, font=("Arial", 10, "bold")).grid(row=0, column=j + 1)
        board_frame = tk.Frame(frame)
        board_frame.pack(pady=10)
        buttons = [[None] * 10 for z in range(10)]
        for i in range(10):
            tk.Label(board_frame, text=str(i + 1), width=3, font=("Arial", 10, "bold")).grid(row=i, column=0)
            for j in range(10):
                if interactive:
                    btn = tk.Button(board_frame, width=3, height=1, bg="white",
                                    command=lambda x=i, y=j: self.player_move(x, y))
                else:
                    color = "lightblue" if board[i][j] == 1 else "white"
                    btn = tk.Button(board_frame, width=3, height=1, bg=color, state=tk.DISABLED)
                btn.grid(row=i, column=j + 1, padx=1, pady=1)
                buttons[i][j] = btn
        if interactive:
            self.bot_buttons = buttons
        else:
            self.player_buttons = buttons
    def player_move(self, x, y):
        if not self.player_turn or self.bot_board[x][y] in (2, 3):
            return
        if self.bot_board[x][y] == 1:
            self.bot_board[x][y] = 2
            self.bot_buttons[x][y].config(bg="red", text="X", state=tk.DISABLED)
            for ship in self.bot_ships:
                if (x, y) in ship.positions:
                    ship.hits += 1
                    if ship.is_sunk():
                        self.status_label.config(text="Вы потопили корабль!")
                        for px, py in ship.positions:
                            for dx in (-1, 0, 1):
                                for dy in (-1, 0, 1):
                                    nx, ny = px + dx, py + dy
                                    if 0 <= nx < 10 and 0 <= ny < 10 and self.bot_board[nx][ny] == 0:
                                        self.bot_board[nx][ny] = 3
                                        self.bot_buttons[nx][ny].config(bg="grey", text="", state=tk.DISABLED)
                    else:
                        self.status_label.config(text="Попадание! Ходите снова!")
                    break
        else:
            self.bot_board[x][y] = 3
            self.bot_buttons[x][y].config(bg="grey", text="", state=tk.DISABLED)
            self.status_label.config(text="Промах! Ход бота.")
            self.player_turn = False
            self.root.after(400, self.bot_move)
        if not self.game_over_called and all(ship.is_sunk() for ship in self.bot_ships):
            self.game_over_called = True
            self.game_over("Вы победили!")
    def bot_move(self):
        if len(self.bot_hit_sequence) >= 2:
            (x0, y0), (x1, y1) = self.bot_hit_sequence[0], self.bot_hit_sequence[1]
            dx = x1 - x0
            dy = y1 - y0
            last_x, last_y = self.bot_hit_sequence[-1]
            first_x, first_y = self.bot_hit_sequence[0]
            candidates = [
                (last_x + dx, last_y + dy),
                (first_x - dx, first_y - dy)
            ]
            for nx, ny in candidates:
                if 0 <= nx < 10 and 0 <= ny < 10 and self.player_board[nx][ny] not in (2, 3):
                    self.execute_bot_shot(nx, ny)
                    return
        if self.bot_hunt_stack:
            x, y = self.bot_hunt_stack.pop(0)
            if 0 <= x < 10 and 0 <= y < 10 and self.player_board[x][y] not in (2, 3):
                self.execute_bot_shot(x, y)
                return
        if self.bot_last_hit and not self.bot_hunt_stack:
            x, y = self.bot_last_hit
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10 and self.player_board[nx][ny] not in (2, 3):
                    self.bot_hunt_stack.append((nx, ny))
            if self.bot_hunt_stack:
                x, y = self.bot_hunt_stack.pop(0)
                self.execute_bot_shot(x, y)
                return
        empty_cells = [(i, j) for i in range(10) for j in range(10) if self.player_board[i][j] not in (2, 3)]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.execute_bot_shot(x, y)
        else:
            self.player_turn = True
            self.status_label.config(text="Ваш ход!")
    def execute_bot_shot(self, x, y):
        if self.player_board[x][y] == 1:
            self.player_board[x][y] = 2
            self.player_buttons[x][y].config(bg="red", text="X")
            for ship in self.player_ships:
                if (x, y) in ship.positions:
                    ship.hits += 1
                    self.bot_last_hit = (x, y)
                    self.bot_hit_sequence.append((x, y))  
                    if ship.is_sunk():
                        for px, py in ship.positions:
                            for dx in (-1, 0, 1):
                                for dy in (-1, 0, 1):
                                    nx, ny = px + dx, py + dy
                                    if 0 <= nx < 10 and 0 <= ny < 10 and self.player_board[nx][ny] == 0:
                                        self.player_board[nx][ny] = 3
                                        self.player_buttons[nx][ny].config(bg="gray", text="")
                        self.bot_hunt_stack = []
                        self.bot_last_hit = None
                        self.bot_hit_sequence = []  
                        self.status_label.config(text="Бот потопил ваш корабль!")
                    else:
                        self.status_label.config(text="Бот попал!")
                    break
            self.root.after(400, self.bot_move)
        else:
            self.player_board[x][y] = 3
            self.player_buttons[x][y].config(bg="gray", text="")
            self.status_label.config(text="Ваш ход!")
            self.player_turn = True
        if not self.game_over_called and all(ship.is_sunk() for ship in self.player_ships):
            self.game_over_called = True
            self.game_over("Бот победил!")
    def game_over(self, message):
        self.game_started = False
        messagebox.showinfo("Игра окончена", message)
        tk.Button(self.root, text="Новая игра", command=self.restart_game,
                  font=("Arial", 12), bg="lightgreen").pack(pady=10)
    def restart_game(self):
        self.__init__()
        self.create_ship_placement_window()
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def run(self):
        self.root.mainloop()
if __name__ == "__main__":
    game = BattleshipGame()
    game.run()
