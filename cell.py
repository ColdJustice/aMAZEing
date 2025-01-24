from graphics import Line, Point


class Cell():
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._window = window

    def __repr__(self):
        return f"({self._x1}, {self._y1}), ({self._x2}, {self._y2}) left: {self.has_left_wall} right:{self.has_right_wall} top:{self.has_top_wall} bottom:{self.has_bottom_wall}"

    def draw(self, x1, y1, x2, y2, fill_color="black"):
        if self._window is None:
            return
        
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        missing_wall_color = "#f0f0f0"


        self._window.draw_line(Line(Point(x1, y1), Point(x1, y2)), fill_color if self.has_left_wall   else missing_wall_color)
        self._window.draw_line(Line(Point(x2, y1), Point(x2, y2)), fill_color if self.has_right_wall  else missing_wall_color)
        self._window.draw_line(Line(Point(x1, y1), Point(x2, y1)), fill_color if self.has_top_wall    else missing_wall_color)
        self._window.draw_line(Line(Point(x1, y2), Point(x2, y2)), fill_color if self.has_bottom_wall else missing_wall_color)


    def draw_move(self, to_cell, undo=False):
        if self._window is None:
            return
        
        color = "red" if undo else "blue"
        p1 = self.get_center()
        p2 = to_cell.get_center()
        line = Line(p1, p2)
        self._window.draw_line(line, color)

    def get_center(self):
        return Point(self.center_value(self._x1, self._x2), self.center_value(self._y1, self._y2))
    
    def center_value(self, a, b):
        return abs(b - a) // 2 + min(a, b)

    def __repr__(self):
        return f"({self._x1},{self._y1})/({self._x2},{self._y2})"