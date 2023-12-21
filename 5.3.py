from collections import deque
import tkinter as tk
import copy
import random


class CubePuzzleSolver:
    def __init__(self, initial_state, goal_position):
        self.initial_state = initial_state
        self.goal_position = goal_position

    def is_goal_state(self, state):
        return state[self.goal_position[0]][self.goal_position[1]] == 0

    def generate_moves(self, state):
        moves = []
        empty_row, empty_col = None, None

        for i in range(4):
            for j in range(4):
                if state[i][j] == 0:
                    empty_row, empty_col = i, j
                    break

        if empty_row > 0:
            moves.append((empty_row - 1, empty_col, empty_row, empty_col))
        if empty_row < 3:
            moves.append((empty_row + 1, empty_col, empty_row, empty_col))
        if empty_col > 0:
            moves.append((empty_row, empty_col - 1, empty_row, empty_col))
        if empty_col < 3:
            moves.append((empty_row, empty_col + 1, empty_row, empty_col))

        return moves

    def apply_move(self, state, move):
        new_state = copy.deepcopy(state)
        new_state[move[2]][move[3]] = new_state[move[0]][move[1]]
        new_state[move[0]][move[1]] = 0
        return new_state

    def bfs(self):
        queue = deque([(self.initial_state, [])])
        visited = set()

        while queue:
            current_state, path = queue.popleft()

            if self.is_goal_state(current_state):
                return path

            visited.add(tuple(map(tuple, current_state)))

            for move in self.generate_moves(current_state):
                new_state = self.apply_move(current_state, move)
                if tuple(map(tuple, new_state)) not in visited:
                    queue.append((new_state, path + [move]))

        return None  # No solution found


class CubePuzzleUI(tk.Tk):
    def __init__(self, initial_state, goal_position):
        super().__init__()

        self.title("Cube Puzzle Solver")
        self.geometry("400x550")

        self.initial_state = initial_state
        self.goal_position = goal_position

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        self.goal_entry = tk.Entry(self, width=10)
        self.goal_entry.insert(0, f"{goal_position[0]}, {goal_position[1]}")
        self.goal_entry.pack(pady=10)

        self.random_button = tk.Button(
            self, text="Random Initial State", command=self.generate_random_state)
        self.random_button.pack(pady=10)

        self.start_button = tk.Button(
            self, text="Start Puzzle", command=self.start_puzzle)
        self.start_button.pack()

        self.solver = CubePuzzleSolver(initial_state, goal_position)
        self.solution_path = None

        # Show the initial puzzle when the window starts
        self.draw_puzzle(self.initial_state)

    def generate_random_state(self):
        numbers = list(range(16))
        random.shuffle(numbers)
        self.initial_state = [numbers[i:i+4] for i in range(0, 16, 4)]
        self.draw_puzzle(self.initial_state)

    def start_puzzle(self):
        goal_position_str = self.goal_entry.get()
        goal_position = [int(coord) for coord in goal_position_str.split(",")]
        self.goal_position = goal_position

        self.solver = CubePuzzleSolver(self.initial_state, self.goal_position)
        self.solution_path = self.solver.bfs()

        self.draw_puzzle(self.initial_state)

        if self.solution_path:
            self.animate_solution()

    def draw_puzzle(self, state):
        self.canvas.delete("all")
        cell_size = 100

        for i in range(4):
            for j in range(4):
                value = state[i][j]
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, outline="black", width=2)
                self.canvas.create_text(
                    (x0 + x1) // 2, (y0 + y1) // 2, text=str(value), font=("Arial", 16))

    def animate_solution(self):
        for step, move in enumerate(self.solution_path, 1):
            self.after(1000 * step, lambda m=move: self.perform_move(m))

    def perform_move(self, move):
        self.initial_state = self.solver.apply_move(self.initial_state, move)
        self.draw_puzzle(self.initial_state)


if __name__ == "__main__":
    # Initial state (representing the cube arrangement)
    initial_state = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]  # 0 represents the empty cell
    ]

    # Goal position (bottommost corner)
    goal_position = [2, 2]

    # Create an instance of CubePuzzleUI
    app = CubePuzzleUI(initial_state, goal_position)

    # Start the Tkinter main loop
    app.mainloop()
