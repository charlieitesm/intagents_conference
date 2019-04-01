# Game messages
ILLEGAL_MOVE_MSG = "The move is illegal, please try again..."
WINNER_MSG = "The winner is:"
YOU_WIN_MSG = "You WIN!"
YOU_LOSE_MSG = "You lose!"

# TicTacToe messages
TICTACTOE_ENDING_MSG = "GAME OVER! Final results:"
TICTACTOE_DRAW_MSG = "It's a Draw!"

ENTER_YOUR_MOVE_MSG = "Enter your comma-separated move"
INVALID_FORMAT_FOR_MOVE_MSG = "The format for the entered move is invalid, please try again."
GAME_TOKEN = "game_token"
MOVE = "move"


class GameToken:

    def __init__(self, token_symbol: str):
        self.token_symbol = token_symbol

    def __str__(self):
        return self.token_symbol


TIC_TAC_TOE_TOKENS = [GameToken("X"), GameToken("O")]


class TicTacToeBoard:

    def __init__(self):
        self.current_state = [[]]
        self.init_board()

        for t in TIC_TAC_TOE_TOKENS:
            if str(t) == "X":
                self.x = t
            elif str(t) == "O":
                self.o = t

        assert self.x is not None and self.o is not None

    def init_board(self):
        # Initialize a 3x3 board with no tokens
        self.current_state = [
            [None, None, None] for _ in range(3)
        ]

    def get_empty_spaces_coordinates(self) -> list:
        empty_spaces = []  # What are we living for? ♫

        for x, row in enumerate(self.current_state):
            for y, game_token in enumerate(row):
                if game_token is None:
                    empty_spaces.append((x, y))

        return empty_spaces

    def __str__(self) -> str:
        """
        This will give us a board formatted like this:
         X | O | X
         X | X | O
         X | O | O
        :return: a str representation of the current board
        """
        representation = "\n".join(
            "|".join(["{:^3}".format(str(val)) if val is not None
                      else "{:3}".format("") for val in row]) for row in self.current_state)
        return representation

    def serialize(self) -> str:
        return ",".join([",".join([str(c) if c is not None else "" for c in row]) for row in self.current_state])

    def deserialize(self, serialized_board: str) -> object:
        state = []

        i = 0
        serialized_tokens = [s.upper() for s in serialized_board.split(",")]

        while i < 9:
            row = [None if not e else
                   self.x if e.upper() == str(self.x) else self.o for e in serialized_tokens[i: i + 3]]
            state.append(row)
            i += 3

        self.current_state = state

        return self


class ConsoleUI:

    def input(self, message: str) -> str:
        return input(f"{message}: ")

    def output(self, message: str):
        print(message)


class DummyUI:

    def input(self, message: str) -> str:
        pass

    def output(self, message: str):
        pass


class TicTacToeGame:

    def __init__(self, players: list):
        self.board = TicTacToeBoard()
        self.players = players
        self.winner = None
        self.legal_tokens = None
        self.legal_tokens = TIC_TAC_TOE_TOKENS

    def play(self):  

        # This will contain the main game loop
        is_game_over_yet = False

        while not is_game_over_yet:

            # Ask each of the players for their move
            for player in self.players:

                player.ui.output(f"***** {player}'s turn! ******")
                player.ui.output(self.board)
                move = player.make_move(self.board)

                # Check that the move is legal in the context of the board
                while not self.is_valid_move(move):
                    player.ui.output(ILLEGAL_MOVE_MSG)
                    move = player.make_move(self.board)

                # Apply the player's move to the board since we now know it was legal
                move_x, move_y = move[MOVE]
                self.board.current_state[move_x][move_y] = move[GAME_TOKEN]

                is_game_over_yet = self.is_game_over()

                # If the game has ended, break the player loop which in turn will break the game loop
                if is_game_over_yet:
                    break

        # Leave every concrete game to decide what it needs to do after a game is completed
        self.finish_game()  

    def is_valid_move(self, move: dict) -> bool:
        """
        Determines if the move made by player is legal on this board

        In general, a Tic Tac Toe is valid if:
        1. It is made within the bounds of the board
        2. The space that is intended to be used is not already in use

        :param move: a dict with the move and the game_token to be placed by player
        :return: True if the move is valid, False otherwise.
        """

        move_x, move_y = move[MOVE]

        return TicTacToeGameUtil.is_legal_tic_tac_toe_move(self.board, move_x, move_y)

    def is_game_over(self) -> bool:
        """
        Determines if the game is already over

        In general, a TicTacToe game is over if:
        1. There is a line of the same game_token horizontally, vertically or diagonally
        2. There are no more spaces to use
        :return:
        """
        # Check if we have a winner
        winning_token = TicTacToeGameUtil.get_winner(self.board)

        if winning_token:
            self.winner = self.token_to_player(winning_token)
            return True

        # Check if there are no more places to put a game_token
        for row in self.board.current_state:
            for val in row:
                if val is None:
                    return False
        return True

    def finish_game(self):
        """
        Prepares and outputs to each of the players a message with the results
        :return:
        """
        winner_result = TICTACTOE_DRAW_MSG if not self.winner else f"{WINNER_MSG} {self.winner}"
        final_message = "\n".join([TICTACTOE_ENDING_MSG, str(self.board), winner_result])

        for p in self.players:
            p.ui.output(final_message)

    def token_to_player(self, winning_token: GameToken):
        """
        Get the player holding the game_token represented by token_str
        :param winning_token: a str representing the game_token to look for
        :return: a Player holding the game_token represented by token_str, None if no one was found
        """
        for p in self.players:
            if winning_token == p.game_token:
                return p

    def str_to_game_token(self, str_token: str) -> GameToken:
        for gt in self.legal_tokens:
            if str_token.upper() == str(gt).upper():
                return gt


class TicTacToeGameUtil:

    @staticmethod
    def is_legal_tic_tac_toe_move(board: TicTacToeBoard, move_x: int, move_y: int) -> bool:
        """
        Determines if the move made by player is legal on this board

        In general, a Tic Tac Toe is valid if:
        1. It is made within the bounds of the board
        2. The space that is intended to be used is not already in use
        :param board: a Board where you want to check the move
        :param move_x: an int with the x coordinate for the move
        :param move_y: an int with the y coordinate for the move
        :return: True if the move is valid, False otherwise.
        """
        board_size = len(board.current_state)

        # Check if the move is within bounds
        if not 0 <= move_x < board_size or not 0 <= move_y < board_size:
            return False

        # Check the space is not in use already
        value_at_board = board.current_state[move_x][move_y]

        if value_at_board is not None:
            return False

        return True

    @staticmethod
    def get_winner(board: TicTacToeBoard) -> GameToken:
        for x, row in enumerate(board.current_state):
            for y, gt in enumerate(row):

                # There will be no winner combination on this row/column
                if gt is None:
                    continue

                if TicTacToeGameUtil.check_complete_line_in_board(board, gt, x, y):
                    winner_token = gt
                    return winner_token

    @staticmethod
    def check_complete_line_in_board(board: TicTacToeBoard, game_token: GameToken, x: int, y: int) -> bool:
        """
        Checks if there are exactly three tokens equal to val horizontally, vertically and diagonally on the board
        respective to x and y
        :param board: the Board in which to check the line
        :param game_token: a str representing the game_token to look for
        :param x: an int representing the original X coordinate of val
        :param y: an int representing the original Y coordinate of val
        :return: True if a line of successive val was found, False if otherwise
        """
        num_of_same_tokens = 0
        len_of_board = len(board.current_state)

        # Check horizontally
        for j in range(len_of_board):
            if board.current_state[x][j] == game_token:
                num_of_same_tokens += 1
            else:
                break

        if num_of_same_tokens == 3:
            return True

        num_of_same_tokens = 0

        # Check vertically
        for i in range(len_of_board):
            if board.current_state[i][y] == game_token:
                num_of_same_tokens += 1
            else:
                break

        if num_of_same_tokens == 3:
            return True

        num_of_same_tokens = 0

        # Check diagonally top to bottom, but only if we can do so
        if (x, y) in ((0, 0), (1, 1), (2, 2), (2, 0), (0, 2)):

            # Left to right:
            for i in range(len_of_board):
                if game_token != board.current_state[i][i]:
                    break
                else:
                    num_of_same_tokens += 1

            if num_of_same_tokens == 3:
                return True

            num_of_same_tokens = 0

            # Right to left
            for k in range(len_of_board):
                i = 0 + k
                j = 2 - k
                if game_token == board.current_state[i][j]:
                    num_of_same_tokens += 1

            return num_of_same_tokens == 3

        else:
            return False

    @staticmethod
    def get_token_from_str(token_str: str) -> GameToken:
        for gt in TIC_TAC_TOE_TOKENS:
            if str(gt).lower() == token_str.lower():
                return gt


import math


class TicTacToeBrain:

    def calculate_next_move(self, board: TicTacToeBoard, game_token: GameToken) -> tuple:
        opponent_token = [t for t in TIC_TAC_TOE_TOKENS if t is not game_token][0]
        minimax_result = self.minimax(board, game_token, opponent_token, is_ais_turn=True)
        move = minimax_result[1]
        return move

    def minimax(self, board: TicTacToeBoard,
                my_game_token: GameToken,
                opponent_game_token: GameToken,
                is_ais_turn: bool) -> tuple:
        winning_token = TicTacToeGameUtil.get_winner(board)

        if winning_token:
            if winning_token == my_game_token:
                # The AI won
                return 1, None
            else:
                # The AI lost
                return -1, None

        possible_moves = board.get_empty_spaces_coordinates()

        if not possible_moves and not winning_token:
            # This was a draw
            return 0, None

        if is_ais_turn:  # Maximize this player
            value = -math.inf
            chosen_move = None

            for move in possible_moves:
                # Make a new Board to keep the original intact
                new_board_matrix = [row.copy() for row in board.current_state]
                new_board = TicTacToeBoard()
                new_board.current_state = new_board_matrix

                # Make the move
                new_board.current_state[move[0]][move[1]] = my_game_token

                # Simulate the opponent making a move
                new_value = self.minimax(new_board, my_game_token, opponent_game_token, is_ais_turn=False)[0]

                if new_value > value:
                    value = new_value
                    chosen_move = move

            return value, chosen_move

        else:  # It's the opponents turn, minimize it!
            value = math.inf
            chosen_move = None

            for move in possible_moves:
                # Make a new Board to keep the original intact
                new_board_matrix = [row.copy() for row in board.current_state]
                new_board = TicTacToeBoard()
                new_board.current_state = new_board_matrix

                # Make the move
                new_board.current_state[move[0]][move[1]] = opponent_game_token

                # Simulate the opponent making a move
                new_value = self.minimax(new_board, my_game_token, opponent_game_token, is_ais_turn=True)[0]

                if new_value < value:
                    value = new_value
                    chosen_move = move

            return value, chosen_move


class HumanPlayer:

    PLAYER_NUM = 1

    def __init__(self, ui: ConsoleUI, game_token: GameToken):
        self.name = self.generate_name()
        self.ui = ui
        self.game_token = game_token

    def generate_name(self) -> str:
        self_name = f"H_P{HumanPlayer.PLAYER_NUM}"
        HumanPlayer.PLAYER_NUM += 1
        return self_name

    def make_move(self, board: TicTacToeBoard) -> dict:
        move = self.ui.input(ENTER_YOUR_MOVE_MSG).split(",")

        while not move or len(move) != 2 or not all([m.isdigit() for m in move]):
            self.ui.output(INVALID_FORMAT_FOR_MOVE_MSG)
            move = self.ui.input(ENTER_YOUR_MOVE_MSG).split(",")

        move = (int(move[0]), int(move[1]))

        return {
            GAME_TOKEN: self.game_token,
            MOVE: move
        }

    def __str__(self):
        return self.name


class AIPlayer:

    PLAYER_NUM = 1

    def __init__(self, brain: TicTacToeBrain, game_token: GameToken):
        # An AI doesn't require a UI, so let's use a DummyUI so that the Game can broadcast messages to players but skip
        #  messaging the AIPlayers
        self.name = self.generate_name()
        self.ui = DummyUI()
        self.game_token = game_token
        self.brain = brain

    def generate_name(self) -> str:
        self_name = f"AI_{AIPlayer.PLAYER_NUM}"
        AIPlayer.PLAYER_NUM += 1
        return self_name

    def make_move(self, board: TicTacToeBoard) -> dict:
        move = self.brain.calculate_next_move(board, self.game_token)

        return {
            GAME_TOKEN: self.game_token,
            MOVE: move
        }

    def __str__(self):
        return self.name


def build_game() -> TicTacToeGame:
    players = []
    ui = ConsoleUI()

    # Get the appropriate tokens
    tokens = TIC_TAC_TOE_TOKENS.copy()
    ai_brain = TicTacToeBrain()

    # Build the player instances
    player_tok = tokens.pop(0)
    players.append(HumanPlayer(ui, player_tok))
    player_tok = tokens.pop(0)
    players.append(AIPlayer(ai_brain, player_tok))

    return TicTacToeGame(players)


def main():
    game = build_game()
    game.play()


if __name__ == '__main__':
    main()
