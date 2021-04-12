import StorePuzzle as sp
import time

class Puzzle():
    """
    Puzzle - track current layer of boards, derive next layer of boards
    from them, and assign links from former to latter.
    Use the StorePuzzle interface to save off boards.
    """
    def __init__(self, puzzle_num=0):
        self._puzzle_num = puzzle_num
        self._layernum = 0
        self._curr_layer = []
        self._next_layer = []
        self._storage = None
        self._soln_found = False
        self._maxlayers = 1000

    @property
    def puzzle_num(self):
        return (self._puzzle_num)

    @puzzle_num.setter
    def puzzle_num(self, val):
        self._puzzle_num = val

    @property
    def layer(self):
        return (self._layernum)

    @layer.setter
    def layer(self, val):
        self._layernum = val

    @property
    def current_layer(self):
        return (self._curr_layer)

    @current_layer.setter
    def current_layer(self, val):
        self._curr_layer = val

    @property
    def next_layer(self):
        return (self._next_layer)

    @next_layer.setter
    def next_layer(self, val):
        self._next_layer = val

    @property
    def storage(self):
        return (self._storage)

    @storage.setter
    def storage(self, val):
        self._storage = val

    def __str__(self):
        # just output the current layer
        retstr = ""
        for brd in self._curr_layer:
            retstr += str(brd)
        return (retstr)

    def start_board(self):
        b = self.storage.read_board(self.puzzle_num)
        self.current_layer = [b]

    def make_next_layer(self):
        for brd in self._curr_layer:
            # print("curr board = \n" + str(brd))
            # pull all potential boards from current
            for nubrd in brd.make_next_layer():
                # print("MNL board = \n" + str(brd))
                if self.storage.save_board(nubrd.positions, self.puzzle_num,
                                           self.layer+1):
                    # storage layer did not find a duplicate, so save
                    self._next_layer.append(nubrd)
                    if not self.storage.link_boards(brd, nubrd,
                                                    self.puzzle_num):
                        print("trouble creating link")
                        break
                    solvdbrds = nubrd.solved_vehicles()
                    if len(solvdbrds) > 0:      # make a new board without them
                        # print("Found semi-solved board\n" + str(nubrd))
                        solnbrd = nubrd.make_solved_board(solvdbrds)
                        # print("solution board:\n" + str(solnbrd))
                        if self._storage.save_board(solnbrd.positions,
                                                    self.puzzle_num,
                                                    self.layer+2):
                            if not self.storage.link_boards(nubrd, solnbrd,
                                                            self.puzzle_num):
                                print("trouble creating link to solution")
                                break
                            self._next_layer.append(solnbrd)
                            if solnbrd.solved():
                                print("Solution found!")
                                self._soln_found = True
                                self.storage.mark_solution_board(solnbrd,
                                                                 self.puzzle_num)
                                break
                        else:
                            print("Could not save solution board")
                            break
            if self._soln_found:
                break
        self._curr_layer = self._next_layer     # [nl for nl in self._next_layer]
        self._next_layer = []
        self.layer += 1
        # print("Current: {0}, next (empty): {1}".format(self._curr_layer,
        #                                                self._next_layer))
        return (self._soln_found)

    def find_solution(self):
        retval = False
        sttm = time.perf_counter()
        if not self.storage.solution_exists(self.puzzle_num):
            print("finding solution")
            for _ in range(self._maxlayers):
                if self.make_next_layer():
                    retval = True
                    break
            self.storage.save_solution(self.puzzle_num)
        else:
            retval = True
        entm = time.perf_counter()
        print("Time to find solution = {0} seconds".format(entm - sttm))
        return (retval)

if __name__ == "__main__":
    p = Puzzle()
    # p.next_layer = [1,2,3,4]
    # p.make_next_layer()
    p.storage = sp.StorePuzzle()
    b = p.storage.read_board(2)
    b.assign_vehicles()
    p.current_layer = [b]
    p.find_solution()
