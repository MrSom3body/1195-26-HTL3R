__author__ = "Karun Sandhu"

import time
from collections import deque


def dfs(maze: list[str], start: tuple[int, int]) -> list[tuple[int, int]] | None:
    stack: deque[tuple[tuple[int, int], list[tuple[int, int]]]] = deque(
        [(start, [start])]
    )
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


def bfs(maze: list[str], start: tuple[int, int]) -> list[tuple[int, int]] | None:
    queue: deque[tuple[tuple[int, int], list[tuple[int, int]]]] = deque(
        [(start, [start])]
    )
    visited: set[tuple[int, int]] = set()

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for nx, ny in [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]:
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]):
                if maze[ny][nx] != "#":
                    if maze[ny][nx] == "A":
                        return path + [(nx, ny)]
                    queue.append(((nx, ny), path + [(nx, ny)]))

    return None


def load_maze(path):
    with open(path) as f:
        return [line.strip() for line in f]


def mark_map(maze: list[str], path: list[tuple[int, int]]) -> list[str]:
    maze_copy = [list(row) for row in maze]
    for x, y in path:
        if maze_copy[y][x] not in ("S", "A"):
            maze_copy[y][x] = "."
    return ["".join(row) for row in maze_copy]


if __name__ == "__main__":
    maze_files = [
        ("L1", "./UE04_Labyrinth/l1.txt"),
        ("L2", "./UE04_Labyrinth/l2.txt"),
        ("L3", "./UE04_Labyrinth/l3.txt"),
    ]

    for label, path in maze_files:
        maze = load_maze(path)

        start = time.perf_counter()
        dfs_result = dfs(maze, (1, 1))  # or whatever your start coordinate is
        elapsed = time.perf_counter() - start

        if label == "L2" and dfs_result is not None:
            print("\n".join(mark_map(maze, dfs_result)))

        print(
            f"DFS {label} found path of length {len(dfs_result) if dfs_result else 'None'} "
            f"in {elapsed:.6f} seconds"
        )

        start = time.perf_counter()
        bfs_result = bfs(maze, (1, 1))  # or whatever your start coordinate is
        elapsed = time.perf_counter() - start

        if label == "L2" and bfs_result is not None:
            print("\n".join(mark_map(maze, bfs_result)))

        print(
            f"BFS {label} found path of length {len(bfs_result) if bfs_result else 'None'} "
            f"in {elapsed:.6f} seconds"
        )
