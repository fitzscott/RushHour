import StorePuzzleNeo4j as spn4

class StorePuzzleNeo4jnouc(spn4.StorePuzzleNeo4j):
    """
    No unique constraint on the board nodes.
    Enforce uniqueness in code.
    """
    def save_board(self, positions, puzzle_num=0, layer=0):
        if self._sess is None:
            self.connect()
        if puzzle_num == 0:
            puzzle_num = self.make_puzzle_num()

        # First, see if board exists.  Layer does not matter for uniqueness.
        matchqry = """
        MATCH (b:board {{puzzlenum: {0}, state: {1}}}) 
        RETURN b""".format(puzzle_num, positions)
        try:
            rec = self._sess.run(matchqry)
        except Exception as exc:
            print("exception {0}".format(exc))
            return (None)
        for res in rec:
            self.dups += 1
            return (False)

        cr8qry = """
        CREATE (:board {{ state: {0}, puzzlenum: {1}, layer: {2} }})
        """.format(positions, puzzle_num, layer)
        # print(cr8qry)
        retval = True
        try:
            self._sess.run(cr8qry)
        except Exception as exc:
            errstr = "exception {0} while creating board".format(exc)
            retval = False
        return (retval)
