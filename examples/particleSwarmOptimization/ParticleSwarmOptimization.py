import Tkinter
from time import sleep

from panacea.core.Grid import ObjectGrid2D
from panacea.core.Model import *
from panacea.core.Steppables import *
from panacea.core.helpers.GridDisplayHelper import GridDisplayHelper
from random import *

class ParticleSwarmOptimizationRenderer(GridDisplayHelper):

    def stepPrologue(self, model):
        if(self.isSetup == False):
            grid = model.getGridFromName("psogrid")
            self.setupGrid(grid)
            self.isSetup = True

    def stepEpilogue(self, model):
        self.renderGrid(model.getGridFromName("psogrid"), model.foodLocation)

    def stepMain(self, model):
        pass

    def setupGrid(self, grid):
        self.top = Tkinter.Tk()

        self.multiplier = 5

        self.gridSize = grid.getSize()
        self.gridArray = grid.getGrid()



        self.C = Tkinter.Canvas(self.top, bg="black", height = self.gridSize[1]*self.multiplier,
                           width=self.gridSize[0]*self.multiplier)

    def __init__(self,*args):

        # Not too pretty but obviously we can't load an object from an xml file,
        # so we'll be a bit creative about this just for this example and check whether
        # our grid variable is a grid object or a string pointing to the grid

        grid = args[0]

        if(isinstance(grid, ObjectGrid2D)):
            self.setupGrid(grid)
            self.isSetup = True
        else:
            self.gridName = grid
            self.isSetup = False




    def renderGrid(self, grid, foodLocation):

        self.C.create_rectangle(0,0,self.gridSize[1]*self.multiplier,self.gridSize[0]*self.multiplier,
            fill="black")

        for x in range(0,self.gridSize[1]):
            for y in range(0,self.gridSize[0]):

                agent = grid.getAtPos(Coordinates2D(x,y))

                if(len(agent) == 0):
                    continue

                agent = agent[0]

                mx = x*self.multiplier
                my = y*self.multiplier

                p = self.C.create_oval(mx,my,mx+self.multiplier, my+self.multiplier, fill=agent.displayColor)

        foodLocation = foodLocation.getCoordinates()
        p = self.C.create_rectangle(foodLocation[0]*self.multiplier,foodLocation[1]*self.multiplier,foodLocation[0]*self.multiplier+self.multiplier, foodLocation[1]*self.multiplier+self.multiplier, fill="red")

        self.C.update()
        self.C.pack()
        sleep(0.2)

class PSOModelAutoSetup(Model):

    def __init__(self, *args):
        super(PSOModelAutoSetup, self).__init__(*args)

    def setup(self):
        super(PSOModelAutoSetup, self).setup()

        self.foodLocation = Coordinates2D(self.optionalParameters["food location x"], self.optionalParameters["food location y"])
        self.gBestFit = -1
        self.gBest = Coordinates2D(0,0)

    def teardown(self):
        pass

class PSOAgent(Agent):

    def __init__(self, *args):
        if(len(args) == 1):
            args = args[0]

        radius = int(args[0])

        super(PSOAgent, self).__init__(radius)

        # Each particle will have a random color.
        self.displayColor = "#%06x" % randint(0, 0xFFFFFF)

        self.pBestFit = 0
        self.pBest = Coordinates2D(0,0)

        self.c1 = self.c2 = 2

        self.v = 0

    def stepPrologue(self, model):
        grid = model.getGridFromName("psogrid")

        # Fitness is inversely proportional to the distance from the food Location
        self.pCurrent = grid.getAgentPosition(self)

        dist = grid.getAgentPosition(self).getEuclideanDistanceFromCoordinate(model.foodLocation)

        # Preventing division by zero
        if(dist <= 0):
            self.pCurrentFit = 1000000
        else:
            self.pCurrentFit = 1/dist

        # Looks like we've done our best yet
        if(self.pCurrentFit > self.pBestFit):
            self.pBestFit = self.pCurrentFit
            self.pBest = self.pCurrent


    def stepMain(self, model):
        if(self.pCurrentFit > model.gBestFit):
            model.gBestFit = self.pCurrentFit
            model.gBest = self.pCurrent


    def stepEpilogue(self, model):

        # Standard updating according to PSO rules. And taking advantage of our custom sum and mul operators
        # in the coordinate objects
        movement = self.c1*random()*(self.pBest-self.pCurrent) + self.c2*random()*(model.gBest-self.pCurrent)

        g = model.getGridFromName("psogrid")

        # In light of recent changes, object grid positions are now also stored in the agent itself as well as in the
        # grid object, so this could be changed.
        pos = g.getAgentPosition(self)


        g.moveAgent(pos+movement, self)