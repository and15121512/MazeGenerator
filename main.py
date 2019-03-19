import random
from maze_class import Maze, Cell, Wall

# откомментить для фиксации выдаваемого лабиринта
#random.seed(42)


def generator(maze):
    """
    Генерирует лабиринт с помощью обхода в глубину из полностью заполненного стенами
    лабиринта maze
    :param maze: объект класса Maze из maze_class (полный лабиринт)
    :return: nothing
    """
    called_cells = list()  # stack of recursion

    current = maze.start_cell  # it`s cell
    visited = [maze.start_cell]

    while not maze.is_all_visited(len(visited)):

        neighbours = maze.get_unvis_neighbours(current, visited)

        if len(neighbours) > 0:
            called_cells.append(current)
            next_index = random.randint(0, max(len(neighbours) - 1, -1))
            maze.delete_wall(current, neighbours[next_index])
            current = neighbours[next_index]
            visited.append(neighbours[next_index])
        elif len(called_cells) > 0:
            current = called_cells.pop()


def find_path(maze):
    """
    По данному лабиринту maze находит в нём путь бэктрекингом (аналогично DFS)
    :param maze: объект класса Maze из maze_class (сгенерированный лабиринт)
    :return: путь (list) path из всех клеток (и проходов)
    """
    called_cells = list()  # stack of recursion
    path = list()

    current = maze.start_cell
    visited = [maze.start_cell]

    while not maze.is_all_visited(len(visited)):

        neighbours = maze.get_unvis_neighbours(current, visited)
        need_to_pop = list()
        for i in range(len(neighbours)):
            if maze.has_wall(current, neighbours[i]):
                need_to_pop.append(neighbours[i])

        for elem in need_to_pop:
            neighbours.remove(elem)

        if len(neighbours) > 0:
            called_cells.append(current)

            next_index = random.randint(0, max(len(neighbours) - 1, -1))
            path.append(maze.get_wall(current, neighbours[next_index]))
            path.append(current)

            if maze.is_exit(neighbours[next_index]):
                called_cells.append(neighbours[next_index])
                path.append(maze.get_wall(current, neighbours[next_index]))
                path.append(neighbours[next_index])
                return path

            current = neighbours[next_index]
            visited.append(neighbours[next_index])
        elif len(called_cells) > 0:
            current = called_cells.pop()
            path.pop()
            path.pop()
        else:
            print('no_way_out')


def min_span_tree_generator(maze):
    """
    Генерирует лабиринт с помощью мин. остовного дерева из полностью заполненного стенами
    лабиринта maze
    :param maze: объект класса Maze из maze_class (полный лабиринт)
    :return: nothing
    """
    walls_list = list()

    visited = [maze.start_cell]
    start_neighbours = maze.get_neighbours(maze.start_cell)
    for neigh in start_neighbours:
        walls_list.append(Wall(maze.start_cell, neigh))

    while len(walls_list) > 0:
        current_wall_index = random.randint(0, len(walls_list) - 1)
        current_wall = walls_list[current_wall_index]
        if current_wall.first_cell not in visited:
            maze.delete_wall(current_wall.first_cell, current_wall.second_cell)
            visited.append(current_wall.first_cell)

            next_neighbours = maze.get_neighbours(current_wall.first_cell)
            for neigh in next_neighbours:
                walls_list.append(Wall(current_wall.first_cell, neigh))
        elif current_wall.second_cell not in visited:
            maze.delete_wall(current_wall.first_cell, current_wall.second_cell)
            visited.append(current_wall.second_cell)

            next_neighbours = maze.get_neighbours(current_wall.second_cell)
            for neigh in next_neighbours:
                walls_list.append(Wall(current_wall.second_cell, neigh))

        walls_list.pop(current_wall_index)

######################################################


def create_new_maze():
    """
    Запрашивает необходимые параметры у пользователя (размеры, начало и конец пути,
    метод генерации) и генерирует по ним лабиринт
    :return: объект класса Maze из main_class (сгенерированный лабиринт)
    """
    while True:
        print('Enter width and height: ')
        width, height = int(input()), int(input())
        if not (width > 2 and height > 2):
            print('Width and height must be > 2')
            continue
        print('Enter start cell(x, y): ')
        tmp = input()
        start_cell = Cell(input(), tmp)
        if start_cell.x >= height or start_cell.y >= width:
            print('Start_cell.x must be < height and Start_cell.y must be < width ')
            continue
        print('Enter exit cell: ')
        tmp = input()
        exit_cell = Cell(input(), tmp)
        if exit_cell.x >= height or exit_cell.y >= width:
            print('Exit_cell.x must be < height and Exit_cell.y must be < width ')
            continue
        curr_maze = Maze(width, height, start_cell, exit_cell)
        print('Print alghorithm (DFS or MST): ')
        com1 = input().lower()
        if com1 == 'dfs':
            generator(curr_maze)
        elif com1 == 'mst':
            min_span_tree_generator(curr_maze)
        print('Your maze: ')
        curr_maze.print_maze()
        return curr_maze


def get_maze_from_file(file_name):
    """
    Считывает лабиринт из файла
    :param file_name: открытый файл (объект)
    :return: объект класса Maze (считанный лабиринт)
    """
    maze = list()
    for line in file_name:
        maze_line = list()
        for elem in line:
            if elem == '#':
                maze_line.append(False)
            elif elem == '+':
                maze_line.append(True)
        maze.append(list(maze_line))
    return maze


def put_maze_in_file(maze, start_c, exit_c, file_name):
    """
    Сохраняет лабиринт в файл
    :param maze: объект класса Maze (сохраняемый лабиринт)
    :param start_c: объект класса Cell из maze_class (стартовая клетка - вход в лабиринт)
    :param exit_c: объект класса Cell из maze_class (конечная клетка - выход из лабиринта)
    :param file_name: открытый файл (объект)
    :return: nothing
    """
    file_name.write(str(start_c.x) + '\n' + str(start_c.y) + '\n')
    file_name.write(str(exit_c.x) + '\n' + str(exit_c.y) + '\n')
    firstly = True
    for line in maze:
        line_to_print = []
        for elem in line:
            if not elem:
                line_to_print.append('#')
            else:
                line_to_print.append('+')
        if not firstly:
            file_name.write('\n' + ''.join(line_to_print))
        else:
            file_name.write(''.join(line_to_print))
            firstly = False


def reading_commands():
    """
    Взимодействие с пользователем: считывание команд
    """
    curr_maze = Maze()
    is_maze_created = False

    while True:
        print('Please, enter your command: ')
        command = input().lower()
        if command == 'exit':
            print('Are you sure want to quit?')
            com1 = input().lower()
            if com1 == 'yes':
                break
            elif com1 == 'no':
                pass
            else:
                print('Unexpected command')
                continue

        elif command == 'new maze':
            curr_maze = create_new_maze()
            is_maze_created = True

        elif command == 'solve':
            if not is_maze_created:
                print('Maze must be created')
                continue
            path = find_path(curr_maze)
            if path is None:
                print('Start-cell and end-cell must be different (on 2 points or more)')
            else:
                curr_maze.print_path(path)

        elif command == 'load':
            print('Enter file name: ')
            file_with_maze = None
            is_correct_file = False
            while not is_correct_file:
                try:
                    file_name = input()
                    file_with_maze = open(file_name, 'r')
                    is_correct_file = True
                except FileNotFoundError:
                    print('Can`t find this file. Please, enter it`s name again.')
            start_c = Cell(int(file_with_maze.readline().strip()), int(file_with_maze.readline().strip()))
            exit_c = Cell(int(file_with_maze.readline().strip()), int(file_with_maze.readline().strip()))
            curr_maze.set_maze(get_maze_from_file(file_with_maze), start_c, exit_c)
            curr_maze.print_maze()
            file_with_maze.close()
            is_maze_created = True

        elif command == 'save':
            if not is_maze_created:
                print('You should create new maze or load it first!')
            else:
                print('Enter file name: ')
                file_name = input()
                file_to_put = open(file_name, 'w', encoding='utf-8')
                put_maze_in_file(curr_maze.get_maze(), curr_maze.get_start(), curr_maze.get_exit(), file_to_put)
                file_to_put.close()

        elif command == 'print':
            if not is_maze_created:
                print('You should create new maze or load it first!')
            curr_maze.print_maze()


reading_commands()
