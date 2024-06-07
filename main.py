from maze.fixed_maze import fixed_maze
from maze.plot_maze import plot_maze, move_car_along_path
from maze.bfs import bfs

if __name__ == "__main__":
    maze, start, end = fixed_maze()
    path = bfs(maze, start, end)
    plot_maze(maze, start, end, path)
    move_car_along_path(maze, path)
