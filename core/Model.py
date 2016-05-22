"""The core model object. This encapsulates all model properties and agents (Eg: Schedule, Agents, Grids, etc.)
and is responsible for setup, execution and teardown.

.. moduleauthor:: Dario Panada <dario.panada@postgrad.manchester.ac.uk>
"""

import abc
from panacea.core.utils.SetupLoader import *


class Model(object):
    """Template for all models. Once instantiated, models encapsulate all information related to the simulation.
    epochs is the number of time-steps the simulation will run for (unless another exit condition is met earlier). Models
    will usually extend this to customize setup and teardown methods.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args):
        """ Constructor function, can optionally take parameters for model setup from an external file. Please note
        that this method does NOT setup the model, it simply stores the reference to the location and type of the setup
        file. The setup method is then responsible for actually setting up.

        Args:
            args[0] (str): Relative path to the setup file.
            args[1] (str): Type of setup file, currently only our XML format is supported.

        """
        self.grids = []

        if (len(args) > 0):
            self.setupPath = args[0]
            self.setupType = args[1]
        else:
            self.setupPath = None
            self.setupType = None

        # An array of optional parameter values, this is instantiated as an empty list when the model is instantiated
        # but should be populated in the setup method
        self.optionalParameters = {}

    def getGridFromName(self, gridName):
        """ Returns the specified grid object.

        Args:
            gridName (str): The name of the grid.

        Returns:
            grid: The specified grid object.
                    OR
            None: If no such grid object is found.

        """
        # replace with lambda at some point
        for g in self.grids:
            if (g.getGridName() == gridName):
                return g

        return None

    def addSchedule(self, schedule):
        """ Adds the specified schedule object to the model.

        Args:
            schedule (schedule): The schedule object.
        """
        self.schedule = schedule

    def setEpochs(self, epochs):
        """ Sets the number of epochs the model will run for.

         Args:
             epochs (int): The number of epochs the model will run for.
        """
        self.epochs = epochs

    def addGrid(self, grid):
        """Adds a grid to the model.

        Args:
            grid (grid): The grid object
        """
        self.grids.append(grid)

    def getEpochs(self):
        """ Returns the number of epochs the model runs for.

        Returns:
            int: The number of epochs
        """
        return self.epochs

    def simulateModel(self):
        """ Runs the model as a whole. Executes setup method, simulate (the main loop) and finally teardown
        instructions.

        With regards to setup, if an external setup file has been specified the setup method will instantiate
        the appropriate loader and parametrize it with the path to such file. Any additional instructions programmed
        in the setup method will also be executed.
        """
        self.setup()
        self.simulate()
        self.teardown()

    def addOptionalParameter(self, optionalParameter):
        """ Adds an optional parameter. That is, any pair Key => (NUMERICAL) Value we want the model to store. The scope
        of optional parameters is similar to that of epochs, it's a value shared by all entities in the model.

        Args:
            optionalParameter (dictionary value) : Name of parameter => (Numerical) value. Eg: "temperature" => 15
        """
        v = float(optionalParameter["value"])


        self.optionalParameters[optionalParameter["name"]] = v

    def setup(self, *args):
        """ Sets up the model. If setupPath has been defined and setupType matches one of the known loaders
        then the loader is instantiated and the model is configured as per instructions in the external file.
        (Currently only XML is supported)

        Additional arguments can be passed depending on use cases.
        """
        if (self.setupPath is not None and self.setupType is not None):
            if (self.setupType == "xml"):
                loader = XMLLoader(self)

    def simulate(self):
        """ Responsible for running the main loop of the model. Runs the "step" method on the schedule object
        as many times are there are epochs.
        """
        for i in range(self.epochs):
            print i
            self.schedule.step(self)

    @abc.abstractmethod
    def teardown(self):
        """ Can be overridden when extending the Model class to specify any code we want executed when the simulation
        is over.
        """
        pass
