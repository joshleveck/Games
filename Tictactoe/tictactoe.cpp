#include <iostream>
#include <vector>
#include <string>

class Game
{
private:
    bool p1_turn = true;
    std::vector<std::vector<int>> board = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};

public:
    std::vector<std::vector<int>> get_board()
    {
        return this->board;
    }

    std::string players_turn()
    {
        if (this->p1_turn)
        {
            return "Player 1";
        }
        else
        {
            return "Player 2";
        }
    }

    bool play_move(int square)
    {
        int x = square % 3;
        int y = square / 3;
        if (this->board[y][x] != 0)
        {
            return false;
        }

        if (this->p1_turn)
        {
            this->board[y][x] = 1;
        }
        else
        {
            this->board[y][x] = 2;
        }

        this->p1_turn = (this->p1_turn) ? false : true;
        return true;
    }

    int check_win()
    {
        //verticals
        for (int i = 0; i < 3; i++)
        {
            int vert_check_player = this->board[i][0];
            if (vert_check_player == 0)
            {
                continue;
            }

            for (int j = 1; j < 3; j++)
            {
                if (this->board[i][j] != vert_check_player)
                {
                    break;
                }
                if (j == 2)
                {
                    return vert_check_player;
                }
            }
        }
        //horizontals
        for (int i = 0; i < 3; i++)
        {
            int horz_check_player = this->board[0][i];
            if (horz_check_player == 0)
            {
                continue;
            }

            for (int j = 1; j < 3; j++)
            {
                if (this->board[j][i] != horz_check_player)
                {
                    break;
                }
                if (j == 2)
                {
                    return horz_check_player;
                }
            }
        }
        //diagonals
        int diag_check_player = this->board[0][0];
        if (diag_check_player != 0)
        {
            for (int i = 1; i < 3; i++)
            {
                if (this->board[i][i] != diag_check_player)
                {
                    break;
                }
                if (i == 2)
                {
                    return diag_check_player;
                }
            }
        }

        diag_check_player = this->board[2][0];
        if (diag_check_player != 0)
        {
            for (int i = 1; i < 3; i++)
            {
                if (this->board[2 - i][i] != diag_check_player)
                {
                    break;
                }
                if (i == 2)
                {
                    return diag_check_player;
                }
            }
        }
        return 0;
    }

    Game(){};
};

void print_board(std::vector<std::vector<int>> board)
{
    for (int i = 0; i < 3; i++)
    {
        if (i != 0)
        {
            std::cout << "----------\n";
        }
        std::string one = (board[i][0] == 0) ? " " : ((board[i][0] == 1) ? "X" : "O");
        std::string two = (board[i][1] == 0) ? " " : ((board[i][1] == 1) ? "X" : "O");
        std::string three = (board[i][2] == 0) ? " " : ((board[i][2] == 1) ? "X" : "O");

        std::cout << one << " | " << two << " | " << three << "\n";
    }
}

void print_template_board()
{
    std::vector<std::vector<int>> template_board = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    for (int i = 0; i < 3; i++)
    {
        if (i != 0)
        {
            std::cout << "----------\n";
        }

        std::cout << template_board[i][0] << " | " << template_board[i][1] << " | " << template_board[i][2] << "\n";
    }
}

int main()
{
    std::cout << "\nEach square is a number\nType that number to mark your square\n";
    print_template_board();

    Game active;
    while (true)
    {
        int move;
        std::cout << "It is " << active.players_turn() << "'s turn\nMove: ";

        while (true)
        {
            std::cin >> move;
            bool move_legal = active.play_move(move - 1);
            if (move_legal)
            {
                break;
            }
            else
            {
                std::cout << "Someone's already played there!\nMove: ";
            }
        }

        print_board(active.get_board());

        int win = active.check_win();
        if (win == 1)
        {
            std::cout << "Player 1 has won!";
            return 0;
        }
        else if (win == 2)
        {
            std::cout << "Player 2 has won!";
            return 0;
        }
    }
    return 0;
}
