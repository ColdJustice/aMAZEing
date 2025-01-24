from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = title
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")


    def close(self):
        self.__running = False


    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)


###############################################################################

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

###############################################################################

class Line():
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2


    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y,
            self.p2.x, self.p2.y,
            fill = fill_color,
            width = 2
        )

    def __repr__(self):
        return f"{self.p1} - {self.p2}"


###############################################################################



