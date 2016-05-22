"""This module contains blueprint for steppable objects (essentially anything that can be added to a schedule) as
well as for generic agent and helper objects.

.. moduleauthor:: Dario Panada <dario.panada@postgrad.manchester.ac.uk>
"""

import abc
import random
import hashlib

class Steppable(object):
    """General steppable element. Any steppable object can be added to a schedule.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def stepPrologue(self, model):
        """Set of instructions the steppable should execute during the 'prologue' phase.

        Args:
            model (model): The current model.
        """
        pass

    @abc.abstractmethod
    def stepMain(self, model):
        """Set of instructions the steppable should execute during the 'main' phase.

         Args:
            model (model): The current model.
        """
        pass

    @abc.abstractmethod
    def stepEpilogue(selfs, model):
        """Set of instructions the steppable should execute during the 'epilogue' phase.

         Args:
            model (model): The current model.
        """
        pass


class Helper(Steppable):
    """ A helper is a steppable which isn't a "character" or "member" of the model but is still included
    to perform auxiliary tasks. For example, record model properties at each time-step, change the state of the
    model in-between agent stepping according to some rules, etc.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *args):
        """ Simply making provisions for arguments to be provided either within a single list or explicitly.
        """
        if(len(args) == 1):
            self.args = args[0][0]

class Agent(Steppable):
    """Template for all non-helper agents in the model.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *args):
        """ We instantiate the agent.

        Args:
            radius (int): The "manhattan radius" of the agent.
            gridPositions [(str => Coordinates)] : A dictionary containing the coordinates of the agent on different
            grids. Key values in the grid are the grid names, values are coordinates objects.
        """


        self.setId(self.generateUniqueId())
        self.setRadius(args[0])
        self.gridPositions = {}


    def generateUniqueId(self):
        """ Generates a random hash id for this instance of the agent.
        """
        return hashlib.md5("a"+str(random.random())+str(random.random())+str(random.random())).hexdigest()

    def getId(self):
        """ Returns the agent's id.

        Returns:
            str: The agent's id.
        """
        return self.id

    def getRadius(self):
        """ Returns the radius of the agent.

        Returns:
            int: The agent's radius.
        """
        return self.radius

    def getGridPositions(self):
        """ Returns the position of the agent on all grids where it has been positioned.

        Returns:
            {[str => Coordinates]} : A dictionary where key values are strings, the names of grids, and values are
            coordinates indicating the agent's position on such grids.
        """
        return self.grid_positions

    def setId(self, id):
        """ Sets the agent's id.

         Args:
             id (str): The id.
        """
        self.id = id

    def setRadius(self, radius):
        """ Sets the agent's radius.

         Args:
             radius (int): The agent's radius.
        """
        self.radius = radius

    def setGridPostions(self, grid_positions):
        """ Primarily used when loading from an external file, sets all grid positions at once.

        Args:
            grid_positions {[str => Coordinates]} : A dictionary where key values are strings, the names of grids, and values are
            coordinates indicating the agent's position on such grids.1
        """
        self.grid_positions = grid_positions

    def updateGridPosition(self, grid, coordinates):
        """Given a grid object and a coordinate moves the agent to that position on such grid.

        Args:
            grid (grid): The grid object we want to move the agent on.
            coordinates (Coordinates): The coordinates we want to move the agent to.

        """
        grid.moveAgent(coordinates,self)


    def updateInternalState(self, model):
        """General method which can be used to update the object's internal state.
        Args:
            model (model): The current model object.
        """
        pass

    def __eq__(self, other):
        """ Simple comparator to determine if two agent instances are the same. They are if they have the same id.

         Args:
             other (agent): Another agent instance.

         Returns:
             bool: True if it's the same agent, false otherwise.
        """
        return self.id == other.id
