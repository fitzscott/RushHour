from neo4j import GraphDatabase as gd
import sys
import dbcfg
from datetime import datetime

class file2board():
    def __init__(self, flnm):
        self._flnm = flnm
        self._drv = None
        self._sess = None

    def connect(self):
        self._drv = gd.driver(dbcfg.uri, auth=(dbcfg.usr, dbcfg.pw))
        self._sess = self._drv.session(database=dbcfg.db)

    def disconnect(self):
        self._drv.close()

    def savfileasboard(self, puzl=None, uniq=True):
        if puzl is None:
            dto = datetime.now()
            puzl = dto.strftime("%Y%m%d%H%M%S")
        else:
            puzl = str(puzl)
            # clear out existing boards, if needed
            clrqry = """
            MATCH (b:board {{ puzzlenum: {0} }}) 
            DETACH DELETE b
            """.format(puzl)
            self._sess.run(clrqry)

        print("Puzzle ID is " + puzl)

        fl = open(self._flnm)
        positions = []
        for ln in fl:
            ro = ln.strip().split()
            positions.extend([int(p) if p != "-" else -1 for p in ro])
        fl.close()
        print(",".join([str(p) for p in positions]))
        # In addition to the positions & puzzle #, create a field that
        # combines them to use as a unique constraint.
        if uniq:
            uniqid = "{0}_{1}".format(puzl, ",".join([str(p)
                                                      for p in positions]))
            uspec = ", uid: '{0}'".format(uniqid)
        else:
            uspec = ""
        cr8qry = """
        CREATE (:board {{state: {0}, puzzlenum: {1}, layer: 0{2}}})
        """.format(positions, puzl, uspec)
        print(cr8qry)
        self._sess.run(cr8qry)

if __name__ == "__main__":
    flnm = sys.argv[1]
    if len(sys.argv) > 2:
        puzlnum = int(sys.argv[2])
    else:
        puzlnum = None
    if len(sys.argv) > 3:
        uniq = sys.argv[3] == "1"
    else:
        uniq = True
    f2b = file2board(flnm)
    f2b.connect()
    f2b.savfileasboard(puzlnum, uniq)
    f2b.disconnect()
