import StorePuzzle as sp
from neo4j import GraphDatabase as gd
import dbcfg
import Board as brd

class StorePuzzleNeo4j(sp.StorePuzzle):
    """
    Implement StorePuzzle methods, writing to N4j
    """
    def __init__(self):
        self._drv = None
        self._sess = None
        self._dups = 0
        self._soln = None

    @property
    def dups(self):
        return(self._dups)

    @dups.setter
    def dups(self, val):
        self._dups = val
    
    def save_board(self, positions, puzzle_num=0, layer=0):
        # CREATE CONSTRAINT uniq_board_uid ON (b:board) ASSERT b.uid IS UNIQUE
        if self._sess is None:
            self.connect()
        if puzzle_num == 0:
            puzzle_num = self.make_puzzle_num()

        # In addition to the positions & puzzle #, create a field that
        # combines them to use as a unique constraint.
        uniqid = "{0}_{1}".format(puzzle_num, ",".join([str(p)
                                                        for p in positions]))
        cr8qry = """
        CREATE (:board {{ state: {0}, puzzlenum: {1}, layer: {2}, uid: '{3}' }})
        """.format(positions, puzzle_num, layer, uniqid)
        # print(cr8qry)
        retval = True
        try:
            self._sess.run(cr8qry)
        except Exception as exc:
            errstr = "exception {0} while creating board".format(exc)
            if not "already exists with label" in errstr:
                print(errstr)
                print(cr8qry)
            self._dups += 1
            retval = False
        return (retval)

    def link_boards(self, brd1, brd2, puzzle_num):
        if self._sess is None:
            self.connect()
            
        lnkqry = """
        MATCH (srcbrd:board {{ puzzlenum: {0}, state: {1} }})
        MATCH (tgtbrd:board {{ puzzlenum: {0}, state: {2} }})
        CREATE (srcbrd)-[mt:MOVE_TO]->(tgtbrd)
        RETURN mt
        """.format(puzzle_num, brd1.positions, brd2.positions)
        retval = True
        try:
            rec = self._sess.run(lnkqry)
            # for res in rec:
            #     print("link: " + str(res["mt"]))
        except Exception as exc:
            print("exception {0} while creating link".format(exc))
            retval = False
        return (retval)

    def mark_solution_board(self, brd, puzzle_num):
        markqry = """
        MATCH (solnbrd:board {{ puzzlenum: {0}, state: {1} }})
        SET solnbrd.solution = 1
        RETURN solnbrd
        """.format(puzzle_num, brd.positions)
        retval = True
        try:
            rec = self._sess.run(markqry)
            # for res in rec:
            #     print("solution: " + str(res["solnbrd"]))
        except Exception as exc:
            print("exception {0} while creating link".format(exc))
            retval = False
        return (retval)

    def return_solution(self, puzzle_num):
        if self._soln is not None:
            return (self._soln)
        if self._sess is None:
            self.connect()
        solnpathqry = """
        MATCH (sb:board {{puzzlenum: {0}, solution:1}})<-[:MOVE_TO*]-(bonp:board) 
        RETURN sb, bonp
        """.format(puzzle_num)
        # print(solnpathqry)
        solnpath = []
        try:
            rec = self._sess.run(solnpathqry)
            for res in rec:
                if len(solnpath) == 0:
                    sb = brd.Board(res["sb"]["state"])
                    solnpath.append(sb)
                pb = brd.Board(res["bonp"]["state"])
                solnpath.append(pb)
                # print("Soln: " + str(res["sb"]))
                # print("Path: " + str(res["bonp"]))
        except Exception as exc:
            print("exception {0} while returning solution".format(exc))
        self._soln = reversed(solnpath)
        return (self._soln)

    def read_board(self, puzzle_num):
        if self._sess is None:
            self.connect()
        matchqry = """
        MATCH (b:board {{puzzlenum: {0}, layer: 0}}) 
        RETURN b""".format(puzzle_num)
        try:
            rec = self._sess.run(matchqry)
        except Exception as exc:
            print("exception {0}".format(exc))
            return (None)
        # print(str(rec))
        for res in rec:
            # print(str(res))
            # print("""
            # state: {0}
            # puzzle: {1}
            # layer: {2}
            # uid: {3}
            # """.format(res["b"]["state"], res["b"]["puzzlenum"],
            #            res["b"]["layer"], res["b"]["uid"]))
            b = brd.Board(res["b"]["state"])
            b.assign_vehicles()
        return (b)

    def read_solution(self, puzzle_num):
        soln = self.return_solution(puzzle_num)
        # return (soln is not None)
        return (soln)

    def connect(self):
        self._drv = gd.driver(dbcfg.uri, auth=(dbcfg.usr, dbcfg.pw))
        self._sess = self._drv.session(database=dbcfg.db)

    def disconnect(self):
        self._drv.close()

if __name__ == "__main__":
    spn4j = StorePuzzleNeo4j()
    spn4j.read_board(20210403095022)
    spn4j.disconnect()
