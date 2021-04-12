import Vehicle as veh

class Board():
    """
    Track vehicle positions & empty spaces on the puzzle board
    """
    def __init__(self, positions=None):
        # Need this to be a copy constructor, otherwise reference confusion
        self._positions = [int(p) for p in positions]
        self._minpos = 0
        self._maxpos = 6
        self._vehicles = {}
        self._redcarsids = [0, 20]
        self._solnspaces = [(4, 2), (5,2)]
        self._veh2rm = []

    @property
    def positions(self):
        return (self._positions)

    @positions.setter
    def positions(self, val):
        self._positions = val

    @property
    def vehicles(self):
        return (self._vehicles)

    @property
    def veh2rm(self):
        return (self._veh2rm)

    def __str__(self):
        # print("positions: " + ",".join([str(p) for p in self.positions]))
        strval = ""
        for ro in range(self._maxpos):
            rostr = "\t".join([str(self._positions[idx + ro*self._maxpos])
                              for idx in range(self._maxpos)])
            strval += rostr + "\n"
        return (strval)

    def assign_vehicles(self):
        assert (len(self._positions) == (self._maxpos)**2)
        self._vehicles = {}
        for y in range(self._maxpos):
            for x in range(self._maxpos):
                idx = y * self._maxpos + x
                entry = self._positions[idx]
                if entry != -1:  # not empty
                    if entry not in self._vehicles.keys():
                        self._vehicles[entry] = veh.Vehicle(entry)
                    self._vehicles[entry].location.append((x, y))

    def move_vehicle(self, vehid, positions):
        # print("Before:\n" + str(self))
        # print("moving vehicle {0} ({2}) to {1}".format(vehid, positions,
        #                                                self._vehicles[vehid]))
        for currpos in self._vehicles[vehid].location:
            idx = currpos[0] + currpos[1] * self._maxpos
            if currpos not in positions:    # put a -1
                self._positions[idx] = -1
        for newpos in positions:
            idx = newpos[0] + newpos[1] * self._maxpos
            self._positions[idx] = vehid
        self._vehicles[vehid].location = positions
        # print("After:\n" + str(self))

    def rm_solved(self, veh2rm):
        for v2r in veh2rm:
            # print("removing vehicle {0}, id {1}".format(self._vehicles[v2r],
            #                                             v2r))
            # print(str(self))
            del self._vehicles[v2r]
            for spc in self._solnspaces:      # clear those positions
                idx = spc[1] * self._maxpos + spc[0]
                self.positions[idx] = -1
            # print(str(self))

    def solved_vehicles(self):
        self._veh2rm = []
        for vehid in self._redcarsids:
            if vehid in self._vehicles.keys():
                # check whether the vehicle is on the solution spaces
                # we know the red car only occupies 2 spaces
                veh = self._vehicles[vehid]
                if veh.location[0] in self._solnspaces and \
                        veh.location[1] in self._solnspaces:
                    # mark vehicle for removal
                    self._veh2rm.append(vehid)
        return (self._veh2rm)

    def solved(self):
        retval = True
        for vehid in self._redcarsids:
            if vehid in self._vehicles.keys():
                retval = False
                break
        return (retval)

    def empty_spaces(self):
        empties = []
        for y in range(self._maxpos):
            for x in range(self._maxpos):
                idx = y * self._maxpos + x
                if self._positions[idx] == -1:  # empty
                    empties.append((x, y))
        return (empties)

    def make_next_layer(self):
        # Create a list of boards based on this board, applying moves
        # from each of the vehicles.
        # print("in Board MNL")
        nextlayer = []
        empties = self.empty_spaces()
        for vehid in self._vehicles.keys():
            veh = self.vehicles[vehid]
            # print("Vehicle {0} = {1}".format(vehid, veh))
            mvs = veh.filteredmoves(empties)
            for mv in mvs:
                b = Board(self.positions)
                b.assign_vehicles()
                b.move_vehicle(vehid, mv)
                # print("Appending \n" + str(b))
                nextlayer.append(b)
        return (nextlayer)

    def make_solved_board(self, veh2rm):
        b = Board(self.positions)
        b.assign_vehicles()
        b.rm_solved(veh2rm)
        return(b)

if __name__ == "__main__":
    b = Board([1,1,-1,-1,-1,2,
               3,-1,-1,-1,-1,2,
               3,0,0,4,-1,2,
               3,-1,-1,4,-1,-1,
               5,-1,-1,4,6,6,
               5,-1,7,7,7,-1])
    print(b)
    b.assign_vehicles()
    for vk in b.vehicles.keys():
        print(b.vehicles[vk])
    b.move_vehicle(7, [(3,5), (4,5), (5,5)])
    print(b)
    print("_"*80 + "\nDetermine next layer:\n")
    nxtly = b.make_next_layer()
    # for nlb in nxtly:
    #     print("\n")
    #     print(nlb)

    # b = Board([-1,-1,-1,-1,-1,-1,
    #            -1,0,0,-1,-1,-1,
    #            -1,-1,-1,-1,2,-1,
    #            -1,-1,-1,-1,2,-1,
    #            -1,-1,-1,-1,-1,-1,
    #            -1,-1,-1,-1,-1,-1])
    # b.assign_vehicles()
    # print("Starting position:\n" + str(b))
    # nxtly = b.make_next_layer()

