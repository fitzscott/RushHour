import Puzzle as pz
import StorePuzzleNeo4j as spn4j
import StorePuzzleNeo4jnouc as spn4jnc
import sys

class PuzzleN4j(pz.Puzzle):
    """
    PuzzleN4j - puzzle with results stored in Neo4j
    """
    def __init__(self, puzzle_num=0, uniq=True):
        super().__init__(puzzle_num)
        if uniq:
            self.storage = spn4j.StorePuzzleNeo4j()
        else:
            self.storage = spn4jnc.StorePuzzleNeo4jnouc()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        puzlnum = int(sys.argv[1])
    else:
        puzlnum = 100
    if len(sys.argv) > 2:
        uniq = int(sys.argv[2]) == 1
    else:
        uniq = True
    pn4 = PuzzleN4j(puzlnum, uniq)
    # pn4.storage.read_board(pn4.puzzle_num)
    pn4.start_board()
    print(str(pn4))
    pn4.find_solution()
    soln = pn4.storage.return_solution(pn4.puzzle_num)
    print("tried to create {0} duplicates".format(pn4.storage.dups))
    for brd in soln:
        print(str(brd))
    pn4.storage.disconnect()
