import random
import time

from direction import Direction
from graphics import Window
from cell import Cell


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._window = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def solve(self):
        return self._solve_r(0, 0)
    

    def _solve_r(self, i, j):
        self._animate()
        cell = self._cells[i][j]
        cell.visited = True
        if i + 1 == self._num_cols and j + 1 == self._num_rows:
            return True
        
        # Left
        if i > 0 and not cell.has_left_wall and not self._cells[i - 1][j].visited:
            cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            cell.draw_move(self._cells[i - 1][j], undo=True)

        # Right
        if i + 1 < self._num_cols and not cell.has_right_wall and not self._cells[i + 1][j].visited:
            cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            cell.draw_move(self._cells[i + 1][j], undo=True)

        # Above
        if j > 0 and not cell.has_top_wall and not self._cells[i][j - 1].visited:
            cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            cell.draw_move(self._cells[i][j - 1], undo=True)

        # Below
        if j + 1 <  self._num_rows and not cell.has_bottom_wall and not self._cells[i][j + 1].visited:
            cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            cell.draw_move(self._cells[i][j + 1], undo=True)

        return False

    
    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                column.append(Cell(self._window))
            self._cells.append(column)
        
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        

    def _draw_cell(self, i, j):
        if self._window is None:
            return
        
        x1 = self.x1 + (i * self._cell_size_x)
        y1 = self.y1 + (j * self._cell_size_y)
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    
    def _animate(self):
        if self._window is None:
            return
        
        self._window.redraw()
        time.sleep(0.02)


    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)


    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            if i - 1 >= 0: # Check cell to the left
                self.__add_unvisited_neighbor(i - 1, j, to_visit, Direction.LEFT)
            if i + 1 < self._num_cols: # Check cell to the right
                self.__add_unvisited_neighbor(i + 1, j, to_visit, Direction.RIGHT)
            if j - 1 >= 0: # Check cell above
                self.__add_unvisited_neighbor(i, j - 1, to_visit, Direction.ABOVE)
            if j + 1 < self._num_rows: # Check cell below
                self.__add_unvisited_neighbor(i, j + 1, to_visit, Direction.BELOW)
            
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            
            next_neighbor = random.randrange(len(to_visit))
            x, y, neighbor_cell, direction = to_visit[next_neighbor]
            self.__break_common_wall(self._cells[i][j], neighbor_cell, direction)

            self._break_walls_r(x, y)


    def __add_unvisited_neighbor(self, i, j, to_visit, direction):
        if not self._cells[i][j].visited:
            to_visit.append((i, j, self._cells[i][j], direction))


    def __break_common_wall(self, cell, neighbor, direction):
        match direction:
            case Direction.LEFT:
                cell.has_left_wall = False
                neighbor.has_right_wall = False
                return
            case Direction.RIGHT:
                cell.has_right_wall = False
                neighbor.has_left_wall = False
                return
            case Direction.ABOVE:
                cell.has_top_wall = False
                neighbor.has_bottom_wall = False
                return
            case Direction.BELOW:
                cell.has_bottom_wall = False
                neighbor.has_top_wall = False
                return
            

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
