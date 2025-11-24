package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

type Position struct {
	X int
	Y int
}

type Maze struct {
	start Position
	grid  []string
}

func bfs(maze Maze) []Position {
	visited := make(map[Position]bool)
	parent := make(map[Position]Position)

	queue := make([]Position, 0, 1024)
	queue = append(queue, maze.start)
	visited[maze.start] = true

	directions := []Position{
		{1, 0},
		{-1, 0},
		{0, 1},
		{0, -1},
	}

	var exit Position
	found := false
	head := 0

	for head < len(queue) {
		curr := queue[head]
		head++

		if maze.grid[curr.Y][curr.X] == 'A' {
			exit = curr
			found = true
			break
		}

		for _, d := range directions {
			nx, ny := curr.X+d.X, curr.Y+d.Y
			if ny < 0 || ny >= len(maze.grid) || nx < 0 || nx >= len(maze.grid[0]) {
				continue
			}
			if maze.grid[ny][nx] == '#' {
				continue
			}

			neighbor := Position{nx, ny}
			if visited[neighbor] {
				continue
			}

			visited[neighbor] = true
			parent[neighbor] = curr
			queue = append(queue, neighbor)
		}
	}

	if !found {
		return nil
	}

	path := []Position{}
	for curr := exit; curr != maze.start; curr = parent[curr] {
		path = append(path, curr)
	}
	path = append(path, maze.start)

	for i, j := 0, len(path)-1; i < j; i, j = i+1, j-1 {
		path[i], path[j] = path[j], path[i]
	}

	return path
}

func loadMaze(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func markMap(maze []string, path []Position) []string {
	mazeCopy := make([][]rune, len(maze))
	for i := range maze {
		mazeCopy[i] = []rune(maze[i])
	}

	for _, pos := range path {
		if mazeCopy[pos.Y][pos.X] != 'S' && mazeCopy[pos.Y][pos.X] != 'A' {
			mazeCopy[pos.Y][pos.X] = '.'
		}
	}

	result := make([]string, len(mazeCopy))
	for i, row := range mazeCopy {
		result[i] = string(row)
	}
	return result
}

func main() {
	mazeFiles := []string{"./UE04_Labyrinth/l1.txt", "./UE04_Labyrinth/l2.txt", "./UE04_Labyrinth/l3.txt"}

	for i, path := range mazeFiles {
		grid, err := loadMaze(path)
		if err != nil {
			panic(err)
		}

		start := time.Now()
		result := bfs(Maze{start: Position{X: 1, Y: 1}, grid: grid})
		elapsed := time.Since(start)

		fmt.Printf("BFS L%d found path of length %d in %s\n", i+1, len(result), elapsed)

		if i == 1 && result != nil {
			for _, line := range markMap(grid, result) {
				fmt.Println(line)
			}
		}
	}
}
