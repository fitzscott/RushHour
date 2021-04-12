import StorePuzzle as sp
import Board

class StorePuzzleMem(sp.StorePuzzle):
    """
    Store puzzle solution search space in memory, instead of in a
    graph database.
    """
    def __init__(self):
        super().__init__()
        self._srchspc = []
        self._prntidx = []
        self._lyridx = []
        self._dups = 0
        self._solnidx = -1
        self._soln = None
        self._solndir = "E:/data/rhpuzlsoln/"

    @property
    def dups(self):
        return (self._dups)

    @dups.setter
    def dups(self, val):
        self._dups = val

    def save_position(self, positions, prnt, lyr=-1):
        self._srchspc.append(positions)
        self._prntidx.append(prnt)
        self._lyridx.append(lyr)

    def save_board(self, positions, puzzle_num=0, layer=0):
        # print("Saving board " + ",".join([str(p) for p in positions]))
        if positions in self._srchspc:
            self._dups += 1
            return (False)
        # We don't know the parent yet
        pidx = -1
        self.save_position(positions, pidx, layer)
        return (True)

    def link_boards(self, brd1, brd2, puzzle_num):
        bidx1 = self._srchspc.index(brd1.positions)
        # We know the index for this board is the last one added
        bidx2 = len(self._prntidx) - 1
        # print("Linking {0} back to {1}".format(bidx2, bidx1))
        self._prntidx[bidx2] = bidx1
        return (True)

    def mark_solution_board(self, brd, puzzle_num):
        print("Marking solution for " + str(brd))
        self._solnidx = self._srchspc.index(brd.positions)

    def fetch_solution(self, puzzle_num):
        flnm = self._solndir + "soln{0}.txt".format(puzzle_num)
        try:
            fl = open(flnm)
        except Exception as exc:
            print("Solution does not exist yet. Calculating...")
            # print(str(exc))
            return (False)
        soln = []
        tmpbrd = []
        lnno = 0
        for ln in fl:
            flds = ln.strip().split()
            if len(flds) < 1:
                continue
            tmpbrd.extend([int(f) if f != "-" else -1
                           for f in flds])
            lnno += 1
            if lnno == 6:
                # print("creating board from " + str(tmpbrd))
                b = Board.Board(tmpbrd)
                # print("    fetched board from file:\n" + str(b))
                soln.append(b)
                lnno = 0
                tmpbrd = []
        self._soln = soln
        # print("solution is " + str(soln))
        return (True)

    def solution_exists(self, puzzle_num):
        if self._soln is not None:
            return (True)
        if self.fetch_solution(puzzle_num):
            return (True)
        return (False)

    def prnsoln(self):
        if self._soln is None:
            print("        No solution to print")
        else:
            print("printing existing solution")
            # print("Solution has {0} steps".format(len(self._soln)))
            for x in self._soln:
                print(str(x))

    def read_solution(self, puzzle_num):
        if self._soln is None:
            soln = []
            actvbrd = self._srchspc[self._solnidx]
            actidx = self._prntidx[self._srchspc.index(actvbrd)]
            while actidx != -1:
                b = Board.Board(actvbrd)
                soln.append(b)
                actvbrd = self._srchspc[actidx]
                actidx = self._prntidx[self._srchspc.index(actvbrd)]
            b = Board.Board(actvbrd)    # pick up the 1st position
            soln.append(b)
            assert(len(soln) > 0)
            self._soln = [b for b in reversed(soln)]
            # print("Solution created")
            # self.prnsoln()
        # else:
        #     print("Solution already exists")
        #     self.prnsoln()
        return(self._soln)


    def read_board(self, puzzle_num):
        flnm = "Puzls/puzl" + str(puzzle_num) + ".txt"
        positions = []
        fl = open(flnm)
        for ln in fl:
            ro = ln.strip().split()
            positions.extend([int(p) if p != "-" else -1 for p in ro])
        fl.close()
        # print(",".join(positions))
        self.save_position(positions, -1, 0)
        b = Board.Board(positions)
        b.assign_vehicles()
        return (b)

    def save_solution(self, puzzle_num):
        self.read_solution(puzzle_num)
        assert(self._soln is not None)
        flnm = self._solndir + "soln{0}.txt".format(puzzle_num)
        fl = open(flnm, "w")
        for b in self._soln:
            pos = b.positions
            # print("writing board " + ",".join([str(x) for x in pos]))
            for ro in range(6):
                idx1 = ro * 6
                # print("    writing positions " + " ".join(
                #     [str(p) for p in pos[idx1:idx1+6]]))
                fl.write(" ".join([str(x) if x != -1 else "-"
                                   for x in pos[idx1:idx1+6]]))
                fl.write("\n")
            fl.write("\n")
        fl.close()


if __name__ == "__main__":
    import Puzzle as pz
    import sys
    
    if len(sys.argv) > 1:
        pzlnum = int(sys.argv[1])
    else:
        pzlnum = 1
    puzl = pz.Puzzle(pzlnum)
    spm = StorePuzzleMem()
    puzl.storage = spm
    puzl.start_board()
    print(str(puzl))
    # pos1 = "1,1,-,-,-,2,3,-,-,4,-,2,3,0,0,4,-,2,3,-,-,4,-,-,5,-,-,-,6,6,5,-,7,7,7,-".split(",")
    # if spm.save_board(pos1, pzlnum):
    #     print("Board saved ok (but should not have been)")
    # else:
    #     print("Board rejected (correctly)")
    if puzl.find_solution():
        soln = puzl.storage.read_solution(puzl.puzzle_num)
        print("tried to create {0} duplicates".format(puzl.storage.dups))
        for brd in soln:
            print(str(brd))
    else:
        print("no solution found")
