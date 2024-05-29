import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import deque

def fixed_maze():
    # Статичний лабіринт 21x21
    maze = np.array([
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
    ])
    start = (0, 1)  # координати старту
    end = (20, 19)  # координати фінішу
    return maze, start, end

def bfs(maze, start, end):
    queue = deque([start])  # Створюємо чергу для BFS з початковою позицією
    visited = set()  # Зберігатиме відвідані клітинки
    parent = {}  # Зберігатиме інформацію про батьківські клітинки для відновлення шляху

    while queue:
        current_cell = queue.popleft()
        if current_cell == end:
            break  # Якщо досягли кінця, виходимо з циклу

        row, col = current_cell
        neighbors = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]  # Визначаємо сусідні клітинки

        for neighbor in neighbors:
            if neighbor not in visited and maze[neighbor[0]][neighbor[1]] == 0:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current_cell  # Запам'ятовуємо батьківську клітинку

    # Відновлюємо шлях з кінця до початку
    path = []
    while current_cell != start:
        path.append(current_cell)
        current_cell = parent[current_cell]
    path.append(start)
    path.reverse()

    return path

def plot_maze_with_path(grid, start, end, path):
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary')

    # Додаємо прямокутник (машинку) на старті
    x, y = start
    rect = Rectangle((y - 0.3, x - 0.3), 0.5, 0.7, facecolor='gray', edgecolor='black')
    plt.gca().add_patch(rect)

    # Позначаємо фініш
    plt.scatter([end[1]], [end[0]], c='red', s=200, label='End')

    # Відображаємо шлях
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, linewidth=5, color='blue', label='Path')

    plt.legend()
    plt.xticks([]), plt.yticks([])
    plt.show()

if __name__ == "__main__":
    maze, start, end = fixed_maze()
    path = bfs(maze, start, end)
    plot_maze_with_path(maze, start, end, path)
