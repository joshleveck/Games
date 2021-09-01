import game
from math import inf

# AI is ALWAYS white
def maxTurn(circles, depth, alpha, beta, max_depth):  # returns score,move
    if game.game_end(circles):
        score = game.score(circles)
        if score > 0:
            return (inf, None)
        elif score == 0:
            return (0, None)
        else:
            return (-inf, None)

    legal_moves = game.get_legal_moves(circles, 2)  # returns (i,j)
    if depth >= max_depth or len(legal_moves) == 0:
        return (game.score(circles), None)

    maxim = (-inf, legal_moves[0])
    for x, y in legal_moves:
        circles[x][y].set_player(1)
        score, move = minTurn(circles, depth + 1, alpha, beta, max_depth)

        if score > maxim[0]:
            maxim = (score, (x, y))

        if score >= beta:
            circles[x][y].set_player(None)
            maxim = (score, move)
            return maxim

        if score > alpha:
            alpha = score

        circles[x][y].set_player(None)

    return maxim


def minTurn(circles, depth, alpha, beta, max_depth):  # returns score,move
    if game.game_end(circles):
        score = game.score(circles)
        if score > 0:
            return (inf, None)
        elif score == 0:
            return (0, None)
        else:
            return (-inf, None)

    legal_moves = game.get_legal_moves(circles, 1)  # returns (i,j)
    if depth >= max_depth or len(legal_moves) == 0:
        return (game.score(circles), None)

    minim = (inf, legal_moves[0])
    for x, y in legal_moves:

        circles[x][y].set_player(2)
        score, move = maxTurn(circles, depth + 1, alpha, beta, max_depth)

        if score < minim[0]:
            minim = (score, (x, y))

        if score <= alpha:
            circles[x][y].set_player(None)
            minim = (score, move)
            return minim

        if score < beta:
            beta = score

        circles[x][y].set_player(None)

    return minim
