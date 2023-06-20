import tkinter as tk
import random
from collections import deque

maze_size = 15  # Ukuran maze kolom dan baris
maze = [[0] * maze_size for _ in range(maze_size)]
red_droid_x = 0
red_droid_y = 0
green_droid_x = maze_size - 1
green_droid_y = maze_size - 1
red_droid_moving = False
green_droid_moving = False
movement_speed = 500

def create_maze():
    # Inisialisasi seluruh maze dengan dinding
    for row in range(maze_size):
        for col in range(maze_size):
            maze[row][col] = 1

    stack = [(0, 0)]
    while stack:
        current_x, current_y = stack[-1]
        maze[current_y][current_x] = 0

        valid_neighbors = []
        if current_x > 1 and maze[current_y][current_x - 2] == 1:
            valid_neighbors.append((current_x - 2, current_y))
        if current_x < maze_size - 2 and maze[current_y][current_x + 2] == 1:
            valid_neighbors.append((current_x + 2, current_y))
        if current_y > 1 and maze[current_y - 2][current_x] == 1:
            valid_neighbors.append((current_x, current_y - 2))
        if current_y < maze_size - 2 and maze[current_y + 2][current_x] == 1:
            valid_neighbors.append((current_x, current_y + 2))

        if valid_neighbors:
            next_x, next_y = random.choice(valid_neighbors)
            maze[(current_y + next_y) // 2][(current_x + next_x) // 2] = 0
            stack.append((next_x, next_y))
        else:
            stack.pop()

def update_maze():
    canvas.delete("all")
    cell_width = int(canvas.winfo_width() / maze_size)
    cell_height = int(canvas.winfo_height() / maze_size)
    for row in range(maze_size):
        for col in range(maze_size):
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            if maze[row][col] == 0:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black")
    red_droid_radius = min(cell_width, cell_height) // 2
    green_droid_radius = min(cell_width, cell_height) // 2
    red_droid_center_x = red_droid_x * cell_width + cell_width // 2
    red_droid_center_y = red_droid_y * cell_height + cell_height // 2
    green_droid_center_x = green_droid_x * cell_width + cell_width // 2
    green_droid_center_y = green_droid_y * cell_height + cell_height // 2
    canvas.create_oval(
        red_droid_center_x - red_droid_radius, red_droid_center_y - red_droid_radius,
        red_droid_center_x + red_droid_radius, red_droid_center_y + red_droid_radius,
        fill="red"
    )
    canvas.create_oval(
        green_droid_center_x - green_droid_radius, green_droid_center_y - green_droid_radius,
        green_droid_center_x + green_droid_radius, green_droid_center_y + green_droid_radius,
        fill="green"
    )

def start_movement():
    global red_droid_moving, green_droid_moving
    red_droid_moving = True
    green_droid_moving = True
    move_droids()

def stop_movement():
    global red_droid_moving, green_droid_moving
    red_droid_moving = False
    green_droid_moving = False

def bfs_search(start_x, start_y, target_x, target_y):
    # Inisialisasi visited dan queue
    visited = [[False] * maze_size for _ in range(maze_size)]
    queue = deque([(start_x, start_y, [])])

    # Penelusuran BFS
    while queue:
        x, y, path = queue.popleft()
        visited[y][x] = True

        # Cek apakah target ditemukan
        if x == target_x and y == target_y:
            return path

        # Cek langkah yang valid
        move_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in move_directions:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < maze_size and 0 <= new_y < maze_size and not visited[new_y][new_x] and maze[new_y][new_x] == 0:
                queue.append((new_x, new_y, path + [(new_x, new_y)]))

    return None

def move_droids():
    global red_droid_x, red_droid_y, green_droid_x, green_droid_y
    if red_droid_moving:
        # Gunakan BFS untuk mencari path menuju droid hijau
        path = bfs_search(red_droid_x, red_droid_y, green_droid_x, green_droid_y)
        if path:
            red_droid_x, red_droid_y = path[0]

        if red_droid_x == green_droid_x and red_droid_y == green_droid_y:
            canvas.create_text(
                canvas.winfo_width() // 2, canvas.winfo_height() // 2,
                text="Game Over", font=("ravie", 30), fill="red"
            )
            stop_movement()
            return  # Menghentikan pergerakan droid setelah game over

    if green_droid_moving:
        # Pilih langkah terjauh dari droid merah
        move_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        max_distance = -1
        target_move = None
        for direction in move_directions:
            new_x = green_droid_x + direction[0]
            new_y = green_droid_y + direction[1]
            if 0 <= new_x < maze_size and 0 <= new_y < maze_size and maze[new_y][new_x] == 0:
                distance = abs(new_x - red_droid_x) + abs(new_y - red_droid_y)
                if distance > max_distance:
                    max_distance = distance
                    target_move = (new_x, new_y)

        if target_move:
            green_droid_x, green_droid_y = target_move

    update_maze()

    if red_droid_moving or green_droid_moving:
        window.after(movement_speed, move_droids)


def start_movement():
    global red_droid_moving, green_droid_moving
    red_droid_moving = True
    green_droid_moving = True
    move_droids()



def randomize_droid_positions():
    global red_droid_x, red_droid_y, green_droid_x, green_droid_y
    # Acak posisi droid merah
    while True:
        red_droid_x = random.randint(0, maze_size - 1)
        red_droid_y = random.randint(0, maze_size - 1)
        if maze[red_droid_y][red_droid_x] == 0:
            break

    # Acak posisi droid hijau
    while True:
        green_droid_x = random.randint(0, maze_size - 1)
        green_droid_y = random.randint(0, maze_size - 1)
        if maze[green_droid_y][green_droid_x] == 0 and (green_droid_x != red_droid_x or green_droid_y != red_droid_y):
            break


# Fungsi untuk menghentikan pergerakan droid
def stop_movement():
    global red_droid_moving, red_droid_moving
    red_droid_moving = False
    green_droid_moving = False


def shuffle_maze():
    create_maze()
    update_maze()

window = tk.Tk()
window.title("Droid Chase")
canvas = tk.Canvas(window, width=600, height=600, bg="white")
canvas.pack()

create_maze()
update_maze()

button_frame = tk.Frame(window)
button_frame.pack(pady=10)
start_button = tk.Button(button_frame, text="Mulai", command=start_movement)
start_button.grid(row=0, column=0, padx=10)
stop_button = tk.Button(button_frame, text="Berhenti", command=stop_movement)
stop_button.grid(row=0, column=1, padx=10)
randomize_button = tk.Button(button_frame, text="Acak Droid", command=randomize_droid_positions)
randomize_button.grid(row=0, column=2, padx=10)
shuffle_button = tk.Button(button_frame, text="Acak Map", command=shuffle_maze)
shuffle_button.grid(row=0, column=3, padx=10)

window.mainloop()
