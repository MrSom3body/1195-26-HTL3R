__author__ = "Karun Sandhu"

import time


def load_maze(path):
    with open(path) as f:
        return [line.strip() for line in f]


def dfs(maze: list[str], start: tuple[int, int]) -> list[tuple[int, int]] | None:
    stack: list[tuple[tuple[int, int], list[tuple[int, int]]]] = [(start, [start])]
    visited: set[tuple[int, int]] = set()

    while stack:
        (x, y), path = stack.pop()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        if maze[y][x] == "A":
            return path

        for nx, ny in [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]:
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]):
                if maze[ny][nx] != "#":
                    stack.append(((nx, ny), path + [(nx, ny)]))

    return None


if __name__ == "__main__":
    maze_files = [
        ("L1", "./UE04_Labyrinth/l1.txt"),
        ("L2", "./UE04_Labyrinth/l2.txt"),
        ("L3", "./UE04_Labyrinth/l3.txt"),
    ]

    for label, path in maze_files:
        maze = load_maze(path)

        start = time.perf_counter()
        result = dfs(maze, (1, 1))  # or whatever your start coordinate is
        elapsed = time.perf_counter() - start

        print(
            f"DFS {label} found path of length {len(result) if result else 'None'} "
            f"in {elapsed:.6f} seconds"
        )
