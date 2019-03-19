class Cell:
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __init__(self, x_, y_):
        self.x = int(x_)
        self.y = int(y_)


class Wall:
    def __eq__(self, other):
        return self.first_cell == other.first_cell and self.second_cell == other.second_cell

    def __init__(self, first_cell_, second_cell_):
        self.first_cell = first_cell_
        self.second_cell = second_cell_


class Maze:
    width = 0
    height = 0
    start_cell = Cell(1, 1)
    exit_cell = Cell(1, 1)
    maze = list()  # True - wall, False - path

    def __init__(self, width_=-1, height_=-1, start_cell_=Cell(1, 1), exit_cell_=Cell(1, 1)):
        self.free_count = 0
        if width_ == -1 or height_ == -1:
            self.width = width_
            self.height = height_
            self.maze = []
            return
        self.width = width_ - 1 + (width_ & 1)
        self.height = height_ - 1 + (height_ & 1)
        if self.width < width_ and start_cell_.y >= self.width - 1:
            start_cell_.y -= 2
        if self.height < height_ and start_cell_.x >= self.height - 1:
            start_cell_.x -= 2
        if self.width < width_ and exit_cell_.y >= self.width - 1:
            exit_cell_.y -= 2
        if self.height < height_ and exit_cell_.x >= self.height - 1:
            exit_cell_.x -= 2

        self.start_cell = Cell((start_cell_.x >> 1) << 1 | 1, (start_cell_.y >> 1) << 1 | 1)
        self.exit_cell = Cell((exit_cell_.x >> 1) << 1 | 1, (exit_cell_.y >> 1) << 1 | 1)
        self.maze = [[True for j in range(self.width)] for i in range(self.height)]

        for j in range(self.height):
            for i in range(self.width):
                if j % 2 != 0 and i % 2 != 0 and j < self.height-1 and i < self.width-1:
                    self.maze[j][i] = False  # cell
                    self.free_count += 1
                else:
                    self.maze[j][i] = True  # wall

    def get_neighbours(self, cell):
        neighbours = []
        cells = list()
        cells.append((cell.x + 2, cell.y))
        cells.append((cell.x, cell.y + 2))
        cells.append((cell.x - 2, cell.y))
        cells.append((cell.x, cell.y - 2))

        for curr in cells:
            if (curr[0] > 0 and curr[0] < self.height) and (curr[1] > 0 and curr[1] < self.width):
                if not self.maze[curr[0]][curr[1]]:
                    neighbours.append(Cell(curr[0], curr[1]))
        return neighbours

    def get_unvis_neighbours(self, cell, visited):
        neighbours = self.get_neighbours(cell)
        need_to_remove = list()
        for neigh in neighbours:
            if neigh in visited:
                need_to_remove.append(neigh)

        for neigh in need_to_remove:
            neighbours.remove(neigh)

        return neighbours

    def delete_wall(self, first_cell, second_cell):
        self.maze[(first_cell.x + second_cell.x) >> 1][(first_cell.y + second_cell.y) >> 1] = False

    def has_wall(self, first_cell, second_cell):
        return self.maze[(first_cell.x + second_cell.x) >> 1][(first_cell.y + second_cell.y) >> 1]

    def get_wall(self, first_cell, second_cell):
        return Cell((first_cell.x + second_cell.x) >> 1, (first_cell.y + second_cell.y) >> 1)

    def is_all_visited(self, visited_count):
        return visited_count == self.free_count

    def is_exit(self, cell):
        return cell == self.exit_cell

    def print_maze(self):
        for line in self.maze:
            line_to_print = []
            for elem in line:
                if not elem:
                    line_to_print.append('◻')
                else:
                    line_to_print.append('◼')
            print(''.join(line_to_print))

    def print_path(self, path):
        for j in range(len(self.maze)):
            line_to_print = []
            for i in range(len(self.maze[j])):
                if not self.maze[j][i]:
                    if Cell(j, i) == path[1]:
                        line_to_print.append('▽')
                    elif Cell(j, i) == path[len(path) - 1]:
                        line_to_print.append('☒')
                    elif Cell(j, i) in path:
                        line_to_print.append('◈')
                    else:
                        line_to_print.append('◻')
                else:
                    line_to_print.append('◼')
            print(''.join(line_to_print))

    def set_maze(self, maze_matrix, start_c, exit_c):
        maze_copy = list()
        for line in maze_matrix:
            maze_copy.append(list(line))
        self.maze = maze_copy
        self.width = len(maze_matrix[0])
        self.height = len(maze_matrix)
        self.start_cell = Cell(start_c.x, start_c.y)
        self.exit_cell = Cell(exit_c.x, exit_c.y)

    def get_maze(self):
        maze_copy = list()
        for line in self.maze:
            maze_copy.append(list(line))
        return maze_copy

    def get_start(self):
        return Cell(self.start_cell.x, self.start_cell.y)

    def get_exit(self):
        return Cell(self.exit_cell.x, self.exit_cell.y)
