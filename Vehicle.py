class Vehicle():
    """
    Track a piece's position on the board.
    Return potential moves.
    """
    def __init__(self, id, minpos=0, maxpos=6):
        self._id = id
        self._location = []
        self._minpos = minpos
        self._maxpos = maxpos
        self._offsets = None

    @property
    def location(self):
        return (self._location)

    @location.setter
    def location(self, val):
        self._location = val

    @property
    def loc(self):
        return (self._location)

    def __str__(self):
        locstr = ", ".join(["({0},{1})".format(loc[0], loc[1])
                            for loc in self._location])
        return ("Vehicle {0} at {1}".format(self._id, locstr))

    def offsets(self):
        if self._offsets is None:
            assert (len(self._location) > 1)
            if self._location[0][0] == self._location[1][0]:
                offset = (0, 1)     # moves vertically
            else:
                offset = (1, 0)     # moves horizontally
            self._offsets = [offset, (-1 * offset[0], -1 * offset[1])]
        return(self._offsets)

    def moves(self):
        mvs = []
        for ofs in self.offsets():
            newpos = [(self.loc[i][0] + ofs[0], self.loc[i][1] + ofs[1])
                      for i in range(len(self._location))]
            addpos = True
            for np in newpos:
                if np[0] < self._minpos or np[0] >= self._maxpos\
                        or np[1] < self._minpos or np[1] >= self._maxpos:
                    addpos = False
                    break
            if addpos:
                mvs.append(newpos)
        return (mvs)

    def filteredmoves(self, filt):
        """
        filteredmoves - return a list of legal moves, given empty spaces
        :param filt: list of empty positions from the board
        :return:
        """
        filtmovs = []
        for mov in self.moves():
            addmov = True
            for pos in mov:
                if pos not in filt and pos not in self.loc:
                    addmov = False
                    break
            if addmov:
                filtmovs.append(mov)
        return (filtmovs)


if __name__ == "__main__":
    truk = Vehicle(3)
    for yval in range(3):
        truk.location.append((yval,2))
    print(truk)
    moves = truk.moves()
    print(str(moves))
    truk.location = moves[0]       # [(1,2), (2,2), (3,2)]
    # print(str(truk.offsets()))
    print(truk)
    print(str(truk.moves()))
    # if (2,1) in [(1,0), (1,1), (2,1)]:
    #     print("in works for tuples")
    emptyspaces = [(0,2), (4,2)]    # [(0,2)]
    print(str(truk.filteredmoves(emptyspaces)))
    emptyspaces = []
    print(str(truk.filteredmoves(emptyspaces)))
