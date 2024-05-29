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

def plot_maze(grid, start, end, path):
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary')

    # Вибираємо координати для прямокутника (машинки) на старті
    x, y = start
    rect = Rectangle((y - 0.3, x - 0.3), 0.5, 0.7, facecolor='gray', edgecolor='black')
    plt.gca().add_patch(rect)

    # Позначаємо фініш
    plt.scatter([end[1]], [end[0]], c='red', s=200, label='End')

    # Позначаємо шлях
    for point in path:
        plt.scatter([point[1]], [point[0]], c='blue', s=50)

    plt.legend()
    plt.xticks([]), plt.yticks([])
    plt.show()

def bfs(maze, start, end):
    queue = deque([start])
    visited = set()
    parent = {}

    while queue:
        current = queue.popleft()
        if current == end:
            break

        row, col = current
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if 0 <= n_row < len(maze) and 0 <= n_col < len(maze[0]) and maze[n_row][n_col] == 0 and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    # Відновлюємо шлях з кінця до початку
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path

def move_car_along_path(grid, path):
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary')

    x, y = path[0]  # Початкова позиція машинки

    # Вибираємо координати для машинки на початку
    rect = Rectangle((y - 0.3, x - 0.3), 0.5, 0.7, facecolor='gray', edgecolor='black')
    plt.gca().add_patch(rect)

    # Відтворюємо рух машинки
    for i in range(1, len(path)):
        x_prev, y_prev = path[i - 1]
        x_next, y_next = path[i]

        # Визначаємо відстань між поточною та наступною позиціями
        dx = x_next - x_prev
        dy = y_next - y_prev

        # Рухаємо машинку на наступну позицію
        if abs(dx) == 1 and abs(dy) == 1:  # Діагональний рух
            x += dx
            y += dy
        elif dx == 1:  # Рух вниз
            x += dx
        elif dx == -1:  # Рух вгору
            x += dx
        elif dy == 1:  # Рух вправо
            y += dy
        elif dy == -1:  # Рух вліво
            y += dy

        # Оновлюємо відображення машинки
        rect.set_xy((y - 0.3, x - 0.3))
        plt.draw()
        plt.pause(0.2)  # Затримка для кращого візуального ефекту

    plt.show()

if __name__ == "__main__":
    maze, start, end = fixed_maze()
    path = bfs(maze, start, end)
    plot_maze(maze, start, end, path)  # Відобразити лабіринт з машинкою та шляхом
    move_car_along_path(maze, path)  # Рух машинки вздовж шляху
