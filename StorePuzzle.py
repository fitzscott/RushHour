import Board as brd
from datetime import datetime

class StorePuzzle():
    """
    StorePuzzle
    Interface methods for saving off puzzle state.
    """
    def __init(self):
        self._puzzle_num = None

    @property
    def puzzle_num(self):
        return (self._puzzle_num)

    @puzzle_num.setter
    def puzzle_num(self, val):
        self._puzzle_num = val

    def make_puzzle_num(self, puzl=None):
        if self._puzzle_num is None:
            dto = datetime.now()
            self._puzzle_num = dto.strftime("%Y%m%d%H%M%S")
        else:
            self._puzzle_num = str(puzl)
        return(self._puzzle_num)

    def save_board(self, positions, puzzle_num=0, layer=0):
        if puzzle_num == 0:
            puzzle_num = self.make_puzzle_num()
        print("Saving puzzle {0}, positions {1}".format(puzzle_num, positions))
        return(True)

    def link_boards(self, brd1, brd2, puzzle_num):
        pass

    def mark_solution_board(self, brd, puzzle_num):
        pass

    def read_board(self, puzzle_num):
        if puzzle_num == 1:
            b = brd.Board([1, 1, -1, -1, -1, 2,
                           3, -1, -1, -1, -1, 2,
                           3, 0, 0, 4, -1, 2,
                           3, -1, -1, 4, -1, -1,
                           5, -1, -1, 4, 6, 6,
                           5, -1, 7, 7, 7, -1])
        else:
            b = brd.Board([-1,-1,-1,-1,-1,-1,
                       -1,-1,-1,-1,2,-1,
                       -1,0,0,-1,2,-1,
                       -1,-1,-1,-1,-1,-1,
                       -1,-1,-1,-1,-1,-1,
                       -1,-1,-1,-1,-1,-1])
        return (b)

    def read_solution(self, puzzle_num):
        pass

    def return_solution(self, puzzle_num):
        pass

    def save_solution(self, puzzle_num):
        pass

    def solution_exists(self, puzzle_num):
        return (False)

    def fetch_solution(self, puzzle_num):
        return (False)

    def connect(self):
        pass

    def disconnect(self):
        pass
