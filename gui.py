import tkinter as tk
from quoridor.game import QuoridorGame
from quoridor.ai import random_ai_move

CELL = 50


class QuoridorGUI(tk.Tk):
    def __init__(self, vs_ai=False):
        super().__init__()
        self.title("Quoridor")
        self.vs_ai = vs_ai
        self.game = QuoridorGame()
        self.mode = "move"

        self.canvas = tk.Canvas(self, width=CELL * 9, height=CELL * 9, bg="white")
        self.canvas.pack()

        btns = tk.Frame(self)
        tk.Button(btns, text="Move", command=lambda: self.set_mode("move")).pack(side="left")
        tk.Button(btns, text="Horizontal Wall", command=lambda: self.set_mode("h")).pack(side="left")
        tk.Button(btns, text="Vertical Wall", command=lambda: self.set_mode("v")).pack(side="left")
        btns.pack()

        self.status = tk.Label(self, text="")
        self.status.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def set_mode(self, mode):
        self.mode = mode
        self.status.config(text=f"Player {self.game.current_player} - {self.mode}")

    def cell_coords(self, r, c):
        return c * CELL, r * CELL, (c + 1) * CELL, (r + 1) * CELL

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(9):
            for c in range(9):
                self.canvas.create_rectangle(*self.cell_coords(r, c), outline="black")

        for r, c in self.game.horizontal_walls:
            x0, y0, x1, y1 = self.cell_coords(r, c)
            self.canvas.create_rectangle(x0, y0 + CELL // 2 - 4, x1 + CELL, y0 + CELL // 2 + 4, fill="brown")
        for r, c in self.game.vertical_walls:
            x0, y0, x1, y1 = self.cell_coords(r, c)
            self.canvas.create_rectangle(x0 + CELL // 2 - 4, y0, x0 + CELL // 2 + 4, y1 + CELL, fill="brown")

        for player, (r, c) in self.game.positions.items():
            x0, y0, x1, y1 = self.cell_coords(r, c)
            self.canvas.create_oval(x0 + CELL * 0.25, y0 + CELL * 0.25, x1 - CELL * 0.25, y1 - CELL * 0.25,
                                     fill="blue" if player == 0 else "red")

        self.status.config(text=f"Player {self.game.current_player} - {self.mode}")

    def on_click(self, event):
        c = event.x // CELL
        r = event.y // CELL
        try:
            if self.mode == "move":
                winner = self.game.move_pawn(r, c)
            else:
                self.game.place_wall(r, c, self.mode)
                winner = None
        except Exception as e:
            self.status.config(text=str(e))
            return

        if winner is not None:
            self.draw_board()
            self.status.config(text=f"Player {winner} wins!")
            return

        if self.vs_ai and self.game.current_player == 1:
            random_ai_move(self.game)
            if self.game.current_player is None:
                self.draw_board()
                self.status.config(text="Player 1 wins!" if winner == 0 else "Player 0 wins!")
                return

        self.draw_board()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Play Quoridor with a GUI")
    parser.add_argument("--ai", action="store_true", help="Play against random AI")
    args = parser.parse_args()

    app = QuoridorGUI(vs_ai=args.ai)
    app.mainloop()


if __name__ == "__main__":
    main()
