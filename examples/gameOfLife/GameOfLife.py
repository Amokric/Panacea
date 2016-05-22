from panacea.core.Coordinates import Coordinates2D
from panacea.core.Grid import ObjectGrid2D
from panacea.core.Schedule import Schedule
from panacea.core.Steppables import *
from panacea.core.Model import *
import Tkinter
from time import sleep

import random

from panacea.core.helpers.GridDisplayHelper import GridDisplayHelper


class GameOfLifeRenderer(GridDisplayHelper):
    def stepPrologue(self, model):
        if (self.isSetup == False):
            grid = model.getGridFromName("golgrid")
            self.setupGrid(grid)
            self.isSetup = True

    def stepEpilogue(self, model):
        self.renderGrid(model.getGridFromName("golgrid"))

    def stepMain(self, model):
        pass

    def setupGrid(self, grid):
        self.top = Tkinter.Tk()

        self.multiplier = 20

        self.gridSize = grid.getSize()
        self.gridArray = grid.getGrid()

        self.C = Tkinter.Canvas(self.top, bg="black", height=self.gridSize[1] * self.multiplier,
                                width=self.gridSize[0] * self.multiplier)

    def __init__(self, *args):

        # Not too pretty but obviously we can't load an object from an xml file,
        # so we'll be a bit creative about this just for this example and check whether
        # our grid variable is a grid object or a string pointing to the grid

        grid = args[0]

        if (isinstance(grid, ObjectGrid2D)):
            self.setupGrid(grid)
            self.isSetup = True
        else:
            self.gridName = grid
            self.isSetup = False

    def renderGrid(self, grid):



        self.C.create_rectangle(0, self.gridSize[1] * self.multiplier, 0, self.gridSize[0] * self.multiplier,
                                fill="black")

        for x in range(0, self.gridSize[1]):
            for y in range(0, self.gridSize[0]):

                agent = grid.getAtPos(Coordinates2D(x, y))
                agent = agent[0]

                mx = x * self.multiplier
                my = y * self.multiplier

                if (agent.state == 1):
                    p = self.C.create_rectangle(mx, my, mx + self.multiplier, my + self.multiplier,
                                                fill="red", width=3)
                else:
                    p = self.C.create_rectangle(mx, my, mx + self.multiplier, my + self.multiplier,
                                                fill="darkblue", width=3)

        self.C.update()
        self.C.pack()



class GOLCell(Agent):
    state = None
    stateNext = None

    def __init__(self, *args):

        if (len(args) == 1):
            args = args[0]

        radius = int(args[0])
        state = int(args[1])
        super(GOLCell, self).__init__(radius)
        self.state = state

    def stepPrologue(self, model):
        pass

    def stepEpilogue(self, model):
        # Making good use of our three-act timestep
        self.state = self.stateNext

    def stepMain(self, model):
        # get the grid
        grid = model.getGridFromName("golgrid")

        # use it to get our position
        coord = grid.getAgentPosition(self)

        # use the coordinates to get the moore neighbourhood
        neigh = grid.getMooreNeigh(coord)

        counter = 0

        # loop through the moore neighhbourhood
        for n in neigh:
            # getting the agent at the position
            agent = n[1][0]

            # we keep track of how many neighbours are "on"
            if (agent.state == 1):
                counter = counter + 1

        # Any live cell with two or three live neighbours lives on to the next generation.
        if (self.state == 1 and (counter == 2 or counter == 3)):
            self.stateNext = 1
        # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
        # Any live cell with more than three live neighbours dies, as if by over-population.
        elif (self.state == 1 and (counter < 2 or counter > 3)):
            self.stateNext = 0
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        elif (self.state == 0 and counter == 3):
            self.stateNext = 1
        else:
            self.stateNext = self.state

        a = 1




class GOLModelAutoSetup(Model):
    def __init__(self, *args):
        super(GOLModelAutoSetup, self).__init__(*args)

    def setup(self):
        super(GOLModelAutoSetup, self).setup()
        # self.schedule.addHelper(GameOfLifeRenderer(self.getGridFromName("golgrid")))

    def teardown(self):
        pass


class GOLModel(Model):
    def __init__(self, *args):
        super(GOLModel, self).__init__(*args)

    def teardown(self):
        pass


    def setup(self, *args):

        self.optionalParameters = {}

        epochs = 100

        self.setEpochs(epochs)

        size = 20
        grid = ObjectGrid2D(size, size, "golgrid")
        s = Schedule()

        s.addHelper(GameOfLifeRenderer(grid))

        for x in range(size):
            for y in range(size):

                if (random.random() <= 0.5):
                    state = 1
                else:
                    state = 0

                h = GOLCell([1, state])
                grid.moveAgent(Coordinates2D(x, y), h)
                s.addAgent(h)

        self.addSchedule(s)

        self.addGrid(grid)


    def teardown(self):
        pass
