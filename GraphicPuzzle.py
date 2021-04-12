import Puzzle as pz
import PuzzleN4j as pn4j
import StorePuzzleMem as spm
import pygame
import sys


class GraphicPuzzle():
    """
    Start out just stepping through the solution for a given puzzle.
    """
    Gray = (127, 127, 127)
    Colors = {0: (255, 0, 0), 1: (127, 127, 255), 2: (255, 192, 192),
              3: (127, 255, 127), 4: (0, 192, 192), 5: (192, 0, 192),
              6: (0, 127, 0), 7: (32, 32, 32), 8: (127, 255, 255),
              9: (255, 255, 127), 10: (127, 32, 32), 11: (32, 127, 127),
              12: (192, 192, 0), 13: (255, 127, 255), 14: (0, 0, 255),
              15: (0, 255, 255), 16: (255, 0, 255), 17: (127, 255, 0),
              20: (255, 0, 0), -1: Gray}

    def __init__(self, puzzle_num=0, useDB=True):
        # super().__init__(puzzle_num)
        self._brddim = 6
        self._sqsiz = 50
        self._dims = [self._brddim * self._sqsiz, self._brddim * self._sqsiz]
        if useDB:
            self._puzl = pn4j.PuzzleN4j(puzzle_num)
        else:
            self._puzl = pz.Puzzle(puzzle_num)
            stor = spm.StorePuzzleMem()
            self._puzl.storage = stor
            self._puzl.start_board()
            assert(self._puzl.find_solution())
        print("retrieving solution...")
        self._soln = self._puzl.storage.read_solution(puzzle_num)
        # print("solution retrieved:")
        # for b in self._soln:
        #     print(str(b))
        pygame.init()
        self._screen = pygame.display.set_mode(self._dims)
        pygame.display.set_caption("Rush Hour")
        self._clock = pygame.time.Clock()

    def draw_board(self, brd):
        print(str(brd))
        self._screen.fill(GraphicPuzzle.Gray)
        pos = brd.positions
        for ro in range(self._brddim):
            for col in range(self._brddim):
                idx = ro * self._brddim + col
                if pos[idx] == -1:
                    continue
                clr = GraphicPuzzle.Colors[pos[idx]]
                uly = ro * self._sqsiz
                ulx = col * self._sqsiz
                pygame.draw.rect(self._screen, clr,
                                 [ulx, uly, self._sqsiz, self._sqsiz], width=0)

    def draw_soln(self):
        tiktime = 1000
        for brd in self._soln:
            self.draw_board(brd)
            pygame.display.flip()
            self._clock.tick(tiktime)
            pygame.time.wait(tiktime)   # which do we use?
        self._puzl.storage.disconnect()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        puzlnum = int(sys.argv[1])
    else:
        print("usage: python {0} puzzle#".format(sys.argv[0]))
        sys.exit(-1)
    if len(sys.argv) > 2:
        useDB = int(sys.argv[2]) == 1
    else:
        useDB = True

    gpn4 = GraphicPuzzle(puzlnum, useDB)
    gpn4.draw_soln()
