from collections import deque

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

    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path
