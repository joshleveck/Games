DIR = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def debug_grid(circles):
    print("\n")
    for x in range(len(circles)):
        print(
            "{:<8s}{:>8s}{:>8s}{:>8s}".format(
                str(circles[0][x].player),
                str(circles[1][x].player),
                str(circles[2][x].player),
                str(circles[3][x].player),
                # str(circles[4][x].player),
                # str(circles[5][x].player),
                # str(circles[6][x].player),
                # str(circles[7][x].player),
            )
        )


def check_legal(circle, circles, p1):
    if circle.player != None:
        return False, None
    if p1:
        p = 1
    else:
        p = 2
    flip = []
    for d in DIR:
        pot_flip = []
        for i in range(len(circles)):
            if (
                d[0] * (i + 1) + circle.x > -1
                and d[0] * (i + 1) + circle.x < len(circles)
                and d[1] * (i + 1) + circle.y > -1
                and d[1] * (i + 1) + circle.y < len(circles)
            ):
                c = circles[d[0] * (i + 1) + circle.x][d[1] * (i + 1) + circle.y]
                if c.player == None:
                    break
                elif c.player == p:
                    flip += pot_flip
                    break
                else:
                    pot_flip.append(c)
            else:
                break
    if len(flip) > 0:
        flip.append(circle)
        return True, flip
    else:
        return False, None


def get_legal_moves(circles, player):
    if player == 1:
        p1 = True
    else:
        p1 = False

    moves = []
    for i in range(len(circles)):
        for j in range(len(circles)):
            circle = circles[i][j]
            if circle.player == None:
                outcome, _ = check_legal(circle, circles, p1)
                if outcome == True:
                    moves.append((i, j))
    return moves


def game_end(circles):
    moves1 = get_legal_moves(circles, 1)
    moves2 = get_legal_moves(circles, 2)
    if len(moves1) == 0 and len(moves2) == 0:
        return True
    return False


def score(circles):
    white = 0
    black = 0
    for i in range(len(circles)):
        for j in range(len(circles)):
            player = circles[i][j].player
            if player == 1:
                black += 1
            elif player == 2:
                white += 1
    return white - black


def winner(circles):
    white = 0
    black = 0
    for i in range(len(circles)):
        for j in range(len(circles)):
            player = circles[i][j].player
            if player == 1:
                black += 1
            elif player == 2:
                white += 1
    if black > white:
        return 1
    elif white > black:
        return 2
    else:
        return 0
