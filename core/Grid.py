"""This model defines all core grids. Grids can be Numerical Grid, which hold a single numerical grid per position,
or object grids, which can hold one or more steppables per position. Additionally, both numerical and object
grids can be 2D or 3D."""

import abc
import numpy
from random import shuffle

from panacea.core.Coordinates import Coordinates2D, Coordinates3D


class Grid(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, gridName):
        """ Constructor, defines the grid name which must be unique within the model.

        Args:

            gridName (string): The name of the grid.
        """
        self.gridName = gridName

    @abc.abstractmethod
    def getSize(self):
        """ Returns the size of the grid

        Returns:

            (int, int) OR (int, int, int) : A tuple or triple containing the x-size, y-size and eventually
            z-size of the grid.
        """
        pass

    @abc.abstractmethod
    def getGrid(self):
        """ Returns the grid object

        Returns:

            (grid): The current object.
        """
        pass

    def getGridName(self):
        """ Returns the name of the grid

        Returns:

            string: The name of the grid.
        """
        return self.gridName

    @abc.abstractmethod
    def getMooreNeigh(self, coordinates):
        """ Returns the values/agents in all moore neighbourhood (radius 1) coordinates with respect to a given
        coordinate.

        Args:

            coordinates (Coordinates): The coordinates object pointing to the center of the moore
            neighbourhood.

        Returns:

            [(Coordinates => CellValue)]: A list of tuples where the first element is a coordinate and the second
            element is the value at such coordinate. Either a list of agents for an ObjectGrid or a list of doubles
            for a numerical grid.

        """
        pass


class NumericalGrid(Grid):
    """ A prototype for a numerical grid. A numerical grid will hold a single numerical value per position.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def setAllGridValues(self, value):
        """ This method allows to set all grid positions to a given value.

        Args:

            value (double): The value to which all positions will be set.
        """
        pass

    @abc.abstractmethod
    def setGridValue(self, coordinate, value):
        """ Sets the value of a particular position.

        Args:
            coordinate (Coordinates): The position we are setting the value for.
            value (double): The value we are setting.
        """
        pass

    @abc.abstractmethod
    def getGridValue(self, coordinate):
        """ Returns the value of a particular position.

        Args:

            coordinate (Coordinates): The position we are retrieving the value for.

        Returns:

            double: The value at such position.
        """
        pass


class NumericalGrid2D(NumericalGrid):
    """ An implementation of a 2D Numerical Grid
    """
    def __init__(self, *args):
        """ Constructor method, sets the size of the grid and the grid's name, by default all grid values
        are set to zero.

        Args:

            xsize (int): The width of the grid.
            ysize (int): The height of the grid.
            name (string): The name of the grid.

                OR
            listOfParameters (list): A list of form [(int) xsize, (int) ysize, (string) name]
        """
        if(len(args) == 1):
            args = args[0]
            args[0] = int(args[0])
            args[1] = int(args[1])
            
        xsize = args[0]
        ysize = args[1]
        gridName = args[2]

        super(NumericalGrid2D, self).__init__(gridName)
        self.xsize = xsize
        self.ysize = ysize
        self.grid = numpy.zeros((xsize, ysize))

    def getGrid(self):
        """ Returns the grid object

        Returns:

            (grid): The current object.
        """
        return self.grid

    def getSize(self):
        """ Returns the size of the grid

        Returns:

            (int, int) : A tuple containing the x-size and y-size of the grid.
        """
        return (self.xsize, self.ysize)

    def setAllGridValues(self, value):
        """ This method allows to set all grid positions to a given value.

        Args:

            value (double): The value to which all positions will be set.
        """
        newGrid = numpy.ones((self.xsize, self.ysize))
        newGrid = value * newGrid

        self.grid = newGrid

    def setGridValue(self, coordinates, value):
        """ Sets the value of a particular position.

        Args:
            coordinate (Coordinates2D): The position we are setting the value for.
            value (double): The value we are setting.
        """
        coordinates = coordinates.getCoordinates()
        self.grid[coordinates[0], coordinates[1]] = value

    def getGridValue(self, coordinates):
        """ Returns the value of a particular position.

        Args:

            coordinate (Coordinates2D): The position we are retrieving the value for.

        Returns:

            double: The value at such position.
        """
        coordinates = coordinates.getCoordinates()
        return self.grid[coordinates[0], coordinates[1]]

    def getMooreNeigh(self, coordinates):
        """ Returns the values all moore neighbourhood (radius 1) coordinates with respect to a given
        coordinate.

        Args:

            coordinates (Coordinates2D): The coordinates object pointing to the center of the moore
            neighbourhood.

        Returns:

            [(Coordinates => Double)]: A list of tuples where the first element is a coordinate and the second
            element is the value at such coordinate.
        """
        mooreNeigh = coordinates.getMooreNeigh(self)

        neigh = []

        for m in mooreNeigh:
            neigh.append((m, self.getGridValue(m)))

        return neigh


class NumericalGrid3D(NumericalGrid):
    """ An implementation of a 3D Numerical Grid
    """

    def __init__(self, xsize, ysize, zsize, gridName):
        """ Constructor method, sets the size of the grid and the grid's name, by default all grid values
        are set to zero.

        Args:

            xsize (int): The width of the grid.
            ysize (int): The length of the grid.
            zsize (int): The height of the grid.
            name (string): The name of the grid.

                OR
            listOfParameters (list): A list of form [(int) xsize, (int) ysize, (int) zsize, (string) name]
        """
        super(NumericalGrid3D, self).__init__(gridName)
        self.xsize = xsize
        self.ysize = ysize
        self.zsize = zsize
        self.grid = numpy.zeros((xsize, ysize, zsize))

    def getGrid(self):
        """ Returns the grid object

        Returns:

            (grid): The current object.
        """
        return self.grid

    def getSize(self):
        """ Returns the size of the grid

        Returns:

            (int, int, int) : A tuple containing the x-size, y-size and z-size of the grid.
        """
        return (self.xsize, self.ysize, self.zsize)

    def setAllGridValues(self):
        """ This method allows to set all grid positions to a given value.

        Args:

            value (double): The value to which all positions will be set.
        """
        pass

    def setGridValue(self, coordinates, value):
        """ Sets the value of a particular position.

        Args:
            coordinate (Coordinates3D): The position we are setting the value for.
            value (double): The value we are setting.
        """
        coordinates = coordinates.getCoordinates()
        self.grid[coordinates[0], coordinates[1], coordinates[2]] = value

    def getGridValue(self, coordinates):
        """ Returns the value of a particular position.

        Args:

            coordinate (Coordinates3D): The position we are retrieving the value for.

        Returns:

            double: The value at such position.
        """
        coordinates = coordinates.getCoordinates()
        return self.grid[coordinates[0], coordinates[1], coordinates[2]]

    def getMooreNeigh(self, coordinates):
        """ Returns the values all moore neighbourhood (radius 1) coordinates with respect to a given
        coordinate.

        Args:

            coordinates (Coordinates3D): The coordinates object pointing to the center of the moore
            neighbourhood.

        Returns:

            [(Coordinates => Double)]: A list of tuples where the first element is a coordinate and the second
            element is the value at such coordinate.
        """
        pass


class ObjectGrid(Grid):
    __metaclass__ = abc.ABCMeta


    def __init__(self, gridName):
        """ Constructor method, sets the name of the grid and initializes the grid with no agents.

        Args:

            gridName (str): The name of the grid.
        """
        self.gridAgents = []
        super(ObjectGrid, self).__init__(gridName)


    @abc.abstractmethod
    def getAtPos(self, coordinates):
        """ Returns a list containing all agents at a given position.

        Args:
            coordinates (Coordinates): The coordinates we are interested in.

        Returns:
            [agent] : A list of agents containing all agents at such position.
        """
        pass

    @abc.abstractmethod
    def moveAgent(self, coordinates, agent):
        """ Moves an agent to a certain position on the grid. If the agent wasn't on the grid, it is added.

         Args:
             coordinates (Coordinates): The coordinates we want to move the agent to.
             agent (Agent): The agent we want to move.
        """
        pass

    @abc.abstractmethod
    def getAgentPosition(self, agent):
        """ Returns the position of an agent on this grid.

        Args:
            agent (Agent): The agent whose position we want to find.

        Returns:
            Coordinates: Coordinates representing the position of the agent.
        """
        pass

    @abc.abstractmethod
    def removeAgent(self, agent):
        """ Removes an agent from the grid.

        Args:
            agent (Agent): The agent we want to remove.
        """
        pass

    @abc.abstractmethod
    def getLeastPopulatedMooreNeigh(self, coordinates):
        """ Returns the coordinates of the moore neighbour with the fewest agents. If there are more than one
        with equally few agents, a random one is returned.

        Args:
            coordinates (Coordinates): The coordinates around which the moore neighbourhood will be centered.

        Returns:
            Coordinates: The coordinates referring to the least populated moore neighbourhood.
        """
        pass

    @abc.abstractmethod
    def getMostPopulatedMooreNeigh(self, coordinates):
        """ Returns the coordinates of the moore neighbour with the most agents. If there are more than one
        with equally many agents, a random one is returned.

        Args:
            coordinates (Coordinates): The coordinates around which the moore neighbourhood will be centered.

        Returns:
            Coordinates: The coordinates referring to the most populated moore neighbourhood.
        """
        pass


class ObjectGrid2D(ObjectGrid):
    """ An implementation of an ObjectGrid2D.
    """

    def __init__(self, *args):
        """ Initializes the grid. Initially, all positions are empty.

         Args:
             xsize (int): The width of the grid.
             ysize (int): The length of grid.
             name (str): The name of the grid.

                OR

            [(int) xsize, (int) ysize, (str) name] : A list containing the three parameters.
        """

        # Not a beautiful solution but we need to account for arguments being given explicitly
        # (xsize, ysize, name) or as a list [xsize, ysize, name]
        if(len(args) == 1):
            args = args[0]

            args[0] = int(args[0])
            args[1] = int(args[1])

        xsize = args[0]
        ysize = args[1]
        name = args[2]

        super(ObjectGrid2D, self).__init__(name)
        self.xsize = args[0]
        self.ysize = args[1]

        # creating the general grid object
        grid = []

        for i in range(xsize):

            # creating a column
            col = []

            for j in range(ysize):
                # adding row elements to the column
                col.append([])

            grid.append(col)

        self.grid = grid

    def getSize(self):
        """ Returns the size of the grid

        Returns:

            (int, int) : A tuple containing the x-size and y-size of the grid.
        """
        return (self.xsize, self.ysize)

    def getGrid(self):
        """ Returns the grid object

        Returns:

            (grid): The current object.
        """
        return self.grid

    def getAtPos(self, coordinates):
        """ Returns a list containing all agents at a given position.

        Args:
            coordinates (Coordinates2D): The coordinates we are interested in.

        Returns:
            [agent] : A list of agents containing all agents at such position.
        """
        coordinates = coordinates.getCoordinates()

        x = coordinates[0]
        y = coordinates[1]

        agentsAtPos = []

        for a in self.gridAgents:
            a = a[1]
            agentPos = self.getAgentPosition(a)

            agentRadius = a.getRadius()
            agentCoords = agentPos.getCoordinates()

            agentX = agentCoords[0]
            agentY = agentCoords[1]

            # Remember agents with radius > 1 span multiple grid cells. This is where we make sure we include
            # all agents spanning into this cell and not only those centered at it.
            if((agentX-(agentRadius-1) <= x and agentX+(agentRadius-1) >= x)) and ( (agentY-(agentRadius-1) <= y and agentY+(agentRadius-1) >= y )):
                agentsAtPos.append(a)

        return agentsAtPos


    def moveAgent(self, coordinates, agent):
        """ Moves an agent to a certain position on the grid. If the agent wasn't on the grid, it is added.

         Args:
             coordinates (Coordinates2D): The coordinates we want to move the agent to.
             agent (Agent): The agent we want to move.
        """

        # The actual x/y tuple representing the coordinates we want to move our agent to
        coordinatesTuple = coordinates.getCoordinates()

        # We first check if the agent is known to the grid
        matching = [agent_coords for agent_coords in self.gridAgents if agent_coords[1] == agent]

        # Storing the agent's position for this grid in the agent itself too
        agent.gridPositions[self.gridName] = coordinates

        if (len(matching) == 0):
            # The agent is not known to the system, let's make them known
            self.gridAgents.append((coordinates, agent))

            # And we add them to the grid
            self.grid[coordinatesTuple[0]][coordinatesTuple[1]].append(agent)

        else:

            x = coordinatesTuple[0]
            y = coordinatesTuple[1]


            # preventing an agent from moving off the grid
            if(x < 0):
                x = 0

            if(x > self.xsize-1):
                x = self.xsize-1

            if(y < 0):
                y = 0

            if(y > self.ysize-1):
                y = self.ysize-1

            coordinates = Coordinates2D(x,y)

            # getting the tuple representing the current location
            listTuple = matching[0]

            # from it, we get its current position
            coordinatesOld = listTuple[0].getCoordinates()

            # creating a new tuple representing the new coordinates
            newTuple = (coordinates, agent)

            # and registering it
            loc = self.gridAgents.index(listTuple)
            self.gridAgents[loc] = newTuple

            # physically removing the agent from the old position on the grid
            self.grid[coordinatesOld[0]][coordinatesOld[1]].remove(agent)




            # ...and physically adding it to the new position on the grid
            self.grid[x][y].append(agent)

    def getAgentPosition(self, agent):
        """ Returns the position of an agent on this grid.

        Args:
            agent (Agent): The agent whose position we want to find.

        Returns:
            Coordinates2D: Coordinates representing the position of the agent.
        """
        return agent.gridPositions[self.gridName]

    def removeAgent(self, agent):
        """ Removes an agent from the grid.

        Args:
            agent (Agent): The agent we want to remove.
        """

        agentPosition = self.getAgentPosition(agent)

        agentCoords = agentPosition.getCoordinates()

        matching = [agent_coords for agent_coords in self.gridAgents if agent_coords[1] == agent]

        # removing the agent from the agent grid
        self.gridAgents.remove(matching[0])

        self.grid[agentCoords[0]][agentCoords[1]].remove(agent)

    def getMooreNeigh(self, coordinates):
        """ Returns moore neighbourhood coordinates and a list of agents at each such coordinate.

        Args:
            coordinates (Coordinates2D): The coordinates around which the moore neighbourhood will be centered.

        Returns:
            [(Coordinates2D, [Agent])] : A list of tuples where the first element is a coordinate and the second
            element is the list of agents at such position.
        """
        mooreCoords = coordinates.getMooreNeigh(self)

        neigh = []

        for c in mooreCoords:
            agentsAtCoords = self.getAtPos(c)
            neigh.append((c, agentsAtCoords))

        return neigh

    def getLeastPopulatedMooreNeigh(self, coordinates):
        """ Returns the coordinates of the moore neighbour with the fewest agents. If there are more than one
        with equally few agents, a random one is returned.

        Args:
            coordinates (Coordinates2D): The coordinates around which the moore neighbourhood will be centered.

        Returns:
            Coordinates2D: The coordinates referring to the least populated moore neighbourhood.
        """
        mooreNeigh = self.getMooreNeigh(coordinates)
        shuffle(mooreNeigh)

        first = mooreNeigh[0]

        bestCoord = first[0]
        highestPop = len(first[1])

        for n in mooreNeigh:
            c = n[0]
            a = n[1]
            nA = len(a)

            if (nA <= highestPop):
                highestPop = nA
                bestCoord = c

        return bestCoord

    def getMostPopulatedMooreNeigh(self, coordinates):
        """ Returns the coordinates of the moore neighbour with the most agents. If there are more than one
        with equally many agents, a random one is returned.

        Args:
            coordinates (Coordinates2D): The coordinates around which the moore neighbourhood will be centered.

        Returns:
            Coordinates2D: The coordinates referring to the most populated moore neighbourhood.
        """
        mooreNeigh = self.getMooreNeigh(coordinates)
        shuffle(mooreNeigh)

        first = mooreNeigh[0]

        bestCoord = first[0]
        highestPop = len(first[1])

        for n in mooreNeigh:
            c = n[0]
            a = n[1]
            nA = len(a)

            if (nA >= highestPop):
                highestPop = nA
                bestCoord = c

        return bestCoord


class ObjectGrid3D(ObjectGrid):
    """ An implementation of a 3D Object Grid
    """


    def __init__(self, *args):
        """ Initializes the grid. Initially, all positions are empty.

         Args:
             xsize (int): The width of the grid.
             ysize (int): The length of grid.
             zsize (int): The height of the grid.
             name (str): The name of the grid.

                OR

            [(int) xsize, (int) ysize, (int) zsize, (str) name] : A list containing the three parameters.
        """

        # Not a beautiful solution but we need to account for arguments being given explicitly
        # (xsize, ysize, name) or as a list [xsize, ysize, name]

        # Not a beautiful solution but we need to account for arguments being given explicitly
        # (xsize, ysize, name) or as a list [xsize, ysize, name]
        if(len(args) == 1):
            args = args[0]

            args[0] = int(args[0])
            args[1] = int(args[1])
            args[2] = int(args[2])

        xsize = args[0]
        ysize = args[1]
        zsize = args[2]
        name = args[3]

        super(ObjectGrid3D, self).__init__(name)
        self.xsize = args[0]
        self.ysize = args[1]
        self.zsize = args[2]

        # creating the general grid object
        grid = []

        for i in range(xsize):

            # creating a column
            col = []

            for j in range(ysize):
                # adding row elements to the column

                colB = []

                for k in range(zsize):
                    colB.append([])

                col.append(colB)

            grid.append(col)

        self.grid = grid

    def getGrid(self):
        """ Returns the grid object

        Returns:

            (grid): The current object.
        """
        return self.grid

    def getMooreNeigh(self, coordinates):
        """ Returns moore neighbourhood coordinates and a list of agents at each such coordinate.

        Args:
            coordinates (Coordinates3D): The coordinates around which the moore neighbourhood will be centered.

        Returns:
            [(Coordinates3D, [Agent])] : A list of tuples where the first element is a coordinate and the second
            element is the list of agents at such position.
        """

        mooreCoords = coordinates.getMooreNeigh(self)

        neigh = []

        for c in mooreCoords:
            agentsAtCoords = self.getAtPos(c)
            neigh.append((c, agentsAtCoords))

        return neigh

    def moveAgent(self, coordinates, agent):
        """ Moves an agent to a certain position on the grid. If the agent wasn't on the grid, it is added.

         Args:
             coordinates (Coordinates3D): The coordinates we want to move the agent to.
             agent (Agent): The agent we want to move.
        """

        # The actual x/y tuple representing the coordinates we want to move our agent to
        coordinatesTuple = coordinates.getCoordinates()

        # We first check if the agent is known to the grid
        matching = [agent_coords for agent_coords in self.gridAgents if agent_coords[1] == agent]

        agent.gridPositions[self.gridName] = coordinates

        if (len(matching) == 0):
            # The agent is not known to the system, let's make them known
            self.gridAgents.append((coordinates, agent))

            # And we add them to the grid
            self.grid[coordinatesTuple[0]][coordinatesTuple[1]][coordinatesTuple[2]].append(agent)

        else:

            x = coordinatesTuple[0]
            y = coordinatesTuple[1]
            z = coordinatesTuple[2]

            # preventing an agent from moving off the grid
            if(x < 0):
                x = 0

            if(x > self.xsize-1):
                x = self.xsize-1

            if(y < 0):
                y = 0

            if(y > self.ysize-1):
                y = self.ysize-1

            if(z < 0):
                z = 0

            if(z > self.zsize-1):
                z = self.zsize-1

            coordinates = Coordinates3D(x,y,z)

            # getting the tuple representing the current location
            listTuple = matching[0]

            # from it, we get its current position
            coordinatesOld = listTuple[0].getCoordinates()

            # creating a new tuple representing the new coordinates
            newTuple = (coordinates, agent)

            # and registering it
            loc = self.gridAgents.index(listTuple)
            self.gridAgents[loc] = newTuple

            # physically removing the agent from the old position on the grid
            self.grid[coordinatesOld[0]][coordinatesOld[1]][coordinatesOld[2]].remove(agent)




            # ...and physically adding it to the new position on the grid
            self.grid[x][y].append(agent)


    def getSize(self):
        """ Returns the size of the grid

        Returns:

            (int, int, int) : A tuple containing the x-size and y-size of the grid.
        """
        return (self.xsize, self.ysize, self.zsize)

    def getAgentPosition(self, agent):
        """ Returns the position of an agent on this grid.

        Args:
            agent (Agent): The agent whose position we want to find.

        Returns:
            Coordinates3D: Coordinates representing the position of the agent.
        """
        return agent.gridPositions[self.gridName]

    def getAtPos(self, coordinates):
        """ Returns a list containing all agents at a given position.

        Args:
            coordinates (Coordinates3D): The coordinates we are interested in.

        Returns:
            [agent] : A list of agents containing all agents at such position.
        """

        coordinates = coordinates.getCoordinates()

        x = coordinates[0]
        y = coordinates[1]
        z = coordinates[2]

        agentsAtPos = []

        for a in self.gridAgents:
            a = a[1]
            agentPos = self.getAgentPosition(a)

            agentRadius = a.getRadius()
            agentCoords = agentPos.getCoordinates()

            agentX = agentCoords[0]
            agentY = agentCoords[1]
            agentZ = agentCoords[2]

            if((agentX-(agentRadius-1) <= x and agentX+(agentRadius-1) >= x)) and ( (agentY-(agentRadius-1) <= y and agentY+(agentRadius-1) >= y )) and ((agentZ-(agentRadius-1) <= z and agentZ+(agentRadius-1) >= z )):
                agentsAtPos.append(a)

        return agentsAtPos

    def getLeastPopulatedMooreNeigh(self, coordinates):
        """ Returns the coordinates of the moore neighbour with the fewest agents. If there are more than one
        with equally few agents, a random one is returned.

        Args:
            coordinates (Coordinates3D): The coordinates around which the moore neighbourhood will be centered.

        Returns:
            Coordinates3D: The coordinates referring to the least populated moore neighbourhood.
        """
        mooreNeigh = self.getMooreNeigh(coordinates)
        shuffle(mooreNeigh)

        first = mooreNeigh[0]

        bestCoord = first[0]
        highestPop = len(first[1])

        for n in mooreNeigh:
            c = n[0]
            a = n[1]
            nA = len(a)

            if (nA <= highestPop):
                highestPop = nA
                bestCoord = c

        return bestCoord


    def getMostPopulatedMooreNeigh(self, coordinates):
        """ Returns the coordinates of the moore neighbour with the most agents. If there are more than one
        with equally many agents, a random one is returned.

        Args:
            coordinates (Coordinates3D): The coordinates around which the moore neighbourhood will be centered.

        Returns:
            Coordinates2D: The coordinates referring to the most populated moore neighbourhood.
        """
        mooreNeigh = self.getMooreNeigh(coordinates)
        shuffle(mooreNeigh)

        first = mooreNeigh[0]

        bestCoord = first[0]
        highestPop = len(first[1])

        for n in mooreNeigh:
            c = n[0]
            a = n[1]
            nA = len(a)

            if (nA >= highestPop):
                highestPop = nA
                bestCoord = c

        return bestCoord

    def removeAgent(self, agent):
        """ Removes an agent from the grid.

        Args:
            agent (Agent): The agent we want to remove.
        """

        agentPosition = self.getAgentPosition(agent)

        agentCoords = agentPosition.getCoordinates()

        matching = [agent_coords for agent_coords in self.gridAgents if agent_coords[1] == agent]

        # removing the agent from the agent grid
        self.gridAgents.remove(matching[0])

        self.grid[agentCoords[0]][agentCoords[1]][agentCoords[2]].remove(agent)