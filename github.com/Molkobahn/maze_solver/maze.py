from cell import Cell
import time
import random

class Maze():
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None,
            ):
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()


    def _create_cells(self):
        for i in range(self.num_cols):
            self._cells.append([])
            for j in range(self.num_rows):
                self._cells[i].append(Cell(self.win))
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)


    def _draw_cell(self, i, j):
        if self.win is None:
            return
        cell_x1 = self.x1 + (self.cell_size_x * i)
        cell_x2 = self.x1 + (self.cell_size_x * (i + 1))
        cell_y1 = self.y1 + (self.cell_size_y * j)
        cell_y2 = self.y1 + (self.cell_size_y * (j + 1))
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()


    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)


    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(len(self._cells)-1, len(self._cells[-1])-1)


    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True
        
        while True:
            to_visit = []
            
            # Checking all the adjacent cells
            # Check north
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i,j-1))
            #Check east
            if i < len(self._cells) - 1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            #Check south
            if j < len(self._cells[0]) - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))
            #Check west
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))

            if len(to_visit) == 0:
                if current._win:
                    current.draw(current._x1, current._y1, current._x2, current._y2)
                return
            
            # Pick a direction
            rand_index = random.randrange(len(to_visit))
            next_i, next_j = to_visit[rand_index]

            # Determine wich walls to break
            if next_i < i: # Moveing west
                current.has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif next_i > i: # Moving east
                current.has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif next_j < j: # Moveing north
                current.has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif next_j > j: #Moving south
                current.has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            
            # Recursively continue from next cell
            self._break_walls_r(next_i, next_j)
            
    
    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False


    def solve(self):
        return self.solve_r(i=0, j=0)
    

    def solve_r(self, i, j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True

        # Check if we are at the goal
        if current == self._cells[-1][-1]:
            return True
        
        # Check the directions
        # Check North
        if j > 0 and not current.has_top_wall and not self._cells[i][j-1].visited:
            current.draw_move(self._cells[i][j-1])
            if self.solve_r(i, j-1) == True:
                return True
            else:
                current.draw_move(self._cells[i][j-1], undo=True)
        # Check east
        if i < len(self._cells) - 1 and not current.has_right_wall and not self._cells[i+1][j].visited:
            current.draw_move(self._cells[i+1][j])
            if self.solve_r(i+1, j) == True:
                return True
            else:
                current.draw_move(self._cells[i+1][j], undo=True)
        #Check south
        if j < len(self._cells[0]) - 1 and not current.has_bottom_wall and not self._cells[i][j+1].visited:
            current.draw_move(self._cells[i][j+1])
            if self.solve_r(i, j+1) == True:
                return True
            else:
                current.draw_move(self._cells[i][j+1], undo=True)
        #Check west
        if i > 0 and not current.has_left_wall and not self._cells[i-1][j].visited:
            current.draw_move(self._cells[i-1][j])
            if self.solve_r(i-1, j) == True:
                return True
            else:
                current.draw_move(self._cells[i-1][j], undo=True)
        
        return False