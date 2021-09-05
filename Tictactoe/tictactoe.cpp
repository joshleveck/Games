#include <iostream>
#include <vector>
#include <string>
#include <tuple>

void print_board(std::vector<std::vector<int>>);
int end_of_game(std::vector<std::vector<int>>);
std::vector<std::vector<int>> play_move(int, std::vector<std::vector<int>>, bool);
bool legal_move(int, std::vector<std::vector<int>>);
int end_of_game(std::vector<std::vector<int>>);
std::vector<std::vector<int>> reverse_move(int, std::vector<std::vector<int>>);

class AI
{
public:
    //return: (move, predicted value)
    std::tuple<int, int> max(std::vector<std::vector<int>> board)
    {
        int result = end_of_game(board);
        if (result == 1)
        {
            return std::make_tuple(0, -1);
        }
        else if (result == 2)
        {
            return std::make_tuple(0, 1);
        }
        else if (result == 3)
        {
            return std::make_tuple(0, 0);
        }

        std::vector<int> avail_moves = vect_of_avail_moves(board);

        std::vector<std::tuple<int, int>> values_of_moves;
        for (int i = 0; i < avail_moves.size(); i++)
        {
            board = play_move(avail_moves[i], board, false);
            std::tuple<int, int> ret_value = min(board);
            board = reverse_move(avail_moves[i], board);
            std::tuple<int, int> final_values(avail_moves[i], std::get<1>(ret_value));
            values_of_moves.push_back(final_values);
        }

        int best_value = -10;
        int best_move;
        for (int i = 0; i < values_of_moves.size(); i++)
        {
            int move, value;
            std::tie(move, value) = values_of_moves[i];
            if (value > best_value)
            {
                best_move = move;
                best_value = value;
            }
        }

        std::tuple<int, int> best_pair(best_move, best_value);
        return best_pair;
    }

    std::tuple<int, int> min(std::vector<std::vector<int>> board)
    {

        int result = end_of_game(board);
        if (result == 1)
        {
            return std::make_tuple(0, -1);
        }
        else if (result == 2)
        {
            return std::make_tuple(0, 1);
        }
        else if (result == 3)
        {
            return std::make_tuple(0, 0);
        }

        std::vector<int> avail_moves = vect_of_avail_moves(board);
        std::vector<std::tuple<int, int>> values_of_moves;
        for (int i = 0; i < avail_moves.size(); i++)
        {
            board = play_move(avail_moves[i], board, true);
            std::tuple<int, int> ret_value = max(board);
            board = reverse_move(avail_moves[i], board);
            std::tuple<int, int> final_values(avail_moves[i], std::get<1>(ret_value));
            values_of_moves.push_back(final_values);
        }

        int best_value = 10;
        int best_move;
        for (int i = 0; i < values_of_moves.size(); i++)
        {
            int move, value;
            std::tie(move, value) = values_of_moves[i];
            if (value < best_value)
            {
                best_move = move;
                best_value = value;
            }
        }

        std::tuple<int, int> best_pair(best_move, best_value);
        return best_pair;
    }

    std::vector<int> vect_of_avail_moves(std::vector<std::vector<int>> board)
    {
        std::vector<int> moves;
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                if (board[i][j] == 0)
                {
                    moves.push_back(i * 3 + j);
                }
            }
        }
        return moves;
    }

    AI(){};
};

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

    std::string players_turn_string()
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

    void change_turns()
    {
        this->p1_turn = (this->p1_turn) ? false : true;
    }

    void play_player_move()
    {
        int move;
        while (true)
        {
            std::cin >> move;
            if (move > 9 || move < 0)
            {
                std::cout << "Try a number from 1-9";
            }
            bool move_legal = legal_move(move - 1, this->board);
            if (move_legal)
            {
                this->board = play_move(move - 1, this->board, this->p1_turn);
                break;
            }
            else
            {
                std::cout << "Someone's already played there!\nMove: ";
            }
        }
    }

    void play_ai_move(int move)
    {
        bool move_legal = legal_move(move, this->board);
        if (move_legal)
        {
            this->board = play_move(move, this->board, this->p1_turn);
        }
        else
        {
            throw "AI played illegal move";
        }
    }

    //two player games
    int play_two_game()
    {
        while (true)
        {
            std::cout << "It is " << this->players_turn_string() << "'s turn\nMove: ";

            this->play_player_move();
            this->change_turns();

            print_board(this->get_board());

            int end = end_of_game(this->board);
            if (end == 1)
            {
                std::cout << "Player 1 Won!";
                return 0;
            }
            else if (end == 2)
            {
                std::cout << "Player 2 Won!";
                return 0;
            }
            else if (end == 3)
            {
                std::cout << "You drew! Better luck next time.";
                return 0;
            }
        }
        return 0;
    }

    //one player game
    int play_one_game()
    {
        AI comp;
        while (true)
        {
            if (p1_turn)
            {
                std::cout << "It is your turn\nMove: ";

                this->play_player_move();
                this->change_turns();
            }
            else
            {
                std::tuple<int, int> ret_values = comp.max(board);
                int move = std::get<0>(ret_values);
                this->play_ai_move(move);
                this->change_turns();
            }

            print_board(this->get_board());

            int end = end_of_game(this->board);
            if (end == 1)
            {
                std::cout << "Player 1 Won!";
                return 0;
            }
            else if (end == 2)
            {
                std::cout << "The AI Won!";
                return 0;
            }
            else if (end == 3)
            {
                std::cout << "You drew! Better luck next time.";
                return 0;
            }
        }
        return 0;
    }
    Game(){};
};

std::vector<std::vector<int>> play_move(int square, std::vector<std::vector<int>> board, bool p1_turn)
{
    int x = square % 3;
    int y = square / 3;
    if (p1_turn)
    {
        board[y][x] = 1;
    }
    else
    {
        board[y][x] = 2;
    }
    return board;
}

std::vector<std::vector<int>> reverse_move(int square, std::vector<std::vector<int>> board)
{
    int x = square % 3;
    int y = square / 3;
    board[y][x] = 0;
    return board;
}

bool legal_move(int square, std::vector<std::vector<int>> board)
{
    int x = square % 3;
    int y = square / 3;
    if (board[y][x] != 0)
    {
        return false;
    }

    return true;
}

int check_win(std::vector<std::vector<int>> board)
{
    //verticals
    for (int i = 0; i < 3; i++)
    {
        int vert_check_player = board[i][0];
        if (vert_check_player == 0)
        {
            continue;
        }

        for (int j = 1; j < 3; j++)
        {
            if (board[i][j] != vert_check_player)
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
        int horz_check_player = board[0][i];
        if (horz_check_player == 0)
        {
            continue;
        }

        for (int j = 1; j < 3; j++)
        {
            if (board[j][i] != horz_check_player)
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
    int diag_check_player = board[0][0];
    if (diag_check_player != 0)
    {
        for (int i = 1; i < 3; i++)
        {
            if (board[i][i] != diag_check_player)
            {
                break;
            }
            if (i == 2)
            {
                return diag_check_player;
            }
        }
    }

    diag_check_player = board[2][0];
    if (diag_check_player != 0)
    {
        for (int i = 1; i < 3; i++)
        {
            if (board[2 - i][i] != diag_check_player)
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

bool check_draw(std::vector<std::vector<int>> board)
{
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            if (board[i][j] == 0)
            {
                return false;
            }
        }
    }
    return true;
}

int end_of_game(std::vector<std::vector<int>> board)
{
    int ret;
    int win = check_win(board);
    if (win == 0)
    {
        bool draw = check_draw(board);
        draw ? ret = 3 : ret = 0;
        return ret;
    }
    else
    {
        return win;
    }
}
//These are the printing functions

//param: int[3][3]
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

// This is the main function
int main()
{
    int players;
    while (true)
    {
        std::cout << "\nHow many players? Type 1 or 2: ";
        std::cin >> players;
        if (players == 1 || players == 2)
        {
            break;
        }
        else
        {
            std::cout << "Try again";
        }
    }

    std::cout << "\nEach square is a number\nType that number to mark your square\n";
    print_template_board();

    Game active;
    if (players == 1)
    {
        active.play_one_game();
        return 0;
    }
    else
    {
        active.play_two_game();
        return 0;
    }
}