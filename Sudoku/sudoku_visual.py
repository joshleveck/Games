import pygame as py
import webscraper
import backtracking

PASS = 0
# pygame init
WIDTH = 800
WIN = py.display.set_mode((WIDTH, WIDTH))
py.display.set_caption("Sudoku")
py.font.init()

# colours
SELECTED = (255, 254, 179)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# test board
SUDOKU = [
    [0, 0, 6, 0, 0, 0, 0, 0, 8],
    [0, 8, 9, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 6, 0, 1, 0],
    [0, 0, 0, 7, 3, 0, 0, 0, 0],
    [3, 9, 0, 2, 0, 0, 0, 0, 1],
    [4, 0, 0, 0, 0, 5, 0, 6, 0],
    [0, 0, 0, 0, 2, 0, 1, 7, 0],
    [0, 6, 2, 0, 4, 0, 0, 9, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0],
]
BOARD = webscraper.sudoku()
FONT = py.font.Font("FreeSansBold.ttf", 50)  # font


class Sq:
    def __init__(self, value, col, row, width):
        self.value = value
        self.col = col
        self.row = row
        self.width = width
        self.focus = False

    def draw(self, win):  # called every update; square draws itself
        if self.focus:  # if its selected
            py.draw.rect(
                win,
                SELECTED,
                (self.col * self.width, self.row * self.width, self.width, self.width),
            )
        else:
            py.draw.rect(
                win,
                WHITE,
                (self.col * self.width, self.row * self.width, self.width, self.width),
            )
        if self.value == 0:  # if its 0, leave
            return
        value = str(self.value)
        text = FONT.render(value, True, BLACK)
        text_rect = (
            text.get_rect(  # create a rectangle so that the text can be drawn in
                center=(
                    self.col * self.width + self.width / 2,
                    self.row * self.width + self.width / 2,
                )
            )
        )
        win.blit(text, text_rect)  # draw itself

    def set_value(self, value):
        self.value = value

    def selected(self):
        self.focus = True

    def clear(self):
        self.focus = False

    def num(self):
        return self.value


def get_clicked_pos(pos, rows, width):  # from mouse pos, get selected sq
    gap = width // rows
    y, x = pos

    col = y // gap
    row = x // gap

    return col, row


def make_grid(
    rows, width
):  # makes the sudoku grid, and saves the original so that it won't be altered
    grid = []
    gap = width // rows
    sudoku = BOARD
    original = []
    for i in range(rows):
        grid.append([])
        original.append([])
        for j in range(rows):
            value = sudoku[i][j]
            sq = Sq(value, j, i, gap)
            original[i].append(value)
            grid[i].append(sq)

    return grid, original


def draw_grid(win, rows, width):  # draws the lines on the grid
    gap = width // rows
    for i in range(rows):
        if i % 3 == 0:
            py.draw.line(win, BLACK, (0, i * gap), (width, i * gap), width=3)
        else:
            py.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        if j % 3 == 0:
            py.draw.line(win, BLACK, (j * gap, 0), (j * gap, width), width=3)
        else:
            py.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):  # tells all helper funcitons to draw themselves
    win.fill(WHITE)
    for row in grid:
        for sq in row:
            sq.draw(win)
    draw_grid(win, rows, width)
    py.display.update()


def current_grid(grid):
    curr = []
    for row in grid:
        row = []
        for sq in row:
            value = sq.value()
            row.append(value)
        curr.append(row)
    return curr


def solve(bo):
    find = backtracking.find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if backtracking.valid(bo, i, (row, col)):
            bo[row][col] = i
            WIN.fill(WHITE)
            draw_from_array(bo)
            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def draw_from_array(board):
    width = WIDTH // 9
    for i in range(9):
        for j in range(9):
            value = str(board[i][j])
            text = FONT.render(value, True, BLACK)
            text_rect = (
                text.get_rect(  # create a rectangle so that the text can be drawn in
                    center=(
                        j * width + width / 2,
                        i * width + width / 2,
                    )
                )
            )
            WIN.blit(text, text_rect)
    draw_grid(WIN, 9, WIDTH)
    py.display.update()


def assess(solve, org, win):
    width = WIDTH // 9
    for i in range(9):
        for j in range(9):
            if org[i][j].num() != 0:
                if solve[i][j] == org[i][j].num():
                    py.draw.rect(
                        win,
                        GREEN,
                        (j * width, i * width, width, width),
                    )
                else:
                    py.draw.rect(
                        win,
                        RED,
                        (j * width, i * width, width, width),
                    )
            else:
                py.draw.rect(
                    win,
                    GREEN,
                    (j * width, i * width, width, width),
                )
    draw_from_array(solve)


def main(win, width):
    ROWS = 9
    grid, original = make_grid(ROWS, width)

    run = True
    started = False  # algo started

    selected = None
    while run:
        if not started:
            draw(win, grid, ROWS, width)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

            if started:
                pass

            if py.mouse.get_pressed()[0]:  # LEFT
                pos = py.mouse.get_pos()
                col, row = get_clicked_pos(pos, ROWS, width)
                sq = grid[row][col]
                if sq in original:  # don't alter originals
                    pass
                else:
                    if selected != None:  # gets rid of bug
                        selected.clear()
                    selected = sq
                    selected.selected()

            elif py.mouse.get_pressed()[2]:  # RIGHT
                pos = py.mouse.get_pos()
                col, row = get_clicked_pos(pos, ROWS, width)
                sq = grid[row][col]
                if sq in original:  # same as left
                    pass
                else:
                    sq.set_value(0)

            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:  # starts solving algorithm
                    started = True
                    solve_grid = original
                    solve(solve_grid)
                    draw_from_array(solve_grid)
                    assess(solve_grid, grid, WIN)

                if event.key == py.K_r:  # resets all sqs but originals
                    started = False
                    for row in grid:
                        for sq in row:
                            if sq in original:
                                pass
                            else:
                                sq.set_value(0)

                if selected != None:  # changes value of selected sq
                    if event.key == py.K_0:
                        selected.set_value(0)
                        selected.clear()
                        selected = None
                    if event.key == py.K_1:
                        selected.set_value(1)
                        selected.clear()
                        selected = None
                    if event.key == py.K_2:
                        selected.set_value(2)
                        selected.clear()
                        selected = None
                    if event.key == py.K_3:
                        selected.set_value(3)
                        selected.clear()
                        selected = None
                    if event.key == py.K_4:
                        selected.set_value(4)
                        selected.clear()
                        selected = None
                    if event.key == py.K_5:
                        selected.set_value(5)
                        selected.clear()
                        selected = None
                    if event.key == py.K_6:
                        selected.set_value(6)
                        selected.clear()
                        selected = None
                    if event.key == py.K_7:
                        selected.set_value(7)
                        selected.clear()
                        selected = None
                    if event.key == py.K_8:
                        selected.set_value(8)
                        selected.clear()
                        selected = None
                    if event.key == py.K_9:
                        selected.set_value(9)
                        selected.clear()
                        selected = None
    py.quit()


main(WIN, WIDTH)