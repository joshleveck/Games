import pygame as py
from game import check_legal, game_end, winner, get_legal_moves
import ai
from math import inf
import time

WIDTH = 1000
SQ = 8
COLOURS = {
    "bg": (15, 122, 43),
    "white": (245, 245, 245),
    "black": (38, 38, 38),
    "grid": (38, 38, 38),
}
R = (WIDTH // SQ) // 2 - 5
MAX_D = 8
WIN = py.display.set_mode((WIDTH, WIDTH))
py.init()
py.display.set_caption("Othello")


def debug_grid(circles):
    print("\n\n")
    for x in range(len(circles)):
        print(
            "{:<8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}".format(
                str(circles[0][x].player),
                str(circles[1][x].player),
                str(circles[2][x].player),
                str(circles[3][x].player),
                str(circles[4][x].player),
                str(circles[5][x].player),
                str(circles[6][x].player),
                str(circles[7][x].player),
            )
        )


class Circles:
    r = R
    width = WIDTH
    sq = SQ
    shift = (WIDTH // SQ) // 2
    white = COLOURS["white"]
    black = COLOURS["black"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player = None
        self.colour = None

    def set_player(self, player):
        self.player = player
        if player == 1:
            self.colour = self.black
        elif player == 2:
            self.colour = self.white
        else:
            self.colour = None

    def draw(self, win):
        py.draw.circle(
            win,
            self.colour,
            (
                self.x * self.width // self.sq + self.shift,
                self.y * self.width // self.sq + self.shift,
            ),
            self.r,
        )


def run_AI(circles, win, max_d):
    start = time.time()
    score, move = ai.maxTurn(circles, 0, -inf, inf, max_d)
    end = time.time()
    legal, flip = check_legal(circles[move[0]][move[1]], circles, False)
    if score == inf:
        eva = "White win"
    elif score == -inf:
        eva = "Black win"
    elif score == 0:
        eva = "Tie"
    else:
        eva = str(score)
    print("Best Move: {}, Evaluated Score: {}".format(move, eva))
    print("Evaluation time: {}s\n".format(round(end - start, 7)))
    for c in flip:
        c.set_player(2)
        c.draw(win)
        p1 = True


def get_coords(pos, width, sq):
    x = pos[0] // (width // sq)
    y = pos[1] // (width // sq)
    return x, y


def set_sqs(sq, width, win):
    circles = []
    for i in range(sq):
        col = []
        for j in range(sq):
            circle = Circles(i, j)
            col.append(circle)
            if (i, j) == ((sq - 2) / 2, (sq - 2) / 2) or (i, j) == (sq / 2, sq / 2):
                circle.set_player(2)
                circle.draw(win)
            elif (i, j) == ((sq - 2) / 2, sq / 2) or (i, j) == (sq / 2, (sq - 2) / 2):
                circle.set_player(1)
                circle.draw(win)
        circles.append(col)
    return circles


def set_grid(win, colour, sq, width):
    for i in range(sq - 1):
        py.draw.line(
            win, colour, (width // sq * (i + 1), 0), (width // sq * (i + 1), width)
        )  # across
        py.draw.line(
            win, colour, (0, width // sq * (i + 1)), (width, width // sq * (i + 1))
        )  # down


def main(win, width, sq, colours, max_d):
    clock = py.time.Clock()
    run = True
    win.fill(colours["bg"])
    set_grid(win, colours["grid"], sq, width)
    circles = set_sqs(sq, width, win)
    p1 = True
    while run:
        clock.tick(15)

        if not p1:
            run_AI(circles, win, max_d)
            p1 = True

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

            if py.mouse.get_pressed()[0]:
                pos = py.mouse.get_pos()
                x, y = get_coords(pos, width, sq)
                circle = circles[x][y]
                legal, flip = check_legal(circle, circles, p1)
                if legal:
                    for c in flip:
                        c.set_player(1)
                        c.draw(win)
                    p1 = False
        if p1:
            if len(get_legal_moves(circles, 1)) == 0:
                print("No moves for you, AI's turn again\n")
                p1 = False
        else:
            if len(get_legal_moves(circles, 2)) == 0:
                print("No moves for the AI, your turn again\n")
                p1 = True

        if game_end(circles):
            win = winner(circles)
            if win == 1:
                print("Winner is Black!")
            elif win == 2:
                print("Winner is White!")
            else:
                print("Draw!")
            run = False
        py.display.update()


main(WIN, WIDTH, SQ, COLOURS, MAX_D)
