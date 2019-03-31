"""
ITESM - MCC
Intelligent Systems
Assignment L3 - 8-Puzzle Breadth-First Search Solver

Author: Carlos Eduardo Hernandez Rincon
Student ID: A01181616
Email: a01181616@itesm.mx

Date: January 24th 2019
"""
import sys

from copy import deepcopy
from datetime import datetime
from queue import Queue


class SolutionNode:

    def __init__(self,
                 board: list,
                 parent=None,
                 action_taken: str = None):
        self.board = board
        self.fingerprint = SolutionNode.board_2_fingerprint(board)
        self.size_of_board = len(self.board)

        self.parent = parent
        self.action_taken = action_taken
        self.position_of_zero = self.find_position_of_zero()
        self.has_been_visited = False

        # We'll wait until the node is visited in order to calculate the possible movements
        self._possible_movements = []

    def get_possible_movements(self) -> list:
        # If we have already calculated the movements, just return them
        if self._possible_movements:
            return self._possible_movements

        # In a board like this
        #
        # 7, 8, 9
        # 4, 0, 2
        # 3, 5, 1
        #
        # The 0 can only move up, down, left or right, we just need to see if the 0 would go out of the board to see
        #  if the move is legal

        legal_moves = []
        zero_x = self.position_of_zero[0]
        zero_y = self.position_of_zero[1]

        # UP
        if zero_x != 0:
            # If we are not on the upper level
            new_board = deepcopy(self.board)
            number_to_switch = self.board[zero_x - 1][zero_y]
            new_board[zero_x][zero_y] = number_to_switch
            new_board[zero_x - 1][zero_y] = 0

            new_node = SolutionNode(board=new_board, parent=self, action_taken="UP")
            legal_moves.append(new_node)

        # DOWN
        if zero_x != self.size_of_board - 1:
            # If we are not on the lower level
            new_board = deepcopy(self.board)
            number_to_switch = self.board[zero_x + 1][zero_y]
            new_board[zero_x][zero_y] = number_to_switch
            new_board[zero_x + 1][zero_y] = 0

            new_node = SolutionNode(board=new_board, parent=self, action_taken="DOWN")
            legal_moves.append(new_node)

        # RIGHT
        if zero_y != self.size_of_board - 1:
            # If we are not on the right-most level
            new_board = deepcopy(self.board)
            number_to_switch = self.board[zero_x][zero_y + 1]
            new_board[zero_x][zero_y] = number_to_switch
            new_board[zero_x][zero_y + 1] = 0

            new_node = SolutionNode(board=new_board, parent=self, action_taken="RIGHT")
            legal_moves.append(new_node)

        # LEFT
        if zero_y != 0:
            # If we are not on the left-most level
            new_board = deepcopy(self.board)
            number_to_switch = self.board[zero_x][zero_y - 1]
            new_board[zero_x][zero_y] = number_to_switch
            new_board[zero_x][zero_y - 1] = 0

            new_node = SolutionNode(board=new_board, parent=self, action_taken="LEFT")
            legal_moves.append(new_node)

        self._possible_movements = legal_moves

        return legal_moves

    def find_position_of_zero(self) -> tuple:
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] == 0:
                    return x, y
        return -1, -1

    @staticmethod
    def fingerprint_2_board(fingerprint: str, separator: str = " ") -> list:
        # This parses a fingerprint in the form 0 1 2 3 4 5 6 7 8 separate by the specified separator into
        # a numeric matrix
        elements = fingerprint.split(separator)
        size_of_board = int(len(elements) ** 0.5)
        board = []
        row = []

        for e in elements:

            row.append(int(e))

            if len(row) == size_of_board:
                board.append(row)
                row = []

        return board

    @staticmethod
    def board_2_fingerprint(board: list, separator: str = " ") -> str:
        # This turns a numeric matrix into a string representation of the values separated by the separator
        result = [str(e) for row in board for e in row]
        return separator.join(result)


def solve_8_puzzle_using_bfs(puzzle: str, goal: str = "0 1 2 3 4 5 6 7 8"):
    print("Solving!...")

    root = SolutionNode(SolutionNode.fingerprint_2_board(puzzle))

    start_time = datetime.now()
    solution = breadth_first_search(root, goal)
    finish_time = datetime.now() - start_time

    print(f"Execution time: {finish_time}")

    if not solution["success"]:
        print(f"No viable solution was found for {puzzle} and a goal {goal}")
        print(f"Visited nodes: {len(solution['visited'])}")
        print(f"Memory used in bytes: {solution['memory_used']}")

    else:
        # We need to follow the tree from the solution leaf up to the root in order to show the path taken
        steps = []
        traversing_node = solution["end_node"]

        while traversing_node is not None:
            steps.append(traversing_node)
            traversing_node = traversing_node.parent

        # Since we started at the solution leaf, we need to reverse the list of steps in order to get
        #  a chronological description of the required steps to reach the solution
        steps.reverse()

        print(f"Visited nodes: {len(solution['visited'])}")
        print(f"Depth level reached: {len(steps)}")
        print(f"Memory used in bytes: {solution['memory_used']}")

        for idx, s in enumerate(steps):
            print(f"{idx}. Move: {s.action_taken}" if s.action_taken else "")

            # Print a nice formatted board from the matrix representing it
            print("\n".join(["".join(["{:4}".format(item) for item in row]) for row in s.board]))


def breadth_first_search(root: SolutionNode, goal: str) -> dict:
    frontier = Queue()
    visited = set()
    memory_used_in_bytes = 0

    frontier.put(root)

    while not frontier.empty():
        current_node = frontier.get()

        if current_node.fingerprint == goal:
            memory_used_in_bytes += sys.getsizeof(current_node)
            return {
                "end_node": current_node,
                "visited": visited,
                "memory_used": memory_used_in_bytes,
                "success": True
            }

        for possible_movements in current_node.get_possible_movements():
            if possible_movements.fingerprint not in visited and not current_node.has_been_visited:
                frontier.put(possible_movements)

        visited.add(current_node.fingerprint)
        current_node.has_been_visited = True
        memory_used_in_bytes += sys.getsizeof(current_node)

    return {
        "visited": visited,
        "memory_used": memory_used_in_bytes,
        "success": False
    }


# The following methods are helper methods to create the menu, read input from the user or parse it from files
def menu_selection(options: list, title: str = "Please select an option") -> int:
    if not options:
        return 0

    lower_bound = 1
    higher_bound = len(options)

    menu = ["\n" + title]

    for idx, o in enumerate(options):
        line = f"{idx + 1}. {o}"
        menu.append(line)
    menu = "\n".join(menu)
    menu += "\nSelection: "

    selection = ask_for_a_number(menu)

    while not lower_bound <= selection <= higher_bound:
        print("That's not a valid selection, please try again...")
        selection = ask_for_a_number(menu)

    return selection


def ask_for_a_number(message: str = "Please enter an int number: ") -> int:

    # The following loops until the user inputs a valid number
    while True:
        try:
            x = int(input(message))
            return x
        except ValueError:
            print(f"That's not a valid number, please try again...")


def read_inputs_from_file(filename: str) -> tuple:

    with open(filename, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return tuple(lines)


if __name__ == '__main__':
    option = menu_selection(["Read from a file.",
                             "Read from std input.",
                             "Use the assignment case <7 2 4 5 0 6 8 3 1>"],
                            "****N-Puzzle Solver Using BFS****\nPlease select an option:")

    if option == 1:
        filename = input("Enter the filename from which to read: ")
        start_board, goal = read_inputs_from_file(filename)

    elif option == 2:
        start_board = input("Input the starting state of the board separated by spaces: ").strip()
        goal = input("Input the goal state of the board separated by spaces: ").strip()

    elif option == 3:
        start_board = "7 2 4 5 0 6 8 3 1"
        goal = "0 1 2 3 4 5 6 7 8"

    solve_8_puzzle_using_bfs(start_board, goal)
